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


# Run this Bootstrap script as root to make the Pi
# setup according to Wiki


TARGET_SITE=www.google.com  # to check internet connectivity
PYTHON_CHECK=/usr/bin/python3   # to check if python3 exists on Jessie
PIP_CHECK=/usr/bin/pip3   # to check if pip3 exists on Jessie

TWIN_HOME=/home/pi/   # Designated Folder
# specific directories for TWIN
DIRECTORIES=(bin bsl incoming logFiles outgoing)

CURRENT_USER=$(who | awk '{print $1}')   # used to change ownership

# log files to be in logFiles
LOG_FILES=(bsl incoming paramiko scheduler session TWIN)

# Determine which Raspberry Pi model using Hardware Revision Value
WHICH_PI=$(cat /proc/cpuinfo | grep "Revision" | awk '{print $3}')

# Check for Pi's Wireless Interface: For Pi - 2 --> External USB Dongle
EXT_WLAN_CHIPSET=$(lsusb | grep "Ralink")  # Only Ralink Chipsets for TWIN

# Check for Pi's Wireless Interface: for Pi - 3 --> Internal Driver
INT_WLAN_CHIPSET=$(lsmod | grep "brcmfmac")  # standard BRCM Based Chipsets


#------------------------------------------------------------------------#
 # Step 0
#------------------------------------------------------------------------#
if [[ $EUID -ne 0 ]]; then
  echo
  echo "TWIN: Step 0: You need root privilege to run this script"
  exit 1
fi

#------------------------------------------------------------------------#
# Step 1
#------------------------------------------------------------------------#
echo
echo "TWIN: Step 1: Checking Internet connectivity"
echo

ping -I eth0 -c 1 -q -W 1 $TARGET_SITE > /dev/null

if [[ "$1" -ne 0 ]]; then
  echo
  echo "Cannot reach target website"
  echo
  echo "Check internet connectivity on Pi"
  exit 1
fi

# Provide User an option to skip the "apt" updates and upgrades
# if the script fails the first time

if [ "$#" = "1" ]; then
  argument_cmd="$1"  # take the argument
else
  argument_cmd="none"
fi

# If the argument along with the script is "skip-apt" then let go
# of these steps

if [ "$argument_cmd" != "skip-apt" ]; then
  #------------------------------------------------------------------------#
  #Step 2
  #------------------------------------------------------------------------#
  echo
  echo "TWIN: Step 2: update and upgrade"
  echo
  # always good to be updates
  apt update && apt upgrade

  #------------------------------------------------------------------------#
  # Step 3
  #------------------------------------------------------------------------#
  echo
  echo "TWIN: Step 3: Installing dependencies and modules for TWIN"
  echo

  # CHECK: For Jessie Lite
  # since Jessie Lite does not have python3 pre-installed
  if [[ -x $PYTHON_CHECK && -x $PIP_CHECK ]]; then
    echo
    echo "TWIN: Step 3.a: python3 and pip3 already installed"
    echo
  else
    #------------------------------------------------------------------------#
    # Step 3.a
    #------------------------------------------------------------------------#
    echo "TWIN: Step 3.a: installing python3 and pip3 on Pi"
	echo
    apt install python3 python3-pip
  fi

  #------------------------------------------------------------------------#
  # Step 3.b
  #------------------------------------------------------------------------#
  echo
  echo "TWIN: Step 3.b: Installing apt dependencies"
  echo
  # python-pip is for installing Flask
  apt install git python-pip figlet libssl-dev \
				libffi-dev inotify-tools tmux

  #------------------------------------------------------------------------#
  # Step 3.c
  #------------------------------------------------------------------------#
  echo
  echo "TWIN: Step 3.c: Installing python pip modules"
  echo
  pip install flask
  pip3 install paramiko scp cryptography schedule lt-code

fi

# If "skip-apt" as argument is mentioned
#------------------------------------------------------------------------#
# Step 4
#------------------------------------------------------------------------#
echo
echo "TWIN: Step 4: Creating directories for TWIN/Sprinkler protocol"
echo

if [[ "$TWIN_HOME" != "$pwd" ]]; then

  cd $TWIN_HOME   # change to /home/pi/ if triggered from cloned Repo

fi


# create the directories in /home/pi/ directory

for directory in ${DIRECTORIES[@]}; do
  mkdir $directory
  # change ownership of directory since this script is run by root
  # change it to pi:pi (generally)
  chown -R $CURRENT_USER:$CURRENT_USER $directory
done

touch routeTable.json  # Route cache JSON file
chown -R $CURRENT_USER:$CURRENT_USER routeTable.json   # change owner

# create empty log files in logFiles directory

for log_file_name in ${LOG_FILES[@]}; do
  touch logFiles/${log_file_name}.log
  chown -R $CURRENT_USER:$CURRENT_USER logFiles/${log_file_name}.log
done

