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
import numpy as np
import healpy as hp
from detectors import*


def nside_pix2ang(nside):
    """
    The healpix nside parameter to angle theta and phi

    Parameters
    ----------
    nside: integer
           Must be a power of 2, less than 2**30

    Returns
    -------
    ntheta: float scalar or array-like
            Angular coordinates corresponding to pixel indices

    nphi: float, scalar or array-like
          Angular coordinates corresponding to pixel indices
    """
    ntheta, nphi  = hp.pix2ang(nside, np.arange(hp.nside2npix(nside)))
    return ntheta, nphi


def combined_antenna_response(ifo1,ifo2,gps_tarray,theta,phi,psi=None):
    """
    Combined antenna response and time delay between two Gravitational wave
    interferometry detectors in the given GPS time

    The velocity of light in vaccum

    C_SI  = 299792458e0    m s^-1

    Parameters
    ----------
    ifo1: string
          The First interferometery name.

    ifo2: string
          The Second interferometery name.

    gps_tarray: array-like
                Global Positioning System Time.

    phi: list or array-like
         Range = [0, 2 pi)
         The right ascension angle (in rad) of the signal.

    theta: list or array-like
           Range = [0, pi]
           The declination angle (in rad) of the signal 

    psi: list or array-like
         Range = [0, pi) 
         The polarization angle (in rad) of the source.

    Returns
    -------
    combined_response: array-like
                       Combined Antenna Response FPlus and FCross from the two
                       Gravitational wave interferometery detectors

    time_delay: array-like
                Time delay between two Gravitational wave 
                interferometery detectors.
    """
    # Get the detector information 
    combined_response   = []
    time_delay          = []

    for gg in range(0,len(gps_tarray)):
        total_fp1   = []
        total_fc1   = []
        total_fp2   = []
        total_fc2   = []
        total_td    = []
        for jj in range(0,len(theta)):
            fplus_det1,fcross_det1=antenna_response(ifo1,gps_tarray[gg],
                                                    phi[jj],theta[jj])
            fplus_det2,fcross_det2=antenna_response(ifo2,gps_tarray[gg],
                                                    phi[jj],theta[jj])
            total_fp1.append(fplus_det1)
            total_fp2.append(fplus_det2)
            total_fc1.append(fcross_det1)
            total_fc2.append(fcross_det2)
            toa_det1= arrival_time(ifo1,gps_tarray[gg],phi[jj],theta[jj])
            toa_det2= arrival_time(ifo2,gps_tarray[gg],phi[jj],theta[jj])
            total_td.append(toa_det2-toa_det1)

        comb_resp = (np.asarray(total_fp1) * np.asarray(total_fp2)) \
                    + (np.asarray(total_fc1) * np.asarray(total_fc2))
        combined_response.append(np.asarray(comb_resp))
        time_delay.append(np.asarray(total_td))
    return np.asarray(combined_response),np.asarray(time_delay)
