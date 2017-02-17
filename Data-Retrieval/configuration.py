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

# give executable rights to this script:
#  chmod +x configuration.py

"""
This is an automated script.
It takes help of "inotify-tools" which keeps
checking for any changes in the folder for any '.tar' files
"""


import tarfile
import sys
import logging
import subprocess

from configparser import ConfigParser
from os import path, uname, remove
import RPi.GPIO as gpio

parser = ConfigParser()

# GPIO Settings
gpio.setmode(gpio.BCM)

GPINS = [20, 21]  # According to BCM Layout


for pin in GPINS:
    gpio.setup(pin. gpio.OUT)  # set as OUTPUT

# Logging information
logger = logging.getLogger("INCOMING")
logger.setLevel(logging.DEBUG)

# Handler for Logging
handler = logging.FileHandler(path.expanduser("~") + "/logFiles/incoming.log")
handler.setLevel(logging.DEBUG)

# Formatter for Logging
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def Configuration():
    """Extract File, Read the Config file,
    send the file to designated folder,
    in the end remove the cfg file from folder
    """

    # 1. Open the tar file and check for config.ini file
    with tarfile.open(FILENAME, 'r') as t:
        contents = t.getnames()

        for fName in contents:
            if(fName == 'config.ini'):

                # if file found extract it here!
                t.extract(fName, path='.')

    # 2. parse through the cfg file and get the value
    # configured for this machine
    parser.read(['config.ini'])
    try:

        fileValue = parser.get(uname()[1], 'file')
        logger.debug("file for this Pi: %s" % fileValue)
        timeValue = parser.get(uname()[1], 'time')

        # use 'DATA' for data access and 'POWER' for supply

        if 'DATA' in parser[uname()[1]]:
            dataValue = int(parser.get(uname()[1], 'DATA'))
            logger.debug("DATA pin 20:%d" % dataValue)
            gpio.output(20, dataValue)

        if 'POWER' in parser[uname()[1]]:
            powerValue = int(parser.get(uname()[1], 'POWER'))
            logger.debug("POWER pin 21:%d" % powerValue)
            gpio.output(21, powerValue)

    except:
        logger.exception("No File for this Node..")

    # 3. Open the tar file and extract the file to a
    # Destination (DEST) folder
    with tarfile.open(FILENAME, 'r') as t:
        contents = t.getnames()

        for name in contents:
            if(fileValue == name):
                t.extract(fileValue, path=DEST)

    # Work Done. Clean Up
    logger.info("file extracted")
    logger.info("removing the config file")
    remove('config.ini')

    # Schedule the File Transfer
    sched_cmd = 'python3 scheduleSend.py %s &' % str(timeValue)
    pr = subprocess.Popen(sched_cmd, shell=True)
    logger.info("Scheduler Triggered with PID %d" % pr.pid)


if __name__ == '__main__':

    # This is the BootStrapLoader Folder where the IHex File
    # Needs to be sent.
    DEST = path.expanduser("~") + "/bsl/"

    FILENAME = str(sys.argv[1])

    if not tarfile.is_tarfile(FILENAME):

        logger.error("ERROR: File is not a .tar")
        sys.exit(1)

    Configuration()
