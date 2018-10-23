#!/usr/bin/env python


from jnpr.junos import Device               # PyEZ to connect to juniper device
from jnpr.junos.exception import *          # Various exceptions
import sys                                  # for command line arguments
import getpass                              # in order to get password without echo
import operator                             # for dict sorting




if len(sys.argv) < 2:
    print "Usage: ", sys.argv[0], " file/device"
    print "Script either opens the file or connects to the device"
    exit(0)



###
###  getting vendor data from the registry file
###  In the decitionarary variable vendor part of mac is used as key
###
vendormacs = {}

try:
    macfile = open("oui.csv" , "r")
except IOError as e:
    print "I/O error while reading {0}: {1}".format("oui.csv", e.strerror)
    exit ("Some issue opening file with vendor mac data, giving up")

# sample:
#MA-L,9C8E99,Hewlett Packard,11445 Compaq Center Drive Houston  US 77070
for line in macfile:
    vendorline = line.split(',')
    if '"' in vendorline[2]:
        subvendorline = line.split('"')
        #print vendorline[1] , subvendorline[1]
        vendormacs[vendorline[1]] = subvendorline[1]
    else:
        #print vendorline[1], vendorline[2]
        vendormacs[vendorline[1]] = vendorline[2]

macfile.close()



### 
### Is there filename provided or hostname? assuming filename first
###
withdevice = False

try:
    macfile = open(sys.argv[1] , "r")
except IOError as e:
    #print "I/O error while reading {0}: {1}".format(sys.argv[1], e.strerror)
    print "Can't open a file ({0}), trying device instead".format(e.strerror)
    withdevice = True




### We need two arrays like variables to store mac data

decimalmacs  = []   ### first one is list of macs in decimal value for sorting purposes
devicemacs   = {}   ### and second one is a dictionary containing hex values where keys are the same as in list above



if withdevice:

    ### current user is used to connect
    password = getpass.getpass("Please enter the password to connect to the device: ")
    router  = Device(host=sys.argv[1], password=password)
    print "Connecting to the device..."

    try:
        router.open(gather_facts = False)
    except ConnectError as error:
        print 'Unable to connect to ' , sys.argv[1] , error
        exit()

    router.timeout=25000

    arps = router.rpc.get_arp_table_information(no_resolve = True)
    for arp in arps.xpath('//arp-table-entry'):
        mac = ((arp[0].text.strip()).replace(":","")).upper()
        macdecimal = int(mac,16)

        if macdecimal in decimalmacs:
            continue
        else:
            decimalmacs.append(macdecimal)
            devicemacs[macdecimal]= {}
            devicemacs[macdecimal]['hexmac'] = mac

    router.close()


else:

######## getting mac data from file
######## assuming colonseparated data : mac,data
######## aa:bb:cc:11:22:33,something

    for line in macfile:
        macline = line.split(',')
        mac     = macline[0].replace(":","")

        macdecimal = int(mac,16)

        if macdecimal in decimalmacs:
            # Don't add dupes
            continue
        else:
            decimalmacs.append(macdecimal)
            devicemacs[macdecimal]= {}
            devicemacs[macdecimal]['hexmac']=mac.upper()


    macfile.close()


print len(decimalmacs) , " unique MACs found"
decimalmacs.sort()
print "removing potential same chassis MACs"



### and try to count vendors
vendorsummary = {}

i = 0;
for j in decimalmacs:

    vendor = devicemacs[j]['hexmac'][:6]
    #print vendor
    if vendor in vendormacs:
        vendor = vendormacs[vendor]
    else:
        vendor = 'Unknown'

    if vendor in vendorsummary:
        vendorsummary[vendor] += 1
    else:
        vendorsummary[vendor] = 1


    #print "macs too close, delta: ", j-i, devicemacs[j]['hexmac'],  vendor

    if (j - i ) < 2048:
        decimalmacs.remove(j)
    else:
        i = j



print len(decimalmacs),  " MACs left now"
print


onepercent = float(len(decimalmacs))/100

sorted_vendors = sorted (vendorsummary.items(), key = operator.itemgetter(1), reverse=True)

for vendor in sorted_vendors:
    percent =  vendor[1]/onepercent
    if percent <= 0.5:
        continue
    print ("{0:40s}  {1:>9d} {2:>8.2f}%").format(vendor[0], vendor[1], percent)

exit()

