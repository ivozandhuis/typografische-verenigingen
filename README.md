# Linking Linked Data tools
Ivo Zandhuis (@ivozandhuis)
International Institute of Social History

## Introduction
Archival sources, digital processible text/data and relevant literature are the raw materials an historian uses to construct his story and analysis. All these building blocks are interrelated: the primary source is the basis for a dataset or processible text, a data analyses is part of the argument made in an historical paper, of which its footnotes contain references to sources and literature. In order to create a thorough and reproducible historical reconstruction or explanation all these building blocks and its relations should be stored in a network (or 'graph') that is reusable and processible in an automatic way. Because of its gradual adoption Linked Data is the most obvious technique to use in this endeavour.

In this repo I'm building such a graph for research into a Dutch phenomenon called 'typografische verenigingen'. During the first half of the 19th century print labourers in The Netherlands ('typografen') organized themselves in these local associations. These associations were founded to ensure sickness benefits and organize a yearly feast to celebrate their identity as 'children of Laurens Coster', the Dutch man they believed invented printing. They were connected in a nation wide network and organized the erection of a statue in Coster's honour. Eventually this led to the establishment of the first national union in The Netherlands in 1866. I'm interested in how this phenomenon developed through time, until its cancellation in the 20th century.

This practical use case teaches us a lot about how digital building blocks, needed to study the subject, can be created, linked and stored. Various types of building blocks are created and stored in different applications. I try to find online tooling to do this, with -obviously- the possibility to export or convert data into the Linked Data format RDF. The results of these actions are combined into the aimed graph. But how easy can we construct the links between data created in the different applications?

Central nodes in the graph are [sources and literature recorded in Zotero](https://www.zotero.org/groups/2707622/typografische-verenigingen/library). Zotero is a convenient tool for recording resources and creating footnotes in the historical papers that eventually will be written based on the material. Metadata about sources and literature is obtained from the catalogues maintained by GLAM-instutions holding the material. A link to the original description in the catalogue should be kept, but not always a sustainable URI is available. I developed a preliminary translator for the data in Zotero to RDF. 

In the Zotero-data I refer to individual typographical associations and cultural heritage institutions holding the material. For these entities I have created csv-files from which I derive nodes in my graph. To do this I use [CoW](https://github.com/CLARIAH/COW) to convert the csv into RDF. The [LDWizard](https://ldwizard.netwerkdigitaalerfgoed.nl/) can be used to create an easy kick-off for developing a transformation script. The LDWizard and CoW are convenient tools to transform data about persons as well. In some of the archives membership registers are handed done and I create datasets from them in csv-format. These references to persons are linked to the original sources, linked to sources with additional demographical data (future work) and linked to each other, for instance with family relations (future work).

[Recogito](https://recogito.pelagios.org/) enables users to create textual or image sources with links in the text or on the image. The links are typed (is the marking a person, place or event?) and for places can be reconciled to for instance [geonames](https://geonames.org/). From this tool text can be exported into TEI/XML format and the links can - although incomplete - be exported into RDF. 

First conclusions in the experiments are that every tool is good in its particular function (reference management, data conversion, source enrichment). Creating the combined graph needs thorough thinking and some additional coding, because the links _between_ the data exported from the tools can not be easily created and stored. Future development of tooling should take the decentralised data principle of Linked Data into account.

Future work:
* expand on the data
* find new/better tools
** nodegoat
* answer the question: how to publish my graph?

## References