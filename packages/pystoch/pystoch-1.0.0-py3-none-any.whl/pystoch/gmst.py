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

PI = 3.141592653589793238462643383279502884


def gpstogmst(gpst):
    """
    Convert Global Positioning System Time (GPST) to Greenwich Median
    Sideral Time (GMST)

    GPS leap second since 1980-01-06

    Add GPS leap second manually

    Last leap second = 1167264017 : Dec 31, 2016	23:59:60	UTC

    The value of pi and 2pi

    PI    = 3.141592653589793238462643383279502884

    TWOPI = 6.283185307179586476925286766559005768

    References
    ----------
    https://oeis.org/

    http://dx.doi.org/10.1103/RevModPhys.84.1527

    http://hpiers.obspm.fr/eop-pc/index.php

    http://www.iausofa.org/index.html

    https://www.andrews.edu/~tzs/timeconv/timeconvert.php

    Parameters
    ----------
    gpst: float
          Global Positioning System Time

    Returns
    -------
    gmst: float
          Greenwich Median Sideral Time
    """
    # list of leap seconds since 1980-01-06
    leapData = [[46828800, +1],[78364801, +1],[109900802, +1],
                [173059203, +1],[252028804, +1],[315187205, +1],
                [346723206, +1],[393984007, +1],[425520008, +1],
                [457056009, +1],[504489610, +1],[551750411, +1],
                [599184012, +1],[820108813, +1],[ 914803214, +1],
                [1025136015, +1],[1119744016, +1],[1167264017, +1]]

    # Limit of validity of leap second data
    leapValid = 1230163218

    if gpst > leapValid:
        print (" Leap Second is not added")

    # Number of leap seconds
    Nleaps = len(leapData)

    # Reference GPS time (2000-01-01 12:00:00 UTC) for GMST conversion
    reference = 630763213

    # Issue warning if outside of valid leap second data
    if gpst > leapValid:
        print('leap seconds unknown')

    # Determine leap second adjustment
    leap_sec = np.zeros(1)
    for ln in range(1, Nleaps):
        if leapData[ln][0] >= reference :
            leap_sec = leap_sec + leapData[ln][1] * (leapData[ln][0] < gpst)
        else: 
            leap_sec = leap_sec - leapData[ln][1] * (leapData[ln][0] >= gpst)

    # Universal time since reference epoch
    seconds = gpst - reference - leap_sec
    days = seconds / 86400.
    centuries = days / 36525.

    # Fractional day since zero hour universal time
    fraction = (days % 1) - 0.5

    # Greenwich mean sidereal time in seconds
    gmst = +2.411054841000e+04 + (8.640184812866e+06 * centuries) + \
           (9.310400000000e-02 * centuries **2) + \
           (-6.200000000000e-06 * centuries **3) + (86400 * fraction)

    # Restrict to [0, 86400) seconds
    gmst = gmst % 86400.

    # Convert to radians
    gmst = 2 * PI * gmst / 86400.
    return float(gmst)


def gmst_omega(gps_gmst):
    """
    Convert Global Positioning System Time (GPST) to Greenwich Median
    Sideral Time (GMST)

    Multiplying with the angular velocity of the Earth

    omegaE   = 7.29211584085121e-05

    Parameters
    ----------
    gps_gmst: float
              Global Positioning System Time

    Returns
    -------
    gmstw: float
           Greenwich Median Sideral Time in radian
    """
    ref_gpst = 630763213
    ref_gmst = gpstogmst(ref_gpst)
    omegaE   = 7.29211584085121e-05

    if gps_gmst == ref_gpst:
        gmstw   = gpstogmst(gps_gmst)
    elif gps_gmst > ref_gpst:
        gmstw   = ref_gmst + (gps_gmst-ref_gpst)*omegaE
    else:
        gmstw   = ref_gmst - (gps_gmst-ref_gpst)*omegaE
    return gmstw