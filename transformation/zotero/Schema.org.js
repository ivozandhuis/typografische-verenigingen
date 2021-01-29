{
	"translatorID": "29b95718-dbdc-4c03-8c60-662f19fc49b8",
	"label": "Schema.org",
	"creator": "Ivo Zandhuis (based on 'Zotero RDF.js' by Simon Kornblith)",
	"target": "rdf",
	"minVersion": "3.0",
	"maxVersion": "",
	"priority": 100,
	"configOptions": {
		"getCollections": "true",
		"dataMode": "rdf/xml"
	},
	"inRepository": true,
	"translatorType": 2,
	"lastUpdated": "2021-01-29 10:12:00"
}

var item;
var rdf = "http://www.w3.org/1999/02/22-rdf-syntax-ns#";

var n = {
	schema:"https://schema.org/",
	bib:"http://purl.org/net/biblio#",
	dc:"http://purl.org/dc/elements/1.1/",
	dcterms:"http://purl.org/dc/terms/",
	prism:"http://prismstandard.org/namespaces/1.2/basic/",
	foaf:"http://xmlns.com/foaf/0.1/",
	vcard:"http://nwalsh.com/rdf/vCard#",
	vcard2:"http://www.w3.org/2006/vcard/ns#",	// currently used only for NSF, but is probably
												// very similar to the nwalsh vcard ontology in a
												// different namespace
	link:"http://purl.org/rss/1.0/modules/link/",
	z:"http://www.zotero.org/namespaces/export#"
};

function generateRelations(resource, relations) {
	for (let predicate in relations) {
		if (predicate == 'dc:relation') {
			for (let uri of relations[predicate]) {
				if (itemResources[uri]) {
					Zotero.RDF.addStatement(resource, n.dc + "relation", itemResources[uri], false);
				}
			}
		}
	}
}

function generateTags(resource, tags) {
	Zotero.debug("processing tags");
	for (var i=0; i<tags.length; i++) {
		var tag = tags[i];
		if (tag.type == 1) {
			var tagResource = Zotero.RDF.newResource();
			// set tag type and value
			Zotero.RDF.addStatement(tagResource, rdf+"type", n.z+"AutomaticTag", false);
			Zotero.RDF.addStatement(tagResource, rdf+"value", tag.tag, true);
			// add relationship to resource
			Zotero.RDF.addStatement(resource, n.schema+"about", tagResource, false);
		} else {
			Zotero.RDF.addStatement(resource, n.schema+"about", tag.tag, true);
		}
	}
}

function generateCollection(collection) {
	var collectionResource = "#collection_"+collection.id;
	Zotero.RDF.addStatement(collectionResource, rdf+"type", n.schema+"Collection", false);
	Zotero.RDF.addStatement(collectionResource, n.schema+"name", collection.name, true);
	
	var children = collection.children ? collection.children : collection.descendents;
	if (!children) return;
	for (var i=0; i<children.length; i++) {
		var child = children[i];
		// add child list items
		if (child.type == "collection") {
			Zotero.RDF.addStatement(collectionResource, n.schema+"hasPart", "#collection_"+child.id, false);
			// do recursive processing of collections
			generateCollection(child);
		} else if (itemResources[child.id]) {
			Zotero.RDF.addStatement(collectionResource, n.schema+"hasPart", itemResources[child.id], false);
		}
	}
}

/**
 * Get display title
 * Analogous to getDisplayTitle in item.js, but returns null if no display title distinct from
 * title property
 */
