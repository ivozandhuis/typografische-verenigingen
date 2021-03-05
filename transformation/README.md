# Creation of the graph from data

## Export Zotero
See zotero-directory

## Transform data using semantics
The data-directory contains a subdirectory 'semantics' defining the semantics of the less-structured data in CSV, XML, TXT or JSON format. The semantics can be used to create the RDF graph based on the data.

### RML
For some data-files I defined a mapping in RML. I kick-started an RML-file with [LDWizard](https://ldwizard.netwerkdigitaalerfgoed.nl/).

To transform the data defined in RML-files, do:
1. Use [RMLMapper](https://github.com/RMLio/rmlmapper-java) in docker
1. copy RML file into the data directory containing the data-file
1. change to this directory
1. run the docker as prescribed

example:
``` sh
sudo docker run --rm -v $(pwd):/data rmlmapper -m leden-jaarboekje1856.rml.ttl > ../graph/leden-jaarboekje1856-2.nt
```
