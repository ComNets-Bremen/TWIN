# TWIN / Sprinkler Protocol

Configuration and Firmware Distribution for the Backchannel for the __TWIN Nodes__.

## General Setup for TWIN Nodes

1. Clone the Repository on Raspberry Pi:

    git clone http://github.com/ComNets-Bremen/TWIN.git

2. Change directory:

	cd TWIN/

3. Run the `bootstrap.sh` with root privilege.

	sudo ./bootstrap.sh

See [Wiki](https://github.com/ComNets-Bremen/TWIN/wiki/Setup) for details.

## Usage of Sprinkler Protocol
	
	$ python3 Sprinkler.py -h

	usage: Sprinkler.py [-h] [-V VERSION] [-b BLOCK] [-p PATH] [-f FILENAME]

	Data Dissemination in TWIN Back-Channel using Sprinkler Protocol

	optional arguments:
  	-h, --help            show this help message and exit
  	-V VERSION, --version VERSION
                        	Version Number
  	-b BLOCK, --block BLOCK
                        	Encoding Block Length
  	-p PATH, --path PATH  
  							Target Folder for Filename
  	-f FILENAME, --filename FILENAME
                        	Main File for Fountain


* `VERSION`: Integer value, describing the Version with which the __TWIN Node__ would start.

* `BLOCK`: Block Size for the LT-Encoded Block. The value should be less than __1500 Bytes__ (in order to avoid IPv6 fragmentation)

* `PATH`: this is the Path to the directory where the Firmware File lies or stored.

* `FILENAME`: the firmware file to be disseminated. This file should be a valid `.tar` file

### Default Values
All Default Values are taken from `Sprinkler/global_variables.py`. These values can be overriden according to applications.


## Description

__TWIN Nodes__ have __802.11 WLAN__ based Back-Channel for Uploading *Intel HEX (ihex)* files
for the __Zolertia Z1__ connected to Raspberry Pis via Isolation Boards.

This Library uses the concepts of __Multicasting over WLAN__. Here each __TWIN Node__ is using
*IPv6 Link-Local Addressing Scheme* and is a part of the Multicast Group `ff02::1`.

Firmware for each __TWIN__ consists of the following:

* A configuration file : `config.ini`

* `program1.ihex`

* `program2.ihex`
...so on.

The complete Firmware above is sent as a single `tar` file over the Back-Channel as, for example `data1.tar`.

## Further Information

This Project is supported with a detailed [Wiki](https://github.com/ComNets-Bremen/TWIN/wiki).

For further queries please [Contact Us at ComNets, Universität Bremen](https://github.com/ComNets-Bremen/TWIN/wiki/Contact-Details)

## License

This Project is issued under the __GNU GPLv3__ License