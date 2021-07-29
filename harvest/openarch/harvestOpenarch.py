#! /usr/bin/env python3
# harvestOpenarch.py

import openarchLib
import csv
import rdflib

# read and process every input
with open('aktes.csv', newline='') as infile:
    reader = csv.DictReader(infile)

    g_totaal = rdflib.Graph()

    for row in reader:
        url = row['akte'].strip()
        jsonResult = openarchLib.showDoc(url)
        g_row = openarchLib.createGraph(jsonResult, url)
        g_totaal = g_totaal + g_row

    s = g_totaal.serialize(format='turtle')
    filename = "aktesdata.ttl"
    f = open(filename,"wb")
    f.write(s)
    f.close()

