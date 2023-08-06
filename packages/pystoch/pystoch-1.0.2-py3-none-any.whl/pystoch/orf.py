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
import time
import os
import sys
from pystoch_parameter import*
from pystochmap import*
from tdelay_response import*
"""
PyStoch: A Python based code for Stochastic Gravitational Wave Background 
mapping from LIGO data
"""


def orf_parameterfile(read_file):
    """
    Pystoch Analysis from the parameter file

    References
    ----------
    'Very fast stochastic gravitational wave background map
    making using folded data'

    https://journals.aps.org/prd/abstract/10.1103/PhysRevD.98.024001

    https://arxiv.org/abs/1803.08285v2

    Acknowledgmets: IUCAA, Pune and Navajbai Ratan Tata Trust (NRTT).

    Parameters
    ----------
    read_file:  .ini file
                 Full path to input .ini file

    Returns
    -------
    None
    """
    print("#-----------------------------------------------------------------#")
    localtime_start = time.asctime( time.localtime(time.time()) )
    print("#---- Pystoch map analysis started at : ",localtime_start)

    # Parameter file not exist
    if not os.path.isfile(read_file):
        print ("!---- Input file not exist or incorrect path")
        sys.exit()
    else:
        # Validate the parameters in the file
        ip_par = parameter_file(read_file)
        gpstime_info,freInfo,csd,sigma_sqinv = read_hdf(ip_par[5])

        # GPS Time Array from input GPS Start,End and Delta Time
        gpstime_Array = np.arange(gpstime_info[0],gpstime_info[1],
                                  int(gpstime_info[2]))

        # Theta and Phi from the HealPix nside
        pixtheta,pixphi = nside_pix2ang(ip_par[0]) # Nside
        
        # Combined Antenna Response and Time Delay
        response,tdelay = combined_antenna_response(ip_par[1],
                                                    ip_par[2],gpstime_Array,
                                                    pixtheta,pixphi)

        # Dirty map matrix
        map_hdf = dirty_map_matrix(response,tdelay,freInfo,
                                   csd,sigma_sqinv,gpstime_info[2],ip_par[0],
                                   ip_par[3],ip_par[4],ip_par[9],ip_par[6])

        # Save map
        map_plot = plot_pystochmap(ip_par[0],map_hdf,ip_par[9],ip_par[10])

        localtime_end = time.asctime( time.localtime(time.time()) )
        print ("#---- Pystoch map analysis ended at : ",localtime_end)
        return