function getDisplayTitle(item) {
	if (!item.title && (item.itemType == "interview" || item.itemType == "letter")) {
		var participants = [];
		for (var i=0; i<item.creators.length; i++) {
			var creator = item.creators[i];
			if (item.itemType == "letter" && creator.creatorType == "recipient" ||
					item.itemType == "interview" && creator.creatorType == "interviewer") {
			   participants.push(creator);
			}
		}
		
		var displayTitle = "["+(item.itemType == "letter" ? "Letter" : "Interview");
		if (participants.length) {
			//var names = [creator.firstName ? creator.firstName+" "+creator.lastName : creator.lastName
			var names = [];
			for (var j=0; j<participants.length; j++) {
				names.push(participants[j].lastName);
			}
			
			displayTitle += (item.itemType == "letter" ? " to " : " of ")+names[0];
			
			if (participants.length == 2) {
				displayTitle += " and "+names[1];
			} else if (participants.length == 3) {
				displayTitle += ", "+names[1]+", and "+names[2];
			} else if (participants.length > 3) {
				displayTitle += " et al.";
			}
		}
		
		return displayTitle+"]";
	} if (item.itemType == "case" && item.title && item.reporter) { // 'case' itemTypeID
		return item.title+' (' + item.reporter + ')';
	}
	return null;
}

