#! /usr/bin/env python3
# harvestOpenarch.py

import openarchLib
import csv
import rdflib

# read and process every input
def harvestOpenarch(filename):

    CSVfilename = filename + ".csv"
    TTLfilename = filename + ".ttl"

    with open(CSVfilename, newline='') as infile:
        reader = csv.DictReader(infile)

        g_totaal = rdflib.Graph()

        for row in reader:
            url = row['URL'].strip()
            jsonResult = openarchLib.showDoc(url)
            if type(jsonResult) is dict:
                print(jsonResult['error_description'])
            else:
                g_row = openarchLib.createGraph(jsonResult, url)
                g_totaal = g_totaal + g_row

        s = g_totaal.serialize(format='turtle')
        f = open(TTLfilename,"wb")
        f.write(s)
        f.close()

harvestOpenarch("aktes")


