#! /usr/bin/env python3
# Python3 transform OpenArch in RDF

import requests
import rdflib
import csv

def transformRDF(filename, query):

    CSVfilename = filename + ".csv"
    TTLfilename = "transformed/" + filename + ".ttl"

    total = rdflib.Graph()

    with open(CSVfilename, newline='') as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            uri = row['URL'].strip()
            identifier = uri.replace("https://www.openarch.nl/","")
            print(identifier) # progress indicator/debugging
            infile = "harvested/" + identifier + ".ttl"
            gin  = rdflib.Graph()
            gin.load(infile, format="ttl")

            outfile = "transformed/" + identifier + ".ttl"
            gout = rdflib.Graph()
            gout = gin.query(query)
            gout.serialize(destination = outfile, format="ttl")

            gout2 = rdflib.Graph()
            gout2.load(outfile, format="ttl")

            total = total + gout2

    total.serialize(destination = TTLfilename, format="ttl")


## Huwelijksakte
marQuery = """
PREFIX civ: <https://iisg.amsterdam/id/civ/>
PREFIX schema: <http://schema.org/>
PREFIX a2a: <https://www.openarch.nl/def/a2a#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

CONSTRUCT {
    ?persoon a schema:Person ;
        rdfs:label ?fullname ;
        civ:personID ?persid ;
        schema:familyName ?familyname ;
        schema:givenName ?givenname .

    ?event a civ:Marriage ;
        rdfs:label ?desc ;
        civ:registrationID ?regid ;
        civ:eventDate ?date ;
        civ:bride ?bride ;
        civ:groom ?groom ;
        civ:motherBride ?motherBride ;
        civ:fatherBride ?fatherBride ;
        civ:motherGroom ?motherGroom ;
        civ:fatherGroom ?fatherGroom .

        ?bride schema:gender schema:Female .
        ?groom schema:gender schema:Male .
        ?motherBride schema:gender schema:Female .
        ?fatherBride schema:gender schema:Male .
        ?motherGroom schema:gender schema:Female .
        ?fatherGroom schema:gender schema:Male .

}
WHERE  {
    ?persoon a a2a:Person ;
        rdfs:label ?fullname ;
        a2a:PersonName/a2a:PersonNameFirstName ?givenname ;
        a2a:PersonName/a2a:PersonNameLastName ?familyname .

    ?akte a2a:hasEvent ?event ;
        rdfs:label ?desc .

    ?event a2a:EventType "Huwelijk" ;
        a2a:EventDate/rdfs:label ?date .

    ?rel1 a2a:EventKeyRef ?event ;
        a2a:PersonKeyRef ?bride ;
        a2a:RelationType "Bruid" .

    ?rel2 a2a:EventKeyRef ?event ;
        a2a:PersonKeyRef ?groom ;
        a2a:RelationType "Bruidegom" .

    ?rel3 a2a:EventKeyRef ?event ;
        a2a:PersonKeyRef ?motherBride ;
        a2a:RelationType "Moeder van de bruid" .

    OPTIONAL { 
        ?rel4 a2a:EventKeyRef ?event ;
            a2a:PersonKeyRef ?fatherBride ;
            a2a:RelationType "Vader van de bruid" .
        }

    ?rel5 a2a:EventKeyRef ?event ;
        a2a:PersonKeyRef ?motherGroom ;
        a2a:RelationType "Moeder van de bruidegom" .

    OPTIONAL { 
        ?rel6 a2a:EventKeyRef ?event ;
            a2a:PersonKeyRef ?fatherGroom ;
            a2a:RelationType "Vader van de bruidegom" .
        }

    BIND(REPLACE(str(?persoon), "https://www.openarch.nl/id/", "", "i") AS ?persid) .
    BIND(REPLACE(str(?event), "https://www.openarch.nl/id/", "", "i") AS ?regid) .

}
"""

