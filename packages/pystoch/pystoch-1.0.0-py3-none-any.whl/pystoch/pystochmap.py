# Copyright (C) 2019 IUCAA-GW Group
#
# This program is part of pystoch
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# If not, see <http://www.gnu.org/licenses/>.
#=============================================================================#
#=============================================================================#
import sys
import h5py
import numpy as np
import healpy as hp
from matplotlib import pyplot as plt
import warnings
warnings.filterwarnings('ignore')


def read_hdf(hdf_file):
    """
    Read the hdf5 data file

    Parameters
    ----------
    hdf_file: string
              Full path to input .hdf5 file

    Returns
    -------
    gps time: numpy array
              GPS time of the given data

    fre_inf: numpy array
             Frequency information of the given data

    csd: numpy array
         Cross Spectral Density (CSD)

    sigma_sq_inv: numpy array
                  Sigma square inverse
    """
    check_extension       = hdf_file.split('.')
    if check_extension[1] =="hdf5":
        load_hdf5         = h5py.File(hdf_file, "r")
        csd               = load_hdf5['csd'][:]
        sigma_sq_inv      = load_hdf5['sigma_sq_inv'][:]
        fre_info          = load_hdf5['Freinfo'][:]
        gps_time          = load_hdf5['GPStime'][:]
        load_hdf5.close()
        print ("#---- Read HDF5 data file ")
        return gps_time,fre_info,csd,sigma_sq_inv
    else:
        print ("!---- HDF5 data file is not found ")
        sys.exit()
    return


def dirty_map_matrix(cmb_antresp,tdelay,fre_info,csd,sigma_sq_inv,
                     segDuration,nside,flow,fhigh,injection,output_path):
    """
    Calculate: Dirty map matrix, Dirty map injection matrix,
    Fisher diagonal matrix and Convolution matrix

    Parameters
    ----------
    cmb_antresp: numpy array
                 Combined Antenna Response

    tdelay: numpy array
            Time delay between the two detectors

    fre_info: numpy array
              Lower frequency, Higher frequency and Delta frequency

    csd: numpy array
         Combined Spectral Density

    sigma_sq_inv: numpy array
                  Sigma Square Inverse

    segDuration: float
                 Time segment duration

    nside: integer
           Input value power of two

    flow: float
          Lower frequency

    fhigh: float
           Higher frequency

    injection: Boolean
               Injection

    Returns
    -------
    maps_output: HDF5 file
                 HDF5 file Contains: Frequency Array, Dirty map matrix, 
                 Dirty map,Dirty map injection,Fisher Diagonal matrix
    """
    npix        = hp.nside2npix(nside)
    map_inj     = np.zeros(npix)

    if injection:
        map_inj[int(npix/2+nside*2)]=1e-50

    delta_f     = fre_info[2]
    freq_array  = np.arange(flow,fhigh,delta_f)

    dmat        = []    # Dirty map matrix
    dmat_inj    = []    # Dirty map injection matrix 
    fisher_diag = []    # Fisher diagonal maxtrix

    for i in range(0,len(freq_array)):
        gamma          = cmb_antresp*np.exp(2*np.pi*1j*freq_array[i]*tdelay)
        gamma_conju    = np.conjugate(gamma)
        map_dirty_f    = np.dot(csd[:,i],gamma_conju)*segDuration
        csd_inj        = np.dot(gamma,map_inj)*segDuration
        csd_inj        = csd_inj*sigma_sq_inv[:,i] + csd[:,i]
        map_dirty_f_inj= np.dot(csd_inj,gamma_conju)*segDuration
        fisher_diag_f  = np.dot(sigma_sq_inv[:,i],np.square(abs(gamma))) \
                                *segDuration**2
        dmat.append(map_dirty_f)
        dmat_inj.append(map_dirty_f_inj)
        fisher_diag.append(fisher_diag_f)

    map_dirty           = np.sum(np.array(dmat) ,axis=0)
    map_dirty_inj       = np.sum(np.array(dmat_inj) ,axis=0)
    fisher_diag         = np.sum(np.array(fisher_diag) ,axis=0)

    rslash_opath = output_path.rstrip('/') # Remove slash at the end, if exist
    output_dir   = rslash_opath +'/'
    map_filename = 'maps_'+str(nside)+'.hdf5'
    maps_output  = h5py.File(output_dir+map_filename, "w")
    maps_output.create_dataset('Frequency', data = freq_array)
    maps_output.create_dataset('map_dirty', data = map_dirty)
    maps_output.create_dataset('map_dirty_mat', data = np.array(dmat))
    maps_output.create_dataset('map_dirty_inj', data = map_dirty_inj)
    maps_output.create_dataset('map_dirty_inj_mat', data = np.array(dmat_inj))
    maps_output.create_dataset('fisher_diag', data = fisher_diag)
    maps_output.close()
    print ("#---- Dirty map HDF5 is created ")
    print ("      Path : ",output_dir)
    print ("      Filename : ",map_filename)
    return output_dir+map_filename


