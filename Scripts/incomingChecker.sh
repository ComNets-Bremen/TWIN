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
##	chmod +x incomingChecker

## This file constantly checks for incoming new .tar file
## in the `~/incoming` folder. 
## This script will trigger the bin/configuration.py script


THISDIR=/home/pi/incoming/	# Target the current dir. here `~/incoming`

LOGFILE=/home/pi/logFiles/incoming.log # Log File for crashes or check


(echo "Logging For: "$THISDIR) >> $LOGFILE

## Inotify-Tools Usage

inotifywait -m -r -e create --format '%f' $THISDIR | while read NEWFILE

do
		if [ ${NEWFILE: -4} = ".tar" ] 	# check for suffix..
		  
		  then
		  		(echo $(date) " Updated File: "$NEWFILE) >> $LOGFILE

		  		## Run the bin/configuration.py with argument $NEWFILE
		  		/home/pi/bin/configuration.py $NEWFILE

		else
				: #do nothing
		fi

done
