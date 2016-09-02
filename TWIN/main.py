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

"""main.py for the TWIN module; calling the Bucket
"""

import TWIN.global_variables as gv
import argparse, sys
from TWIN.Socket import Socket
from TWIN.trickle import trickleTimer
from struct import pack, unpack
from TWIN.bucket import bucket
from os import chdir, path
import logging

# Central Logging Entity
logger = logging.getLogger("MAIN")
logger.setLevel(logging.ERROR)

## Handler for Logging
handler = logging.FileHandler(path.expanduser("~")+"/logFiles/TWIN.log")
handler.setLevel(logging.ERROR)

# Format for Logging
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def main(args):
    parser = argparse.ArgumentParser(description="Data Dissemination in TWIN Back-Channel")

    parser.add_argument("-V", "--version", type=int, default=gv.VERSION, help="Version Number")

    parser.add_argument("-b", "--block", type=int, default=gv.BLOCKSIZE, help="Encoding Block Length")
    
    parser.add_argument("-p", "--path", type=str, default=gv.PATH, help="Target Folder for Filename")

    parser.add_argument("-f", "--filename", type=str, default=gv.FILENAME, help="Main File for Fountain")


    args = parser.parse_args()

    gv.VERSION = args.version

    gv.BLOCKSIZE = args.block

    gv.FILENAME = args.filename

    gv.PATH = args.path

    if not path.isdir(gv.PATH):
        print("Path Does not Exist")
        sys.exit(1)
    else:
        chdir(gv.PATH)
        if not path.exists(gv.FILENAME):
            print("File Does not Exist")
            sys.exit(1)

    logger.debug("Starting with Version %d"%gv.VERSION)

    logger.info("Creating Socket..")

    gv.mcastSock = Socket()

    logger.info("Binding Socket..")
    gv.mcastSock.bindSock()

    logger.info("Configuring Trickle Timer")

    initArgs = {'message':pack('!H', gv.VERSION),
    'host':gv.MCAST_GRP,
    'port':gv.MCAST_PORT
    }

    gv.tt = trickleTimer(gv.mcastSock.send,initArgs)
    gv.tt.start()

    while True:
        bucket()