def plot_pystochmap(nside,map_data,injection=None,all_freq_maps=None):
    """
    Generate Map from the given hdf5 data file

    Parameters
    ----------
    nside: integer
           Input value power of two

    map_data: HDF5 file
              HDF5 data file for map

    injection: Boolean
               Injection

    all_freq_maps: Boolean
                   Generate all narrow band maps in the given frequency

    Returns
    -------
    None
    """
    # Check nside is power of two or no 
    ns          = nside
    if (ns == 0):
        print ("!---- Nside must be a power of 2, less than 2**30 ")
        sys.exit()
    while (ns != 1):
        if (ns % 2 != 0):
            print ("!---- Nside must be a power of 2, less than 2**30 ")
            sys.exit()
        ns = ns // 2
    
    # Injection: Default = False
    if injection==None:
        injection   = False

    # Draw narrow band maps input: Default = 70.3 170 270 470
    if all_freq_maps==None:
        all_freq_maps = False

    check_extension       = map_data.split('.')
    map_imagename         = check_extension[0]

    if check_extension[1] =="hdf5":
        print ("#---- Read Map HDF5 data file ")
        load_hdf5         = h5py.File(map_data, "r")
        frequency         = load_hdf5['Frequency'][:]
        map_dirty         = load_hdf5['map_dirty'][:]
        map_dirty_inj     = load_hdf5['map_dirty_inj'][:]
        map_dirty_mat     = load_hdf5['map_dirty_mat'][:]
        map_dirty_inj_mat = load_hdf5['map_dirty_inj_mat'][:]
        load_hdf5.close()

        nFreqBin          = len(frequency)
        npix = hp.nside2npix(nside)
        map_inj = np.zeros(npix)
        map_res = 300

        hp.mollview(np.real(map_dirty), title="Dirty Map",nest=False)
        plt.savefig(map_imagename+'_dirty'+'.png',dpi = map_res)

        hp.mollview(np.real(map_dirty_inj),
                    title="Dirty Map - Injection",nest=False)
        plt.savefig(map_imagename+'_dirty_inj'+'.png',dpi = map_res)

        if injection:
            map_inj[int(npix/2+nside*2)]=1e-50
            hp.mollview(np.real(map_inj*nFreqBin),
                        title="Injected Map",nest=False)
            plt.savefig(map_imagename+'_inj'+'.png',dpi = map_res)

        if all_freq_maps:
            for ii in range(0,len(frequency)):
                str_frequency= str(frequency[ii])
                title_str_fre=str_frequency.replace('.','d')
                title1 ="Dirty Map at : "+str(frequency[ii])+" (Hz)"
                hp.mollview(np.real(map_dirty_mat[ii][:]),
                            title=title1,nest=False)
                plt.savefig(map_imagename+'_dirty_'+title_str_fre+'.png',
                            dpi = map_res)

                title2 ="Dirty Map - Injection at : " \
                         +str(frequency[ii])+" (Hz)"
                hp.mollview(np.real(map_dirty_inj_mat[ii][:]),
                            title=title2,nest=False)
                plt.savefig(map_imagename+'_dirty_inj_'+title_str_fre+'.png',
                            dpi = map_res)

        plt.close('all')
        print ('#---- Maps are Created ')
    else:
        print ("!---- Map HDF5 data file is not found ")
        sys.exit()
