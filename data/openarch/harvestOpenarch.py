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

# harvestOpenarch('openarch.nl-2021-08-25-%drukker_1800-1940-bs_geboorte')
harvestOpenarch("openarch.nl-2021-08-25-%drukker_1800-1940-bs_huwelijk")
# harvestOpenarch("openarch.nl-2021-08-25-%drukker_1800-1940-bs_overlijden")

# harvestOpenarch('openarch.nl-2021-08-25-%boekbinder_1800-1940-bs_geboorte')
harvestOpenarch('openarch.nl-2021-08-25-%boekbinder_1800-1940-bs_huwelijk')
# harvestOpenarch('openarch.nl-2021-08-25-%boekbinder_1800-1940-bs_overlijden')

# harvestOpenarch('openarch.nl-2021-08-25-%letterzetter_1800-1940-bs_geboorte')
harvestOpenarch('openarch.nl-2021-08-25-%letterzetter_1800-1940-bs_huwelijk-bruidegom')
# harvestOpenarch('openarch.nl-2021-08-25-%letterzetter_1800-1940-bs_huwelijk-getuige')
# harvestOpenarch('openarch.nl-2021-08-25-%letterzetter_1800-1940-bs_huwelijk-vader_van_de_bruid')
# harvestOpenarch('openarch.nl-2021-08-25-%letterzetter_1800-1940-bs_huwelijk-vader_van_de_bruidegom')
# harvestOpenarch('openarch.nl-2021-08-25-%letterzetter_1800-1940-bs_overlijden')

# harvestOpenarch('openarch.nl-2021-08-25-%boekdrukker_1800-1940-bs_geboorte')
harvestOpenarch('openarch.nl-2021-08-25-%boekdrukker_1800-1940-bs_huwelijk')
# harvestOpenarch('openarch.nl-2021-08-25-%boekdrukker_1800-1940-bs_overlijden')


