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

"""Global Variables Used Through Out the Module
"""

# Version for Trickle Algorithm
# initial Version value is 0
VERSION = 0

# Instance of Class trickleTimer
tt = None

# Instance of Multicast Socket
mcastSock = None

# Multicast to all ipv6-nodes
# Link-Local IPv6 Address
MCAST_GRP = "ff02::1"

# Multicast Port
# Chosen as Arbitrary value
MCAST_PORT = 30001

# TTL value for Multicasting
MCAST_TTL = 2

# Luby-Transform Block Size
BLOCKSIZE = 1452

# Filename for Encoding
# Default name chosen due to design
FILENAME = "incomingData0.tar"

# Path Variable for the Filename
# Path is for Raspberry Pi
PATH = "/home/pi/incoming"

# Dictionary Cache for a pseudo-route table
# Python List : JSON file for neighboring nodes
rCache = {'fountain': '', 'neighbors': []}
