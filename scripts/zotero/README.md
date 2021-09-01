# Zotero Translator to RDF/XML (schema.org)

I collect sources and literature on typographical associations in the open source Reference Managementsystem [Zotero](https://zotero.org/). The collected references are available [here](https://www.zotero.org/groups/2707622/typografische-verenigingen/library).

This JavaScript file transforms this data into RDF/XML. It is an adoption of the already available 'Zotero RDF' script created by Simon Kornblith. I used the [schema.org](https://schema.org/) concepts and properties as much as possible to model the data. For archival sources I had to use a workaround as described below.

NB: this is my first attempt doing this, so it is work-in-progress (but what's not ...)

NB2: maybe in the future exporting Zotero in CSV and transforming that into RDF with CoW turns out the be more efficient ...

## Usage
1. Copy the file Schema.org.js to -/Zotero/translators on your computer.
1. Use the "Export Library", "Export Collection" or "Export Item" function in Zotero and choose "Schema.org"
1. Have fun!

## Archival sources
(not yet implemented in the script, so maybe the workaround changes if this turns out to be too complex to implement in the script)
Unfortunately Zotero does not support ([yet?](https://forums.zotero.org/discussion/comment/374107)) efficient and unambiguous ways of storing data on original archival sources. This means I had to design a workaround for storing data on archival material and incorporate this design in my translator. If you want to reuse this script you either must adopt my workaround or create your own workaround and adjust the script accordingly.

### My workaround for storing archival sources
* I create a collection for every (archival) fonds.
* In the collection I store a description of the fonds with the Zotero "Manuscript" documenttype, and use the type-field to indicate that this description is about the 'fonds' as a whole.
* I store a description of the relevant material, part of the fonds, in a separate "Manuscript" documenttype, and use the type-field to indicate that this description is about an 'item', 'file' or 'series'. (Following [ISAD(G)](https://www.ica.org/en/isadg-general-international-standard-archival-description-second-edition))

## Links
(TBD)

### Internal
Because I intend to create Linked Data, I need links instead of strings in some fields. For now, my Zotero-dataset has two links:
* links to the archival and library institutions holding the material. I use ISIL codes as much as possible, and create my own identifier if the ISIL is not available.
* links to the specific typographical association a reference is about. I create my own list of identifiers for this.

For both things I created a csv-file with information about these nodes in my knowledge graph. These are to be transformed into RDF with CoW. Besides that I need to transform the identifier I used in Zotero into the appropriate URI.

### External
Obviously I need to store and export the URI of the source provided by the holding institution.