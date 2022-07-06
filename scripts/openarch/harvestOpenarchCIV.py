#! /usr/bin/env python3
# Python3 harvest OpenArch in N-triples / CIV ontology

import requests
import csv
import time

def resolveURI(uri, requestformat = "application/n-triples+civ"):

    headers = {"Accept": requestformat }

    try:
        r = requests.get(uri, headers = headers)
    except:
        print("Request error") 

    return r.text


def harvestOpenarch(filename,timestr):

    CSVfilename = filename + ".csv"
    outfile = open('harvested/openarch-'+timestr+'.nt','a')

    with open(CSVfilename, newline='') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            uri = row['URL'].strip()
            identifier = uri.replace("https://www.openarch.nl/","")
            print(identifier) # progress indicator/debugging
            outfile.write(resolveURI(uri))

timestr=time.strftime("%Y%m%d-%H%M%S")
harvestOpenarch("huwelijksaktes",timestr)
harvestOpenarch("overlijdensaktes",timestr)
harvestOpenarch("geboorteaktes",timestr)
print('harvest/openarch-'+timestr+'.nt created')
