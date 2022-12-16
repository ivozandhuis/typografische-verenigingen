#! /usr/bin/env python3

import requests
import rdflib
import csv

#ifileName = "../data/zotero-export.rdf.xml"
#ofileName = "intermediate/zotero-export.nt"

ifileName = "../data/tropy-export.json"
ofileName = "intermediate/tropy-export.ttl"

g = rdflib.Graph()
g.parse(ifileName, format="json-ld")
g.serialize(destination=ofileName, format="ttl", encoding='utf-8')
