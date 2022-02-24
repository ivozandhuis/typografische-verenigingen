#! /usr/bin/env python3
# Python3 harvest OpenArch in RDF

import requests
import rdflib
import csv

def resolveURI(uri, requestformat = "text/turtle"):

    headers = {"Accept": requestformat }
    g = rdflib.Graph()

    try:
        r = requests.get(uri, headers = headers)
    except:
        print("Request error") 

    try:
        g.parse(data = r.text, format = "ttl")
    except:
        print("Turtle parse error") 

    return g


def harvestOpenarch(filename):

    CSVfilename = filename + ".csv"

    with open(CSVfilename, newline='') as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            uri = row['URL'].strip()
            identifier = uri.replace("https://www.openarch.nl/","")
            print(identifier) # progress indicator/debugging
            outfile = "harvested/" + identifier + ".ttl"
            g = resolveURI(uri)
            g.serialize(destination = outfile, format="ttl")

harvestOpenarch("aktes")

