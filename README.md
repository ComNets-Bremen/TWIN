#TWIN- Managing Data Distribution

Firmware Distribution for the Back-Channel on the __TWIN__ Testbed.

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

### Mechanism

This Library uses two major concepts:

1. [Luby-Transform Codes (*LT-Codes*)](https://en.wikipedia.org/wiki/Luby_transform_code), a rateless encoding scheme for Erasure channels. The concept is used for quick and reliable data dissemination over the 802.11 WLAN Back-Channel

2. [Trickle Algorithm](https://tools.ietf.org/html/rfc6206) which allows the __TWIN Nodes__ within a network to keep checking for Over The Air Updates. This Algorithm also provides a systematic check for any __TWIN Nodes__ which might be lagging behind the current Update.

These two concepts are merged to provide an *efficient and quick dissemination protocol* for firmware on the Back-Channel for __TWIN__

## Further Information

This Project is supported with a detailed [Wiki](https://github.com/ComNets-Bremen/TWIN/wiki).

For further queries please [Contact Us at ComNets, Universität Bremen](https://github.com/ComNets-Bremen/TWIN/wiki/Contact-Details)

## License

This Project is issued under the __GNU GPLv3__ License
