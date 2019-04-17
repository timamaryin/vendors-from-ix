# Device vendor statistics from internet exchange

## Description
The idea of this script is to display router/device vendor statistics from an Internet exchange.
This is done by connecting to a (Juniper) device and pulling MAC data or analyzing a file with MAC data.

In order to determine vendor to MAC relationship [public registry](https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries) is used.
For simplicity oui.csv from that web-site is provided as part of this repository.


## Requirements
If the filename is provided to the script as a parameter than text file is assumed with one MAC address per line in "show arp" style:

aa:bb:bb:11:22:33 10.20.30.40      hostname    xe-1/1/0


In order to connect to a Juniper router netconf/ssh is used with PyEZ library
It should be installed, more info [here](https://github.com/Juniper/py-junos-eznc)

oui.csv file mentioned in the description should be there in the same directory with script



## Usage


./mac.py (device | filename) user interface


script takes at least one parameter assuming it is either filename or device.
Other two parameters are optional.

First script tries to open a file if that fails connects to device assuming hostname is provided.
If user is not specified then current unix user is used to connect to a device


