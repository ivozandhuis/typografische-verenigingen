# Building an historical knowledge graph in Linked Data with online tooling
Ivo Zandhuis (@ivozandhuis)
International Institute of Social History

## Introduction
A part of the historical knowledge on a subject consists of concrete references to original archival sources and relevant publications. This part of the historical knowledge results in references in paper and datasets for analysis. The modern way of storing and using this data is in a graph. By using Linked Data principles in this graph data at cultural heritage institutes is linked to the historical research and reproducibility is garanteed.

As a use case I'm building a knowledge graph for research to a Dutch fenomenon called 'typografische verenigingen'. Print labourers organized themselves in these local associations to ensure sickness benefits and organize a yearly feast to celebrate their identity as 'children of Laurens Coster', the Dutch man they believed invented printing. The associations were bounded in a nation wide network and organized the erection of a statue in Coster's honour. Eventually this let to the establishment of the first national union in The Netherlands. I'm interested in how this fenomenon developed through time.

First nodes in the knowledge I aim for are the overview of [sources and literature in Zotero](https://www.zotero.org/groups/2707622/typografische-verenigingen/library) that I am creating. I developed a preliminary Translator for the data in Zotero to RDF. 

In the Zotero-data I refer to individual typographical associations and cultural heritage institutions holding the material. For these I have created csv-files from which I derive nodes in my knowledge graph. To do this I use CoW to convert the csv into RDF. The LDWizard was used to create an easy kick-off for developing a transformation script used in CoW.

Finally, I want to use international data on the places where the assocations were founded. I use the World Historical Gazetteer to link the nodes for typographical associations to the unambiguous nodes for places.

Of course my knowledge graph is not finished after these processes. I could add new sources and in the future I'd like to add data

## References