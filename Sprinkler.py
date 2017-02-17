#!/usr/bin/python3
# TWIN node - A Flexible Testbed for Wireless Sensor Networks
# Copyright (C) 2016, Communication Networks, University of Bremen, Germany
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; version 3 of the License.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, see <http://www.gnu.org/licenses/>
#
# This file is part of TWIN

"""Main Script to call the Sprinkler Module
"""

__author__ = "Shantanoo Desai"
__copyright__ = "Copyright (C) 2016, Communication Networks,\
    University of Bremen, Germany"
__license__ = "GPL"
__version__ = "3"
__email__ = "sd@comnets.uni-bremen.de"


import sys

from Sprinkler.main import main

if __name__ == '__main__':
    main(sys.argv)
