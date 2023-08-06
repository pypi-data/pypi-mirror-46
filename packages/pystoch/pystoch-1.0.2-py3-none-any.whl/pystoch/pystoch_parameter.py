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
import os
import sys
import configparser
import warnings
warnings.filterwarnings('ignore')


def parameter_file(para_file):
    """
    Validate the parameters from the input file

    Parameters
    ----------
    para_file: string
               Full path to input .ini file

    Returns
    -------
    parameter_list: list
                    Validated input from the parameter file
    """
    extract_para    = configparser.ConfigParser()
    extract_para.read(para_file)

    # Check nside is power of two or no 
    nside       = extract_para.getint('parameters', 'nside')
    ns          = nside
    if (ns == 0):
        print ("      !---- Nside must be a power of 2, less than 2**30 ")
        sys.exit()
    while (ns != 1):
        if (ns % 2 != 0):
            print ("      !---- Nside must be a power of 2, less than 2**30 ")
            sys.exit()
        ns = ns // 2

    # Check the given detectors
    ifo1        = extract_para.get('parameters', 'ifo1')
    ifo2        = extract_para.get('parameters', 'ifo2')
    detector_list   =   ["GEO","G1","G","LHO","H1","H2","H","LLO","L1","L",
                        "VIRGO","V1","V"]
    in_detector     = [ifo1,ifo2]
    if not bool(set(in_detector).issubset(set(detector_list))):
        print ("      !---- Detector name should be from the list")
        print ("           ",detector_list)
        sys.exit()

    # Check lower frequency cut off
    f_lower     = extract_para.getfloat('parameters', 'f_lower')
    if f_lower <20:
        print ("      !---- Minimum lower frequency is 20 Hz ")
        sys.exit()

    # Check higher frequency cut off
    f_higher    = extract_para.getfloat('parameters', 'f_higher')
    if f_higher >512:
        print ("      !---- Maximum higher frequency is 512 Hz ")
        sys.exit()

    # Check the analysis hdf5 exist or not 
    frame_loc   =extract_para.get('parameters', 'frames_location')
    check_extension = frame_loc.split('.')
    if (check_extension[1] !="hdf5"):
        print ("      !---- HDF5 input file not exist")
        sys.exit()

    # Check the output directory exist or not
    output_loc  = extract_para.get('parameters', 'output_location')
    if not os.path.exists(output_loc):
        print ("      !---- Out put directory is created")
        os.makedirs(output_loc)

    # Overlap: Default = False
    try:
        overlap = extract_para.getboolean('parameters', 'overlap')
    except ConfigParser.NoOptionError:
        overlap = False

    # Injection: Default = False
    try:
        injection   = extract_para.getboolean('parameters', 'injection')
    except ConfigParser.NoOptionError:
        injection   = False

    # Draw Maps: Default = True
    try:
        dr_maps     = extract_para.getboolean('parameters', 'draw_maps')
    except ConfigParser.NoOptionError:
        dr_maps     = True

    # Draw all narrow band maps: Default = False
    try:
        dr_all_nband= extract_para.getboolean('parameters',
                                              'draw_all_narrowband_maps')
    except ConfigParser.NoOptionError:
        dr_all_nband= False

    # Draw narrow band maps input: Default = 70.3 170 270 470
    try:
        dr_nband    = extract_para.get('parameters', 'draw_narrowband_maps')
    except ConfigParser.NoOptionError:
        dr_nband    = [70.3, 170, 270, 470]

    parameter_list  = [nside,ifo1, ifo2,f_lower,f_higher,frame_loc,output_loc,
                       overlap, injection,dr_maps, dr_all_nband,dr_nband]
    print ("#---- Input parameters are valid for the analysis ")
    return parameter_list
