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
## 	chmod +x bslChecker

## This script uploads the incoming (updated)
## Intel Hex Files (.ihex) to the Zolertia Z1

THISDIR=$(pwd)	# Target the current dir. Here, `~/bsl`

LOGFILE='/home/pi/logFiles/bsl.log'	# Log File for crashes or checks

PORT='/dev/ttyUSB0' # considering only one Z1 connected to USB port


## using BSL cmdline of Z1

burnCode(){
	
	echo "------ ERASING MOTE ------"
	./z1-bsl-nopic --z1 -c $PORT -e && sleep 2
	
	echo "------ PROGRAM MOTE ------"
	./z1-bsl-nopic --z1 -c $PORT -I -p $NEWFILE && sleep 2

	echo "------ RESET MOTE ------"
	./z1-bsl-nopic --z1 -c $PORT -r

	(echo $(date) " Program Uploaded on Z1") >> $LOGFILE
}

(echo "Logging For: " $THISDIR) >> $LOGFILE

## Inotify-Tools usage

inotifywait -m -r -e create --format '%f' $THISDIR | while read NEWFILE

do
		if [ ${NEWFILE: -5} = ".ihex" ] 	# check for suffix..

		  then
		  		(echo $(date)" Update File: " $NEWFILE) >> $LOGFILE

		  		# Upload file on the Z1
		  		burnCode

		else

				: # do nothing
		fi
done