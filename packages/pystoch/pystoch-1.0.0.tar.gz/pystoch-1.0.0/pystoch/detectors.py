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

import numpy as np
from numpy import sin as SIN
from numpy import cos as COS
from numpy import array as ARRAY

from gmst import *

C_SI  = 299792458e0 # Speed of light in vacuum, m s^-1


def gwdetectors(detector):
    """
    Location and response matrix data for the specified 
    gravitational wave detectors

    References
    ----------
    https://dcc.ligo.org/public/0072/P000006/000/P000006-D.pdf

    https://journals.aps.org/prd/pdf/10.1103/PhysRevD.63.042003

    Parameters
    ----------
    detector: string
              Gravitational wave detector name

              Valid detector name string

              ["GEO","G1","G","LHO","H1","H2","H","LLO","L1","L",

               "VIRGO","V1","V"]

    Returns
    -------
    detector_location: numpy array
                       Detector location data correspond to the speed of 
                       light travel time from the center of the Earth.

    detector_response: numpy array
                       Detector response matrices are dimensionless. 
    """
    # GEO600 detector
    if bool(set([detector]).issubset(set(["GEO","G1","G"]))):
        g_location=np.array([+0.012863270, +0.002223531,+0.016743719],
                            dtype='float64')
        g_response=np.array([-0.096824981272, -0.365782320499, 0.122137293220,
                             -0.365782320499, 0.222968116403, 0.249717414379,
                              0.122137293220, 0.249717414379, -0.126143142581],
                              dtype='float64')
        GEO={'Detector Name':detector,'Response':g_response,
             'Location':g_location}
        return GEO

    # LIGO Hanford 2k and 4km detectors
    if bool(set([detector]).issubset(set(["LHO","H1","H2","H"]))):
        h_location=np.array([-0.007209704, -0.012791166, +0.015345117],
                            dtype='float64')
        h_response=np.array([-0.392614096403, -0.077613413334, -0.247389048338,
                             -0.077613413334, 0.319524079561, 0.227997839451,
                             -0.247389048338, 0.227997839451, 0.073090031743],
                             dtype='float64')
        LHO={'Detector Name':detector,'Response':h_response,
             'Location':h_location}
        return LHO

    # LIGO Livingston 2k detector
    if bool(set([detector]).issubset(set(["LLO","L1","L"]))):
        l_location=np.array([-0.000247758, -0.018333629, +0.010754964],
                            dtype='float64')
        l_response=np.array([0.411280870438, 0.140210270882, 0.247294589877,
                             0.140210270882, -0.109005689621, -0.181615635753,
                             0.247294589877, -0.181615635753, -0.302275151014],
                             dtype='float64')
        LLO={'Detector Name':detector,'Response':l_response,
             'Location':l_location}
        return LLO

    # Virgo detector
    if bool(set([detector]).issubset(set(["VIRGO","V1","V"]))):
        v_location=np.array([+0.015165071, +0.002811912, +0.014605361],
                            dtype='float64')
        v_response=np.array([0.243874043226, -0.099083781242, -0.232576221228,
                             -0.099083781242, -0.447825849056, 0.187833100557,
                             -0.232576221228, 0.187833100557, 0.203951805830],
                             dtype='float64')
        VIRGO={'Detector Name':detector,'Response':v_response,
               'Location':v_location}
        return VIRGO

    else:
        detector_list   = ["GEO","G1","G","LHO","H1","H2","H",
                           "LLO","L1","L","VIRGO","V1","V"]
        print ("      !---- Detector name should be from the list")
        print ("           ",detector_list)
        sys.exit()


