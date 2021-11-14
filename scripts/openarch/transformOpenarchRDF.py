#! /usr/bin/env python3
# Python3 transform OpenArch in RDF

import requests
import rdflib
import csv

def transformRDF(filename, query):

    CSVfilename = filename + ".csv"

    with open(CSVfilename, newline='') as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            uri = row['URL'].strip()
            identifier = uri.replace("https://www.openarch.nl/","")
            print(identifier) # progress indicator/debugging
            infile = "harvested/" + identifier + ".ttl"
            outfile = "transformed/" + identifier + ".ttl"
            graph = rdflib.Graph()
            graph.load(infile, format="ttl")
            g = graph.query(query)
            g.serialize(destination = outfile, format="ttl")

q = """
PREFIX civ: <https://iisg.amsterdam/id/civ/>
PREFIX schema: <http://schema.org/>
PREFIX a2a: <https://www.openarch.nl/def/a2a#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

CONSTRUCT {
    ?persoon a schema:Person ;
        rdfs:label ?fullname ;
        schema:familyName ?familyname ;
        schema:givenName ?givenname .

    ?huwelijksakte a civ:Marriage ;
        rdfs:label ?huw_desc .
}
WHERE  {
    ?persoon a a2a:Person ;
        rdfs:label ?fullname ;
        a2a:PersonName/a2a:PersonNameFirstName ?givenname ;
        a2a:PersonName/a2a:PersonNameLastName ?familyname .

    ?huwelijksakte a2a:hasEvent/rdfs:label "Huwelijk" ;
        rdfs:label ?huw_desc .

}
"""


transformRDF("aktes", q)







