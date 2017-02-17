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
Routing table Entry function:
add a fountain IPv6 address or Neighbor
IPv6 address to global variable `rCache`
"""

from os import chdir, path
import json
from Sprinkler.global_variables import rCache


def addRoute(foun=None, neigh=None):
    """
    addRoute: Add IPv6 Addresses to a JSON File called `routeTable.json`

    @type foun: string
    @param foun: string as IPv6 LL address determined by hearing a Fountain

    @type neigh: string
    @param neigh: string as IPv6 LL address determined by hearing neighboring
                node Versions

    Description:
        a function to add IPv6 address of either Fountain or
        nearby neighbors and store the content into JSON format
        for future access over REST.
    """

    if foun is None or foun == "":
        # don't add anything if field
        # empty
        pass

    else:
        # if parameter exists
        # update the Dictionary
        rCache['fountain'] = foun

    if neigh is None or neigh == "":
        # don't append entry to list
        # if parameter is empty/None
        pass

    else:
        if neigh in rCache['neighbors']:
            # if the IPv6 address already
            # exists don't append it..
            pass

        else:
            rCache['neighbors'].append(neigh)

    # Save in /home/ folder
    chdir(path.expanduser("~"))

    with open("routeTable.json", 'w+') as rtable:
        json.dump(rCache, rtable)