#------------------------------------------------------------------------#
# Step 5
#------------------------------------------------------------------------#
echo
echo "TWIN: Step 5: Moving Scripts in Designated directories"
echo

# necessary scripts into bin/
mv TWIN/Data-Retrieval/*.py $TWIN_HOME/bin
mv TWIN/Scripts/createSession.sh $TWIN_HOME/bin

# necessary scripts into bsl/
mv TWIN/Scripts/bslChecker.sh $TWIN_HOME/bsl
mv TWIN/Scripts/z1-bsl-nopic $TWIN_HOME/bsl

# necessary scripts into incoming/
mv TWIN/Scripts/incomingChecker.sh $TWIN_HOME/incoming
# create a dummy tar file for TWIN framework check
touch $TWIN_HOME/incoming/incomingData0.tar

#------------------------------------------------------------------------#
# Step 6
#------------------------------------------------------------------------#
echo
echo "TWIN: Step 6: Setting cron job for triggering framework on reboot"
echo
# list all the crontabs for pi (not for root)
crontab -l -u pi > twinCron
echo "@reboot /home/pi/bin/createSession.sh" >> twinCron
crontab -u pi twinCron
rm twinCron

#------------------------------------------------------------------------#
# Step 7
#------------------------------------------------------------------------#
echo
echo "TWIN: Step 7: Changing content of rc.local for Ad Hoc Network setup"
echo
echo "Creating a backup for rc.local"
cp /etc/rc.local /etc/rc.local.backup

# Check Which Model of Pi is configured

case "$WHICH_PI" in
  # For Raspberry Pi 2 Model B
  "a01041" | "a21041" | "a22042")
    echo "Raspberry Pi 2 Model B detected.."

	# check for External Chipset
	echo $EXT_WLAN_CHIPSET > /dev/null

	if [ $? == 0 ]; then  # if Chipset exists
      echo "Ralink Chipset Found.."
	  echo "Writing rc.local for Pi-2.."

	  # using here-docs to write to rc.local file
	  cat <<- 'EOF' > /etc/rc.local
	#!/bin/sh -e
	# contents of rc.local for Pi - 2 Model B
    echo "Setting Ad-Hoc Network Parameters"
	ifconfig wlan0 down
	iwconfig wlan0 mode ad-hoc essid pi-adhoc channel 6 txpower 0
	ifconfig wlan0 up

	exit 0
EOF
# here-docs for rc.local ends above
    fi
  ;;

  # For Raspberry Pi 3
  "a02082" | "a22082")
    echo "Raspberry Pi 3 detected.."

	# check for Internal Chipset

	echo $INT_WLAN_CHIPSET > /dev/null

	if [ $? == 0 ]; then  # if Chipset exists
      echo "Internal WLAN Chipset exists.."
	  echo "Writing rc.local for Pi-3.."

	  # using here-docs to write to rc.local file
	  cat <<- 'EOF' > /etc/rc.local
    #!/bin/sh -e
    # contents of rc.local for Pi - 3
    echo "Setting Ad-Hoc Network Parameters"
    iwconfig wlan0 mode ad-hoc essid pi-adhoc channel 6 txpower 0
    exit 0
EOF
# here-docs ends for rc.local above
    fi
  ;;
esac # End switch case
#------------------------------------------------------------------------#
# STEP 8
#------------------------------------------------------------------------#
echo
echo "TWIN: Step 8: Creating a backup & updating the network-interfaces file"
echo

cp /etc/network/interfaces /etc/network/interfaces.backup

cat << EOF > /etc/network/interfaces
# loopback interface
auto lo
iface lo inet loopback

# ethernet eth0
iface eth0 inet manual

# WLAN wlan0 for Ad Hoc network
# TWIN Node
allow-hotplug wlan0
iface wlan0 inet6 auto

EOF

#------------------------------------------------------------------------#
# STEP 9
#------------------------------------------------------------------------#
echo
echo "TWIN: Step 9: Changing content of dhcpcd configuration file"
echo

cp /etc/dhcpcd.conf /etc/dhcpcd.conf.backup

cat << EOF >> /etc/dhcpcd.conf

# Use Stateless Auto Configuration for LL IPv6 Addresses
slaac slaac

# Avoid using Bootstrap Protocol for DHCP discover on wlan0
denyinterfaces wlan0

EOF

# Jessie Lite takes a long time to boot if dhcpcd service is on
# might as well disable it since it is not needed
systemctl disable dhcpcd.service

#------------------------------------------------------------------------#
				#STEP 10
#------------------------------------------------------------------------#
echo
echo "TWIN: Step 10: Disabling IPv6 on eth0"
echo

cat << EOF >> /etc/sysctl.conf
# disable IPv6
net.ipv6.conf.eth0.disable_ipv6=1

EOF

echo "Bootstrap complete...."
echo "Reboot your Pi using: "
echo "sudo reboot"

exit 0