def polarization_tensor(phi,theta,psi):
    """
    Polarization Tensors

    Sky positions and polarization angles (radians)

    Spherical coordinates [phi, theta, psi]

    Parameters
    ----------
    phi: float
         Range = [0, 2 pi) 
         The Geocentric longitude in the Earth fixed coordinates 
         with 0 on the prime meridian.

    theta: float
           Range = [0, pi]
           The Geocentric colatitude running from 0 at the 
           North pole to pi at the South pole.

    psi: float
         Range = [0, pi) 
         The polarization psi is the right handed angle about the
         direction of propagation from the negative phi direction to the
         plus polarization direction of the source.

    Returns
    -------
    eplus: numpy array
           Plus Polarization Tensor

    ecross: numpy array
            Cross Polarization Tensor
    """
    m1 = -COS(psi) * SIN(phi) - ( SIN(psi) * COS(phi) * SIN(theta))
    m2 = -COS(psi) * COS(phi) + (SIN(psi) * SIN(phi) * SIN(theta))
    m3 =  SIN(psi) * COS(theta)

    n1 =  SIN(psi) * SIN(phi) - (COS(psi) * COS(phi) * SIN(theta))
    n2 =  SIN(psi) * COS(phi) + (COS(psi) * SIN(phi) * SIN(theta))
    n3 =  COS(psi) * COS(theta)

    mm = ARRAY([m1*m1, m1*m2, m1*m3, m2*m1, m2*m2, m2*m3, m3*m1, m3*m2, m3*m3])
    mn = ARRAY([m1*n1, m1*n2, m1*n3, m2*n1, m2*n2, m2*n3, m3*n1, m3*n2, m3*n3])
    nm = ARRAY([n1*m1, n1*m2, n1*m3, n2*m1, n2*m2, n2*m3, n3*m1, n3*m2, n3*m3])
    nn = ARRAY([n1*n1, n1*n2, n1*n3, n2*n1, n2*n2, n2*n3, n3*n1, n3*n2, n3*n3])
    eplus = mm - nn
    ecross = mn + nm
    return eplus,ecross


def ehat(phi,theta):
    """
    Cartesian source direction

    Parameters
    ----------
    phi: float
         Range = [0, 2 pi)

    theta: float
           Range = [0, pi]

    Returns
    -------
    ehat_src: numpy array
              Source direction
    """
    ehat_x = COS(theta) * COS(phi)
    ehat_y = COS(theta) * -SIN(phi)
    ehat_z = SIN(theta)
    ehat_src= np.array([ehat_x,ehat_y,ehat_z])
    return ehat_src


def antenna_response(detName,gps_time,phi,theta,psi=None):
    """
    Antenna response for given Gravitational wave interferometry detector.

    Parameters
    ----------
    detName: string
             Gravitational wave detector name

              Valid detector name string

              ["GEO","G1","G","LHO","H1","H2","H","LLO","L1","L",

               "VIRGO","V1","V"]

    gps_time: float or int
              Global Positioning System Time.

    phi: float
         Range = [0, 2 pi)
         The right ascension angle (in rad) of the signal.

    theta: float
           Range = [0, pi]
           The declination angle (in rad) of the signal 

    psi: float
         Range = [0, pi) 
         The polarization angle (in rad) of the source.

    Returns
    -------
    fplus: float
           FPlus antenna response for given Gravitational wave detector

    fcross: float
           Fcross antenna response for given Gravitational wave detector
    """
    if psi == None:
        psi         = 0

    gha         = gmst_omega(gps_time) - phi
    dec         = (np.pi/2) - theta
    eplus,ecross= polarization_tensor(gha,dec,psi)
    fplus       = np.dot(eplus , gwdetectors(detName)['Response'])
    fcross      = np.dot(ecross, gwdetectors(detName)['Response'])
    return fplus,fcross


def arrival_time(detName,gps_time,phi,theta):
    """
    Arriaval time of Gravitational wave at detector with respect to given 
    GPS time, right ascension and declination

    Parameters
    ----------
    detName: string
             Gravitational wave detector name

              Valid detector name string

              ["GEO","G1","G","LHO","H1","H2","H","LLO","L1","L",

               "VIRGO","V1","V"]

    gps_time: float or int
              Global Positioning System Time.

    phi: float
         Range = [0, 2 pi)
         The right ascension angle (in rad) of the signal.

    theta: float
           Range = [0, pi]
           The declination angle (in rad) of the signal 

    Returns
    -------
    tarrival: float
              Time of arrival at detector
    """
    ra          = gmst_omega(gps_time) - phi
    dec         = (np.pi/2) - theta
    tarrival = np.dot(ehat(ra,dec),gwdetectors(detName)['Location'])#/C_SI
    return tarrival
