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
#==============================================================================#
"""
Setup the pystoch package
"""
from __future__ import print_function

import os
import sys
import subprocess

import io
from shutil import rmtree

from setuptools import (setup, find_packages,
                        __version__ as setuptools_version)

setup_requires = []
install_requires =  setup_requires + ['configparser>= 3.5.0',
                    'matplotlib>= 1.5.1',
                    'numpy>= 1.14.2',
                    'h5py>= 2.7.1',
                    'healpy>= 1.11.0',
                    'six>= 1.12.0',
                    ]                

with open('README.md') as f:
    long_description = f.read()

setup(
    # metadata
    name='pystoch',
    provides=['pystoch'],
    version= '1.0.0',
    description="A Python package for Stochastic Gravitational Wave background",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Anirban Ani, Jishnu Suresh, Sudhagar Suyamprakasam',
    author_email='sudhagar.suyamprakasam@ligo.org',
    license='MIT License',
    url='https://github.com/Sudhagar7/PyStoch',
    packages=['pystoch'],
    install_requires = install_requires,
    include_package_data=True,

    # classifiers
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: Unix',
        'Operating System :: MacOS',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Scientific/Engineering :: Astronomy',
        'Topic :: Scientific/Engineering :: Physics',
    ],

    python_requires='>=3.0',
    py_modules=["six"]
)
