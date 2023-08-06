# Copyright (C) 2019 IUCAA-GW Group
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
import warnings
warnings.filterwarnings("ignore", "Module (.*) was already import from")
warnings.filterwarnings("ignore", "The oldnumeric module",
                        DeprecationWarning)

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Allow distributors to run custom init code
from . import orf







