#! /usr/bin/env python3
# Python3 transform OpenArch in RDF

# TBD:
# * change persID into an integer
# * replace characters

import requests
import rdflib
import csv

# -----
def getIDgraph(graph, idStarter):

    # initialize resultgraph
    gres  = rdflib.Graph()

    # get Persons to add an id to
    select = """
        PREFIX schema: <http://schema.org/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 

        SELECT * WHERE  { ?ding a schema:Person ; }
        """
    result = graph.query(select)

    # add ids
    id = idStarter
    for row in result:
        id = id + 1
        s = rdflib.URIRef(row.ding)
        p = rdflib.URIRef("https://iisg.amsterdam/id/civ/persID")
        gres.add((s, p, rdflib.Literal(id)))

    # get Marriages to add an id to
    select = """
        PREFIX schema: <http://schema.org/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
        PREFIX civ: <https://iisg.amsterdam/id/civ/>
        SELECT * WHERE  { ?ding a civ:Marriage ; }
        """
    result = graph.query(select)

    # add ids
    id = round (idStarter + (idStarter/10))
    for row in result:
        id = id + 1
        s = rdflib.URIRef(row.ding)
        p = rdflib.URIRef("https://iisg.amsterdam/id/civ/registrationID")
        gres.add((s, p, rdflib.Literal(id)))

    # get Births to add an id to
    select = """
        PREFIX schema: <http://schema.org/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
        PREFIX civ: <https://iisg.amsterdam/id/civ/>
        SELECT * WHERE  { ?ding a civ:Birth ; }
        """
    result = graph.query(select)

    # add ids
    id = round (idStarter + (idStarter/10))
    for row in result:
        id = id + 1
        s = rdflib.URIRef(row.ding)
        p = rdflib.URIRef("https://iisg.amsterdam/id/civ/registrationID")
        gres.add((s, p, rdflib.Literal(id)))

    # get Deaths to add an id to
    select = """
        PREFIX schema: <http://schema.org/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
        PREFIX civ: <https://iisg.amsterdam/id/civ/>
        SELECT * WHERE  { ?ding a civ:Death ; }
        """
    result = graph.query(select)

    # add ids
    id = round (idStarter + (idStarter/10))
    for row in result:
        id = id + 1
        s = rdflib.URIRef(row.ding)
        p = rdflib.URIRef("https://iisg.amsterdam/id/civ/registrationID")
        gres.add((s, p, rdflib.Literal(id)))

    return gres

# -----
def transformRDF(filename, query, id):

    CSVfilename = filename + ".csv"
    total = rdflib.Graph()

    with open(CSVfilename, newline='') as infile:
        reader = csv.DictReader(infile)

        for row in reader:
            uri = row['URL'].strip()
            identifier = uri.replace("https://www.openarch.nl/","")
            print(identifier) # progress indicator/debugging

            # read data
            gin  = rdflib.Graph()
            infile = "harvested/" + identifier + ".ttl"
            gin.load(infile, format="ttl")

            # transform data
            gout = rdflib.Graph()
            gout = gin.query(query)

            # write output
            outfile = "transformed/" + identifier + ".ttl"
            gout.serialize(destination = outfile, format="ttl")
            gout2 = rdflib.Graph()
            gout2.load(outfile, format="ttl")

            total = total + gout2

    # add personId integers
    gID = getIDgraph(total, id)
    total = total + gID

    TTLfilename = "transformed/" + filename + ".ttl"
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
        schema:familyName ?familyname ;
        schema:givenName ?givenname .

    ?event a civ:Marriage ;
        rdfs:label ?desc ;
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
        schema:familyName ?familyname ;
        schema:givenName ?givenname .

    ?event a civ:Birth ;
        rdfs:label ?desc ;
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
        schema:familyName ?familyname ;
        schema:givenName ?givenname .

    ?event a civ:Death ;
        rdfs:label ?desc ;
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
}
"""

transformRDF("geboorteaktes", birQuery, 10000)
transformRDF("huwelijksaktes", marQuery, 20000)
transformRDF("overlijdensaktes", dthQuery, 30000)
