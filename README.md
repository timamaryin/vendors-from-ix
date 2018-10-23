# Device/router vendors from internet exchange

The idea of this script is to display router/device vendor statistics from an Internet exchange.
This is done by connecting to the device and pulling MAC data or analyzing a file with MAC data.

In order to determine vendor to MAC relationship public registry is used https://regauth.standards.ieee.org/standards-ra-web/pub/view.html#registries
For simplicity oui.csv from that web-site is provided as part of this repository.


#Usage

Is it assumed that python is installed and available 

./mac.py (device | filename)


script takes one parameter assuming it is either filename or device.
First it tries to open a file if that fails connects to device assuming hostname is provided.


