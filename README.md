# Building an historical knowledge graph in Linked Data with online tooling
Ivo Zandhuis (@ivozandhuis)
International Institute of Social History

## Introduction
The original archival sources, digital processible data and relevant literature refered to in publications can be considered the 'explicit knowledge' used to create new historical insights [Polanyi1966]. The representation of this knowledge is currently done using graph based data structures. The most prominent way of storing these graph based data structures is called the Resource Description Framework (RDF) [ref]. The data created by means of RDF is called a knowledge graph based on Linked Data.

Now why is it important to investigate the principles of Linked Data for storing and disseminating explicit historical knowledge? Those are two questions: why is it important to create explicit historical knowledge in the first place and than why should we use RDF to do so? Representing historical explicit knowledge in a computersystem makes this knowledge 'processible' and thereby enables reproducibility. Historians in the future can retrieve sources efficiently and re-evaluate analysis and interpretation.

Using Linked Data principles to store, link and provide explicit historical knowledge, the data and the metadata provided by cultural heritage institutes is linked directly to the historical research. Dutch government stimulates cultural heritage institutions to use Linked Data for providing their metadata, which means the knowledge graph can be related to this metadata directly [nationale stategie].

As a use case I'm building a knowledge graph for research to a Dutch fenomenon called 'typografische verenigingen'. During the first half of the 19th century print labourers in The Netherlands organized themselves in these local associations. These associations were founded to ensure sickness benefits and organize a yearly feast to celebrate their identity as 'children of Laurens Coster', the Dutch man they believed invented printing. They were connected in a nation wide network and organized the erection of a statue in Coster's honour. Eventually this let to the establishment of the first national union in The Netherlands in 1866. I'm interested in how this fenomenon developed through time, until its cancellation in the 20th century.

First nodes in the knowledge graph I aim for are the overview of [sources and literature in Zotero](https://www.zotero.org/groups/2707622/typografische-verenigingen/library) that I am creating. I developed a preliminary translator for the data in Zotero to RDF. 

In the Zotero-data I refer to individual typographical associations and cultural heritage institutions holding the material. For these entities I have created csv-files from which I derive nodes in my knowledge graph. To do this I use CoW to convert the csv into RDF. The [LDWizard](https://ldwizard.netwerkdigitaalerfgoed.nl/) can be used to create an easy kick-off for developing a transformation script used in CoW.

Finally, I want to use international data on the places where the assocations were founded. I intend to use the World Historical Gazetteer to link the nodes for typographical associations to the unambiguous nodes for places.

Of course my knowledge graph is not finished after these processes. I could add new sources and in the future I'd like to add 'datafied' historical sources.

## References