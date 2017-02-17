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

"""
    This Script uses recursive SCP and sends all files in the `~/outgoing/`.
    It uses Python Modules: Paramiko, SCP, Schedule
    Some Part of the Code is Generic, since it will involve IPv6 Link-Local
    Addresses
"""

import schedule
import json
import time
import sys
import logging
from os import path
from paramiko import SSHClient, AutoAddPolicy, util
from scp import SCPClient

# Paramiko Logging
util.log_to_file(path.expanduser("~") + "/logFiles/paramiko.log")

# Logging information
logger = logging.getLogger("SCHEDULER")
logger.setLevel(logging.DEBUG)

# Handler for Logging
handler = logging.FileHandler(path.expanduser("~") + "/logFiles/scheduler.log")
handler.setLevel(logging.DEBUG)

# Formatter for Logging
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Ssh:
    """Creating a SSH, SCP class for sending Files
    """

    def __init__(self, host, username, passwd):
        """Host, Username, Password for SSH, SCP"""
        self.host = host
        self.username = username
        self.passwd = passwd

        self.client = SSHClient()
        self.client.set_missing_host_key_policy(AutoAddPolicy())
        self.client.load_host_keys(path.expanduser("~") + "/.ssh/known_hosts")
        self.client.connect(host, username=self.username,
                            password=self.passwd, look_for_keys=True)

    def send(self):
        """Send File at the given time parameter"""

        scp = SCPClient(self.client.get_transport())

        # Idea: Collect all the retrieval logs in a folder called "outgoing"
        # send the data to the namesake folder to other Pis and keep sending
        # the Folder if new data of other Pis keeps appending.

        scp.put(path.expanduser("~") + "/outgoing/", "outgoing/",
                recursive=True)
        scp.close()


def job(Ip):
    """Jobber for scheduling job @ dedicated time
    """

    # Server is not a Pi so some attributes will vary
    if Ip == "fe80::server:HWadd":
        connector = Ssh(Ip, username="serverUname", passwd="password")
    else:
        connector = Ssh(Ip, username="pi", passwd="pisPassword")
    connector.send()


def main(timeVal):

    timeVal = str(timeVal)  # just some assurance if input is str !

    # No hard coding anymore.. Retreive the sender's address
    # from the JSON file

    with open("/home/pi/routeTable.json") as rtable:
        jData = json.load(rtable)
    IPadd = jData["fountain"]

    schedule.every().day.at(timeVal).do(job, Ip=IPadd)
    logger.debug("Task Scheduled at: %s", str(schedule.next_run()))
    while True:

        schedule.run_pending()
        logger.debug("Next Scheduled Task at: %s", str(schedule.next_run()))
        # Keep logging every 1 minute
        time.sleep(60)


if __name__ == '__main__':

    timeInput = sys.argv[1]
    main(timeInput)
