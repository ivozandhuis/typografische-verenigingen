#! /usr/bin/env python3
# Python3 library for operations on openarch.nl using the openarch API
# see: https://api.openarch.nl/

import requests
import json
import rdflib

from rdflib.namespace import XSD

from time import sleep

#######
# searchDoc
# function to find list of events querying on personName, period (before, after) and relationType
def searchDoc(personName, before, after, relationType):

    # API variables
    baseUrl = "https://api.openarch.nl/1.0/records/search.json?"
    lang = "nl"
    numberShow = 25

    # initialize variables for loop
    page = 0
    numberFound = 0
    result = []
    while (numberFound >= (page * numberShow)):
        start = page * numberShow
        reqUrl = baseUrl + \
                "name=" + personName + \
                "+" + str(after) + "-" + str(before) + \
                "&relationtype=" + relationType + \
                "&lang=" + lang + \
                "&number_show=" + str(numberShow) + \
                "&start=" + str(start)

        r = requests.get(reqUrl)
        print(reqUrl) # for debugging
        sleep(0.25) # prevent server overload
        jsonResultList = json.loads(r.text)

        numberFound = int(jsonResultList['response']['number_found'])
        end = numberFound - start
        if end > numberShow:
            end = numberShow

        for i in range(0,end):
            url = jsonResultList['response']['docs'][i]['url']
            result.append(url)

        page = page + 1

    return result


#######
# showDoc
# function to get A2A json
def showDoc(url):

    baseUrl = "https://api.openarch.nl/1.0/records/show.json?"

    # if url is the human-readable landingpage, construct REST-url
    url = url.strip() # remove trailing spaces
    if (url.find("show.php") > 0): 
        reqUrl = url.replace("https://www.openarch.nl/show.php?", baseUrl)
    else:
        pid = url.replace("https://www.openarch.nl/","")
        arch_guid = pid.split(":")
        reqUrl = baseUrl + \
                "archive=" + arch_guid[0] + \
                "&identifier=" + arch_guid[1]

    # error handling
    if (reqUrl != ""):
        # do request
        r = requests.get(reqUrl)
        print(reqUrl) # for debugging and progress
        sleep(0.25) # prevent server overload
        jsonResult = json.loads(r.text)
    else:
        jsonResult = {}
        jsonResult['error_description'] = "empty url"

    # jsonResult should be a list of items
    # if jsonResult is of type 'dict', then jsonResult is an errormessage
    if type(jsonResult) is dict:
        # construct a processable jsonResult, that returns the errormessage as a "gebeurtenis"
        error = jsonResult
        jsonResult = {}
        jsonResult['error_description'] = error

    return jsonResult

# function to create a dict, created from A2A json
def createDict(jsonResult):

    row = {}
    row['url']    = url

    # handle Event-part of the A2A record
    a2aEvent       = jsonResult[0].get('a2a_Event', {})

    # get plaats
    a2aEventPlace  = a2aEvent.get('a2a_EventPlace', {})
    a2aPlace       = a2aEventPlace.get('a2a_Place', {})
    row['plaats']  = a2aPlace.get('a2a_Place', "")

    # get gebeurtenis
    a2aEventType       = a2aEvent.get('a2a_EventType', {})
    row['gebeurtenis'] = a2aEventType.get('a2a_EventType', "")

    # get jaar/maand/dag
    a2aEventDate = a2aEvent.get('a2a_EventDate', {})
    a2aYear      = a2aEventDate.get('a2a_Year', {})
    row['jaar']  = a2aYear.get('a2a_Year', "")
    a2aMonth     = a2aEventDate.get('a2a_Month', {})
    row['maand'] = a2aMonth.get('a2a_Month', "")
    a2aDay       = a2aEventDate.get('a2a_Day', {})
    row['dag']   = a2aDay.get('a2a_Day', "")

    # rollen
    roles = {}
    for r in jsonResult[0]['a2a_RelationEP']:
        keyref = r['a2a_PersonKeyRef']['a2a_PersonKeyRef']
        role   = r['a2a_RelationType']['a2a_RelationType']
        roles[keyref] = role.replace(" ","_")

    # persoonsnamen
    for p in jsonResult[0]['a2a_Person']:

        a2aPersonName = p.get('a2a_PersonName', {})

        keyref = p['pid']
        role = roles[keyref]

        key = "voornaam" + role
        a2aPersonNameFirstName = a2aPersonName.get('a2a_PersonNameFirstName', {})
        row[key] =  a2aPersonNameFirstName.get('a2a_PersonNameFirstName', "")

        key = "tussenvoegsel" + role
        a2aPersonNamePrefixLastName = a2aPersonName.get('a2a_PersonNamePrefixLastName', {})
        row[key] =  a2aPersonNamePrefixLastName.get('a2a_PersonNamePrefixLastName', "")

        key = "achternaam" + role
        a2aPersonNameLastName = a2aPersonName.get('a2a_PersonNameLastName', {})
        row[key] =  a2aPersonNameLastName.get('a2a_PersonNameLastName', "")

    return row

