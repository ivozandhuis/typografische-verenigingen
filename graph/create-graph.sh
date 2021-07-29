#!/bin/bash

rapper -o ntriples ../data/zotero-export.rdf.xml > intermediate/zotero-export.nt

jsonld normalize ../data/tropy-export.json > intermediate/tropy-export.nq
rapper -i nquads -o ntriples intermediate/tropy-export.nq > intermediate/tropy-export.nt