function generateItem(item, zoteroType, resource) {
	var container = null;
	var containerElement = null;
	
	/** CORE FIELDS **/
	
	// type
	var type = null;
	if (zoteroType == "book") {
		type = n.schema+"Book";
	} else if (zoteroType == "bookSection") {
		type = n.bib+"BookSection";
		container = n.bib+"Book";
	} else if (zoteroType == "journalArticle") {
		type = n.schema+"Article";
		container = n.schema+"Periodical";
	} else if (zoteroType == "magazineArticle") {
		type = n.schema+"Article";
		container = n.schema+"Periodical";
	} else if (zoteroType == "newspaperArticle") {
		type = n.schema+"Article";
		container = n.schema+"Newspaper";
	} else if (zoteroType == "thesis") {
		type = n.schema+"Thesis";
	} else if (zoteroType == "letter") {
		type = n.bib+"Letter";
	} else if (zoteroType == "manuscript") {
		type = n.schema+"Manuscript";
	} else if (zoteroType == "interview") {
		type = n.bib+"Interview";
	} else if (zoteroType == "film") {
		type = n.schema+"Movie";
	} else if (zoteroType == "artwork") {
		type = n.schema+"VisualArtwork";
	} else if (zoteroType == "webpage") {
		type = n.schema+"WebPage";
		container = n.z+"Website";
	} else if (zoteroType == "note") {
		type = n.bib+"Memo";
		if (!Zotero.getOption("exportNotes")) {
			return;
		}
	} else if (zoteroType == "attachment") {
		type = n.z+"Attachment";
	} else if (zoteroType == "report") {
		type = n.schema+"Report";
	} else if (zoteroType == "bill") {
		type = n.bib+"Legislation";
	} else if (zoteroType == "case") {
		type = n.bib+"Document";	// ??
		container = n.bib+"CourtReporter";
	} else if (zoteroType == "hearing") {
		type = n.schema+"Report";
	} else if (zoteroType == "patent") {
		type = n.bib+"Patent";
	} else if (zoteroType == "statute") {
		type = n.bib+"Legislation";
	} else if (zoteroType == "email") {
		type = n.bib+"Letter";
	} else if (zoteroType == "map") {
		type = n.bib+"Image";
	} else if (zoteroType == "blogPost") {
		type = n.bib+"Document";
		container = n.z+"Blog";
	} else if (zoteroType == "instantMessage") {
		type = n.bib+"Letter";
	} else if (zoteroType == "forumPost") {
		type = n.bib+"Document";
		container = n.z+"Forum";
	} else if (zoteroType == "audioRecording") {
		type = n.bib+"Recording";
	} else if (zoteroType == "presentation") {
		type = n.bib+"ConferenceProceedings";
	} else if (zoteroType == "videoRecording") {
		type = n.bib+"Recording";
	} else if (zoteroType == "tvBroadcast") {
		type = n.bib+"Recording";
	} else if (zoteroType == "radioBroadcast") {
		type = n.bib+"Recording";
	} else if (zoteroType == "podcast") {
		type = n.bib+"Recording";
	} else if (zoteroType == "computerProgram") {
		type = n.schema+"SoftwareApplication";
	} else if (zoteroType == "encyclopediaArticle"
		|| zoteroType == "dictionaryEntry") {
		container = n.bib+"Book";
	} else if (zoteroType == "conferencePaper") {
		container = n.bib+"Journal";
	}
	
	if (type) {
		Zotero.RDF.addStatement(resource, rdf+"type", type, false);
	}
	Zotero.RDF.addStatement(resource, n.schema+"additionalType", zoteroType, true);
	
	// generate section
	if (item.section) {
		var section = Zotero.RDF.newResource();
		// set section type
		Zotero.RDF.addStatement(section, rdf+"type", n.bib+"Part", false);
		// set section title
		Zotero.RDF.addStatement(section, n.schema+"name", item.section, true);
		// add relationship to resource
		Zotero.RDF.addStatement(resource, n.schema+"isPartOf", section, false);
	}
	
	// generate container
	if (container) {
		var testISSN = "urn:issn:"+encodeURI(item.ISSN);
		if (item.ISSN && !Zotero.RDF.getArcsIn(testISSN)) {
			// use ISSN as container URI if no other item is
			containerElement = testISSN;
		} else {
			containerElement = Zotero.RDF.newResource();
		}
		// attach container to section (if exists) or resource
		Zotero.RDF.addStatement((section ? section : resource), n.schema+"isPartOf", containerElement, false);
		// add container type
		Zotero.RDF.addStatement(containerElement, rdf+"type", container, false);
	}
	
	// generate series
	if (item.series || item.seriesTitle || item.seriesText || item.seriesNumber) {
		var series = Zotero.RDF.newResource();
		// set series type
		Zotero.RDF.addStatement(series, rdf+"type", n.bib+"Series", false);
		// add relationship to resource
		Zotero.RDF.addStatement((containerElement ? containerElement : resource), n.schema+"isPartOf", series, false);
	}
	
	// generate publisher
	// BEGIN NSF
	if (zoteroType == "nsfReviewer") {
		var organization = Zotero.RDF.newResource();
		Zotero.RDF.addStatement(organization, rdf+"type", n.schema+"Organization", false);
		Zotero.RDF.addStatement(resource, n.schema+"name", organization, false); // ??
	} else {
	// END NSF
		if (item.publisher || item.distributor || item.label || item.company || item.institution || item.place) {
			var organization = Zotero.RDF.newResource();
			// set organization type
			Zotero.RDF.addStatement(organization, rdf+"type", n.schema+"Organization", false);
			// add relationship to resource
			Zotero.RDF.addStatement(resource, n.schema+"publisher", organization, false);
		}
	}
	
	var typeProperties = ["reportType", "videoRecordingType", "letterType",
							"manuscriptType", "mapType", "thesisType", "websiteType",
							"audioRecordingType", "presentationType", "postType",
							"audioFileType"];
	var ignoreProperties = ["itemID", "itemType", "firstCreator", "dateAdded",
							"dateModified", "section", "sourceItemID"];
	
	// creators
	if (item.creators) {			// authors/editors/contributors
		var creatorContainers = new Object();
		
		// not yet in biblio
		var schemaCreatorTypes = ["author", "editor", "contributor"];
		
		for (var j in item.creators) {
			var creator = Zotero.RDF.newResource();
			Zotero.RDF.addStatement(creator, rdf+"type", n.schema+"Person", false);
			Zotero.RDF.addStatement(creator, n.schema+"familyName", item.creators[j].lastName, true);
			if (item.creators[j].firstName) {
				Zotero.RDF.addStatement(creator, n.schema+"givenName", item.creators[j].firstName, true);
			}
			
			if (schemaCreatorTypes.indexOf(item.creators[j].creatorType) != -1) {
				var cTag = n.schema+item.creators[j].creatorType;
			} else {
				var cTag = n.z+item.creators[j].creatorType;
			}
			
			Zotero.RDF.addStatement(resource, cTag, creator, false);

		}
	}
	
	// notes
	if (item.notes && Zotero.getOption("exportNotes")) {
		for (let note of item.notes) {
			let noteResource = itemResources[note.itemID];
			
			// add note tag
			Zotero.RDF.addStatement(noteResource, rdf+"type", n.bib+"Memo", false);
			// add note item.notes
			Zotero.RDF.addStatement(noteResource, rdf + "value", note.note, true);
			// add relationship between resource and note
			Zotero.RDF.addStatement(resource, n.dcterms+"isReferencedBy", noteResource, false);
			
			// Add note relations to RDF
			if (note.relations) generateRelations(noteResource, note.relations);
			generateTags(noteResource, note.tags);
		}
	}
	
	// child attachments
	if (item.attachments) {
		for (var i=0; i<item.attachments.length; i++) {
			var attachment = item.attachments[i];
			var attachmentResource = itemResources[attachment.itemID];
			Zotero.RDF.addStatement(resource, n.schema+"url", attachmentResource, false);
			generateItem(attachment, "attachment", attachmentResource);
		}
	}
	
	// relative file path for attachment items
	if (item.defaultPath) {	// For Zotero 3.0
		item.saveFile(item.defaultPath, true);
		Zotero.RDF.addStatement(resource, rdf+"resource", item.defaultPath, false);
	} else if (item.path) {	// For Zotero 2.1
		Zotero.RDF.addStatement(resource, rdf+"resource", item.path, false);
	}
    
	// Related items and tags
	if (item.relations) generateRelations(resource, item.relations);
	if (item.tags) generateTags(resource, item.tags);
	
	for (var property in item.uniqueFields) {
		var value = item[property];
		if (!value) continue;
		
		if (property == "title") {					// title
			// BEGIN NSF
			if (zoteroType == "nsfReviewer") {
				Zotero.RDF.addStatement(resource, n.schema+"name", value, true);
			} else {
			// END NSF
				Zotero.RDF.addStatement(resource, n.schema+"name", value, true);
			}
		} else if (property == "source") {			// authors/editors/contributors
			Zotero.RDF.addStatement(resource, n.dc+"source", value, true);
		} else if (property == "url") {				// url
			Zotero.RDF.addStatement(resource, n.schema+"url", value, false);
		} else if (property == "accessionNumber") {	// accessionNumber as generic ID
			Zotero.RDF.addStatement(resource, n.schema+"identifier", value, true);
		} else if (property == "rights") {			// rights
			Zotero.RDF.addStatement(resource, n.dc+"rights", value, true);
		} else if (property == "edition" ||			// edition
		          property == "version") {			// version
			Zotero.RDF.addStatement(resource, n.prism+"edition", value, true);
		} else if (property == "date") {				// date
			if (item.dateSent) {
				Zotero.RDF.addStatement(resource, n.dcterms+"dateSubmitted", value, true);
			} else {
				Zotero.RDF.addStatement(resource, n.schema+"datePublished", value, true);
			}
		} else if (property == "accessDate") {		// accessDate
			Zotero.RDF.addStatement(resource, n.dcterms+"dateSubmitted", value, true);
		} else if (property == "issueDate") {		// issueDate
			Zotero.RDF.addStatement(resource, n.dcterms+"issued", value, true);
		} else if (property == "pages") {			// pages
			// not yet part of biblio, but should be soon
			Zotero.RDF.addStatement(resource, n.bib+"pages", value, true);
		} else if (property == "extra") {			// extra
			Zotero.RDF.addStatement(resource, n.schema+"description", value, true);
		} else if (property == "mimeType") {			// mimeType
			Zotero.RDF.addStatement(resource, n.link+"type", value, true);
		} else if (property == "charset") {			// charset
			Zotero.RDF.addStatement(resource, n.link+"charset", value, true);
		// THE FOLLOWING ARE ALL PART OF THE CONTAINER
		} else if (property == "ISSN") {				// ISSN
			Zotero.RDF.addStatement((containerElement ? containerElement : resource), n.schema+"identifier", "ISSN "+value, true);
		} else if (property == "ISBN") {				// ISBN
			Zotero.RDF.addStatement((containerElement ? containerElement : resource), n.schema+"identifier", "ISBN "+value, true);
		} else if (property == "DOI") {				// DOI
			Zotero.RDF.addStatement((containerElement ? containerElement : resource), n.schema+"identifier", "DOI "+value, true);
		} else if (property == "publicationTitle" ||	// publicationTitle
		          property == "reporter") {			// reporter
			Zotero.RDF.addStatement((containerElement ? containerElement : resource), n.schema+"title", value, true);
		} else if (property == "journalAbbreviation") {	// journalAbbreviation
			Zotero.RDF.addStatement((containerElement ? containerElement : resource), n.dcterms+"alternative", value, true);
		} else if (property == "volume") {			// volume
			Zotero.RDF.addStatement((containerElement ? containerElement : resource), n.prism+"volume", value, true);
		} else if (property == "issue" ||			// issue
				  property == "number" ||			// number
				  property == "patentNumber") {		// patentNumber
			Zotero.RDF.addStatement((containerElement ? containerElement : resource), n.prism+"number", value, true);
		} else if (property == "callNumber") {
			var term = Zotero.RDF.newResource();
			// set term type
			Zotero.RDF.addStatement(term, rdf+"type", n.dcterms+"LCC", false);
			// set callNumber value
			Zotero.RDF.addStatement(term, rdf+"value", value, true);
			// add relationship to resource
			Zotero.RDF.addStatement(resource, n.schema+"about", term, false);
		} else if (property == "abstractNote") {
			Zotero.RDF.addStatement(resource, n.schema+"abstract", value, true);
		// THE FOLLOWING ARE ALL PART OF THE SERIES
		} else if (property == "series") {			// series
			Zotero.RDF.addStatement(series, n.schema+"name", value, true);
		} else if (property == "seriesTitle") {		// seriesTitle
			Zotero.RDF.addStatement(series, n.dcterms+"alternative", value, true);
		} else if (property == "seriesText") {		// seriesText
			Zotero.RDF.addStatement(series, n.schema+"description", value, true);
		} else if (property == "seriesNumber") {		// seriesNumber
			Zotero.RDF.addStatement(series, n.schema+"identifier", value, true);
		// THE FOLLOWING ARE ALL PART OF THE PUBLISHER
		} else if (property == "publisher" ||		// publisher
		          property == "distributor" ||		// distributor (film)
		          property == "label" ||			// label (audioRecording)
		          property == "company" ||			// company (computerProgram)
		          property == "institution") {		// institution (report)
		    // BEGIN NSF
		    if (zoteroType == "nsfReviewer") {
		    	Zotero.RDF.addStatement(organization, n.schema+"name", value, true);
		    } else {
		    // END NSF
				Zotero.RDF.addStatement(organization, n.schema+"name", value, true);
			}
		} else if (property == "place") {			// place
			var address = Zotero.RDF.newResource();
			// set address type
			Zotero.RDF.addStatement(address, rdf+"type", n.schema+"Place", false);
			// set address locality
			Zotero.RDF.addStatement(address, n.schema+"name", value, true);
			// add relationship to organization
			Zotero.RDF.addStatement(organization, n.schema+"address", address, false);
		} else if (property == "archiveLocation") {	// archiveLocation
			Zotero.RDF.addStatement(resource, n.dc+"coverage", value, true);
		} else if (property == "interviewMedium" ||
		          property == "artworkMedium") {	// medium
			Zotero.RDF.addStatement(resource, n.dcterms+"medium", value, true);
		} else if (property == "conferenceName") {
			var conference = Zotero.RDF.newResource();
			// set conference type
			Zotero.RDF.addStatement(conference, rdf+"type", n.schema+"Event", false);
			// set conference title
			Zotero.RDF.addStatement(conference, n.schema+"name", value, true);
			// add relationship to conference
			Zotero.RDF.addStatement(resource, n.bib+"presentedAt", conference, false);
		} else if (typeProperties.indexOf(property) != -1) {
			Zotero.RDF.addStatement(resource, n.schema+"additionalType", value, true);
		// THE FOLLOWING RELATE TO NOTES
		} else if (property == "note") {
			if (Zotero.getOption("exportNotes")) {
				if (item.itemType == "attachment") {
					Zotero.RDF.addStatement(resource, n.schema+"description", value, true);
				} else if (item.itemType == "note") {
					Zotero.RDF.addStatement(resource, rdf+"value", value, true);
				}
			}
		// BEGIN NSF
		} else if (property == "address") {
			var address = Zotero.RDF.newResource();
			Zotero.RDF.addStatement(address, rdf+"type", n.schema+"PostalAddress", false);
			Zotero.RDF.addStatement(address, n.rdfs+"label", value, true);
			Zotero.RDF.addStatement(resource, n.schema+"streetAddress", address, false);
		} else if (property == "telephone") {
			Zotero.RDF.addStatement(resource, n.schema+"telephone", value, true);
		} else if (property == "email") {
			Zotero.RDF.addStatement(resource, n.schema+"email", value, true);
		} else if (property == "accepted") {
			Zotero.RDF.addStatement(resource, n.dcterms+"dateAccepted", value, true);
		// END NSF
		} else if (property == "language") {
			Zotero.RDF.addStatement(resource, n.schema+"inLanguage", value, true);
		} else if (property == "archive") {
			Zotero.RDF.addStatement(resource, n.schema+"holdingArchive", value, true);
		// THIS CATCHES ALL REMAINING PROPERTIES
		} else if (ignoreProperties.indexOf(property) == -1) {
			Zotero.debug("Zotero RDF: using Zotero namespace for property "+property);
			Zotero.RDF.addStatement(resource, n.z+property, value, true);
		}
	}
	
	var displayTitle = getDisplayTitle(item);
	if (displayTitle) Zotero.RDF.addStatement(resource, n.z+"displayTitle", displayTitle, true);
}

