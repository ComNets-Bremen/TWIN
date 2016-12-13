#!/bin/bash

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


## give executable rights to this script:
## 	chmod +x createSession

## This script creates a tmux detached session
## which triggers all important scripts regarding
## TWIN

LOGFILE='/home/pi/logFiles/session.log'

date >> $LOGFILE

## Highly preferred to use complete path to binaries here..

## Step 1: create a Detached Session

/usr/bin/tmux new-session -d -s TWIN

## Step 2: If any/all scripts fail keep the windows freezed
## To know what caused the failure.
## This is a Life Saver..

/usr/bin/tmux set-option -t TWIN set-remain-on-exit on

## Step 3: create Windows for each script..

## create a window called 'bucket' for TWIN python module
## sleep 10 is really import or else script will fail

/usr/bin/tmux new-window -d -n 'bucket' -t TWIN:1 'sleep 10; python3 /home/pi/TWIN/TWIN.py'

## create a window called 'incoming' for Checker scripts
## figlet is optional but a fancy tool

/usr/bin/tmux new-window -d -n 'incoming' -t TWIN:2 'cd /home/pi/incoming; figlet incoming; /home/pi/incoming/incomingChecker.sh'

## create a window called 'bsl' for bootstrap loader Checker Scripts

/usr/bin/tmux new-window -d -n 'bsl' -t TWIN:3 'cd /home/pi/bsl; figlet bootStrapLoader; /home/pi/bsl/bslChecker.sh'

## create a window called 'GPIOaccess' for HTTP Server

/usr/bin/tmux new-window -d -n 'GPIOaccess' -t TWIN:4 'sudo python /home/pi/TWIN/gpioAccess/gpioAPI.py'

exit 0