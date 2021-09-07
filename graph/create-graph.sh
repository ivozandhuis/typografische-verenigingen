#!/bin/bash

# Zotero
# Reserialize the Zotero export in RDF/XML into ntriples
rapper -o ntriples ../data/zotero-export.rdf.xml > intermediate/zotero-export.nt
rapper -o turtle ../data/zotero-export.rdf.xml > intermediate/zotero-export.ttl

# Tropy
# Reserialize the Tropy export in JSONLD into ntriples via nquads
jsonld normalize ../data/tropy-export.json > intermediate/tropy-export.nq
rapper -i nquads -o ntriples intermediate/tropy-export.nq > intermediate/tropy-export.nt
# todo: in the nt-file (1) replace blank nodes with my own (2) add representation property

# Recogito
# todo: 

# OpenArch and BurgerLinker

# CSV files
# todo: Transform the csv-files with cow