birQuery = """
PREFIX civ: <https://iisg.amsterdam/id/civ/>
PREFIX schema: <http://schema.org/>
PREFIX a2a: <https://www.openarch.nl/def/a2a#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

CONSTRUCT {
    ?persoon a schema:Person ;
        rdfs:label ?fullname ;
        civ:personID ?persid ;
        schema:familyName ?familyname ;
        schema:givenName ?givenname .

    ?event a civ:Birth ;
        rdfs:label ?desc ;
        civ:registrationID ?regid ;
        civ:eventDate ?date ;
        civ:mother ?mother ;
        civ:father ?father ;
        civ:newborn ?child .

        ?mother schema:gender schema:Female .
        ?father schema:gender schema:Male .

}
WHERE  {
    ?persoon a a2a:Person ;
        rdfs:label ?fullname ;
        a2a:PersonName/a2a:PersonNameFirstName ?givenname ;
        a2a:PersonName/a2a:PersonNameLastName ?familyname .

    ?akte a2a:hasEvent ?event ;
        rdfs:label ?desc .

    ?event a2a:EventType "Geboorte" ;
        a2a:EventDate/rdfs:label ?date .

    ?rel1 a2a:EventKeyRef ?event ;
        a2a:PersonKeyRef ?mother ;
        a2a:RelationType "Moeder" .

    OPTIONAL { 
        ?rel2 a2a:EventKeyRef ?event ;
            a2a:PersonKeyRef ?father ;
            a2a:RelationType "Vader" .
        }

    ?rel3 a2a:EventKeyRef ?event ;
        a2a:PersonKeyRef ?child ;
        a2a:RelationType "Kind" .

    BIND(REPLACE(str(?persoon), "https://www.openarch.nl/id/", "", "i") AS ?persid) .
    BIND(REPLACE(str(?event), "https://www.openarch.nl/id/", "", "i") AS ?regid) .

}
"""

dthQuery = """
PREFIX civ: <https://iisg.amsterdam/id/civ/>
PREFIX schema: <http://schema.org/>
PREFIX a2a: <https://www.openarch.nl/def/a2a#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 

CONSTRUCT {
    ?persoon a schema:Person ;
        rdfs:label ?fullname ;
        civ:personID ?persid ;
        schema:familyName ?familyname ;
        schema:givenName ?givenname .

    ?event a civ:Death ;
        rdfs:label ?desc ;
        civ:registrationID ?regid ;
        civ:eventDate ?date ;
        civ:mother ?mother ;
        civ:father ?father ;
        civ:deceased ?deceased ;
        civ:partner ?partner .

        ?mother schema:gender schema:Female .
        ?father schema:gender schema:Male .

}
WHERE  {
    ?persoon a a2a:Person ;
        rdfs:label ?fullname ;
        a2a:PersonName/a2a:PersonNameFirstName ?givenname ;
        a2a:PersonName/a2a:PersonNameLastName ?familyname .

    ?akte a2a:hasEvent ?event ;
        rdfs:label ?desc .

    ?event a2a:EventType "Overlijden" ;
        a2a:EventDate/rdfs:label ?date .

    OPTIONAL { 
        ?rel1 a2a:EventKeyRef ?event ;
            a2a:PersonKeyRef ?mother ;
            a2a:RelationType "Moeder" .
        }

    OPTIONAL { 
        ?rel2 a2a:EventKeyRef ?event ;
            a2a:PersonKeyRef ?father ;
            a2a:RelationType "Vader" .
        }

    ?rel3 a2a:EventKeyRef ?event ;
        a2a:PersonKeyRef ?deceased ;
        a2a:RelationType "Overledene" .

    OPTIONAL { 
        ?rel4 a2a:EventKeyRef ?event ;
            a2a:PersonKeyRef ?partner ;
            a2a:RelationType "Partner" .
        }

    BIND(REPLACE(str(?persoon), "https://www.openarch.nl/id/", "", "i") AS ?persid) .
    BIND(REPLACE(str(?event), "https://www.openarch.nl/id/", "", "i") AS ?regid) .

}
"""


transformRDF("huwelijksaktes", marQuery)
transformRDF("geboorteaktes", birQuery)
transformRDF("overlijdensaktes", dthQuery)