function doExport() {
	// add namespaces
	for (var i in n) {
		Zotero.RDF.addNamespace(i, n[i]);
	}
	
	// leave as global
	itemResources = new Array();
	
	// keep track of resources already assigned (in case two book items have the
	// same ISBN, or something like that)
	var usedResources = new Array();
	
	var items = new Array();
	
	// first, map each ID to a resource
	while (item = Zotero.nextItem()) {
		items.push(item);
		Zotero.debug(item);
		
		var testISBN = "urn:isbn:"+encodeURI(item.ISBN);
		if (item.ISBN && !usedResources[testISBN]) {
			itemResources[item.itemID] = itemResources[item.uri] = testISBN;
			usedResources[itemResources[item.itemID]] = true;
		} else if (item.itemType != "attachment" && item.url && !usedResources[item.url]) {
			itemResources[item.itemID] = itemResources[item.uri] = item.url;
			usedResources[itemResources[item.itemID]] = true;
		} else {
			// just specify a node ID
			itemResources[item.itemID] = itemResources[item.uri] = "#item_" + item.itemID;
		}
		
		if (item.notes) {
			for (var j in item.notes) {
				itemResources[item.notes[j].itemID] = itemResources[item.notes[j].uri] = "#item_" + item.notes[j].itemID;
			}
		}
		
		if (item.attachments) {
			for (var i=0; i<item.attachments.length; i++) {
				var attachment = item.attachments[i];
				// just specify a node ID
				itemResources[attachment.itemID] = itemResources[attachment.uri] = "#item_" + attachment.itemID;
			}
		}
	}
	
	for (var i=0; i<items.length; i++) {
		var item = items[i];
		// these items are global
		generateItem(item, item.itemType, itemResources[item.itemID]);
	}
	
	/** RDF COLLECTION STRUCTURE **/
	var collection;
	while (collection = Zotero.nextCollection()) {
		generateCollection(collection);
	}
}