#####
# creates RDF complying to the schema-definition in CLARIAH
def createGraph(jsonResult, url):

    rdf     = rdflib.Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    civ     = rdflib.Namespace("https://iisg.amsterdam/id/civ/")
    schema  = rdflib.Namespace("http://schema.org/")
    sdo     = rdflib.Namespace("https://schema.org/")
    bio     = rdflib.Namespace("http://purl.org/vocab/bio/0.1/")

    g = rdflib.Graph()
    g.namespace_manager.bind('civ', civ, override=False)
    g.namespace_manager.bind('schema', schema, override=False)
    g.namespace_manager.bind('sdo', sdo, override=False)
    g.namespace_manager.bind('bio', bio, override=False)

    akteIRI = rdflib.URIRef(url)

    ### civ:Event ###
    # handle Event-part of the A2A record
    a2aEvent        = jsonResult[0].get('a2a_Event', {})

    # gebeurtenis
    a2aEventType    = a2aEvent.get('a2a_EventType', {})
    gebeurtenis     = a2aEventType.get('a2a_EventType', "")

    eventIRI = rdflib.URIRef(url + "#" + gebeurtenis)

    if (gebeurtenis == "Geboorte"):
        typeIRI = rdflib.URIRef("http://purl.org/vocab/bio/0.1/Birth")
    elif (gebeurtenis == "Overlijden"):
        typeIRI = rdflib.URIRef("http://purl.org/vocab/bio/0.1/Death")
    elif (gebeurtenis == "Huwelijk"):
        typeIRI = rdflib.URIRef("http://purl.org/vocab/bio/0.1/Marriage")
    else:
        typeIRI = rdflib.URIRef("http://schema.org/Event")
    g.add((eventIRI,rdf.type,typeIRI))

    # plaats
    a2aEventPlace  = a2aEvent.get('a2a_EventPlace', {})
    a2aPlace       = a2aEventPlace.get('a2a_Place', {})
    plaats         = a2aPlace.get('a2a_Place', "")

    g.add((eventIRI,civ.eventLocation,rdflib.Literal(plaats)))
    
    # datum
    a2aEventDate = a2aEvent.get('a2a_EventDate', {})
    a2aYear      = a2aEventDate.get('a2a_Year', {})
    jaar         = a2aYear.get('a2a_Year', "")
    a2aMonth     = a2aEventDate.get('a2a_Month', {})
    maand        = a2aMonth.get('a2a_Month', "")
    maand        = str(maand).zfill(2)
    a2aDay       = a2aEventDate.get('a2a_Day', {})
    dag          = a2aDay.get('a2a_Day', "")
    dag          = str(dag).zfill(2)

    datum        = jaar + "-" + maand + "-" + dag

    g.add((eventIRI,civ.eventDate,rdflib.Literal(datum, datatype=XSD.date)))

    ### civ:Person

    # rollen
    roles = {}
    for r in jsonResult[0]['a2a_RelationEP']:
        keyref = r['a2a_PersonKeyRef']['a2a_PersonKeyRef']
        role   = r['a2a_RelationType']['a2a_RelationType']
        roles[keyref] = role.replace(" ","_")

    # persoonsnamen
    for p in jsonResult[0]['a2a_Person']:

        a2aPersonName = p.get('a2a_PersonName', {})
        personPid = p['pid']

        personIRI = rdflib.URIRef(url + "#" + personPid)
        typeIRI = rdflib.URIRef("http://schema.org/Person")
        g.add((personIRI,rdf.type,typeIRI))
        g.add((personIRI,civ.personID,rdflib.Literal(personPid)))

        a2aPersonNameFirstName = a2aPersonName.get('a2a_PersonNameFirstName', {})
        givenName =  a2aPersonNameFirstName.get('a2a_PersonNameFirstName', "")
        g.add((personIRI,sdo.givenName,rdflib.Literal(givenName)))

        a2aPersonNamePrefixLastName = a2aPersonName.get('a2a_PersonNamePrefixLastName', {})
        infix =  a2aPersonNamePrefixLastName.get('a2a_PersonNamePrefixLastName', "")
        if (infix != ""):
            g.add((personIRI,civ.prefixFamilyName,rdflib.Literal(infix)))

        a2aPersonNameLastName = a2aPersonName.get('a2a_PersonNameLastName', {})
        lastName =  a2aPersonNameLastName.get('a2a_PersonNameLastName', "")
        g.add((personIRI, sdo.familyName,rdflib.Literal(lastName)))

        # relating Event to Person with role-properties
        rol = roles[personPid]

        if (rol == "Moeder"):
            roleIRI = rdflib.URIRef("https://iisg.amsterdam/id/civ/mother")
        elif (rol == "Vader"):
            roleIRI = rdflib.URIRef("https://iisg.amsterdam/id/civ/father")
        elif (rol == "Kind"):
            roleIRI = rdflib.URIRef("https://iisg.amsterdam/id/civ/newborn")
        elif (rol == "Partner"):
            roleIRI = rdflib.URIRef("https://iisg.amsterdam/id/civ/partner")
        elif (rol == "Overledene"):
            roleIRI = rdflib.URIRef("https://iisg.amsterdam/id/civ/deceased")
        elif (rol == "Bruid"):
            roleIRI = rdflib.URIRef("https://iisg.amsterdam/id/civ/bride")
        elif (rol == "Bruidegom"):
            roleIRI = rdflib.URIRef("https://iisg.amsterdam/id/civ/groom")
        elif (rol == "Vader_van_de_bruid"):
            roleIRI = rdflib.URIRef("https://iisg.amsterdam/id/civ/fatherBride")
        elif (rol == "Moeder_van_de_bruid"):
            roleIRI = rdflib.URIRef("https://iisg.amsterdam/id/civ/motherBride")
        elif (rol == "Vader_van_de_bruidegom"):
            roleIRI = rdflib.URIRef("https://iisg.amsterdam/id/civ/fatherGroom")
        elif (rol == "Moeder_van_de_bruidegom"):
            roleIRI = rdflib.URIRef("https://iisg.amsterdam/id/civ/motherGroom")
        else:
            roleIRI = rdflib.URIRef("https://iisg.amsterdam/id/civ/participant")

        g.add((eventIRI,roleIRI,personIRI))


    return g
