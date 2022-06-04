# Using burgerLinker on data from civil registries from OpenArch

## Step 1: Get list of relevant certificates
A CSV-file is constructed (for instance by hand) with URL's of relevant certificates. In the CSV-file there must be a column named 'URL' containing the URL of the relevant certificate on [Open Archives](https://openarch.nl/). In this example three csv-files are available: geboorteaktes.csv, huwelijksaktes.csv and overlijdensaktes.csv.

## Step 2: Harvest data from OpenArch, using the URL
Python3 script ```harvestOpenarchRDF.py``` harvests data from OpenArch. The script reads the CSV-file and resolves the URI with accept-header: text/turtle. The result of the harvest is stored in directory "harvested".

## Step 3: Harvested data is transformed into civ-format
Python3 script ```transformOpenarchRDF.py``` uses a SPARQL CONSTRUCT query to transform the data according to the specification to be used in the [burgerLinker](https://github.com/CLARIAH/burgerLinker). The result of the transformation is stored in directory "transformed". It contains separate files for each URI and a combination of all data per certificate-type in geboorteaktes.ttl, huwelijksaktes.ttl and overlijdensaktes.ttl.

## Step 4: Using burgerLinker to create HDT-files
Put the burgerLinker.jar in the same directory as the *.py files.

Make HDT: 
```
java -jar burgerLinker.jar --function ConvertToHDT --inputData transformed/huwelijksaktes.ttl --outputDir hdt
java -jar burgerLinker.jar --function ConvertToHDT --inputData transformed/overlijdensaktes.ttl --outputDir hdt
java -jar burgerLinker.jar --function ConvertToHDT --inputData transformed/geboorteaktes.ttl --outputDir hdt

java -jar burgerLinker.jar --function ConvertToHDT --inputData hdt/huwelijksaktes.hdt,hdt/geboorteaktes.hdt,hdt/overlijdensaktes.hdt --outputDir hdt
```

Get stats and check whether the data is parsed correctly:
```
java -jar burgerLinker.jar --function ShowDatasetStats --inputData hdt/merged-dataset.hdt
```
(Apparently it removes registries that have too less data to be linked)

## Step 5: Create links between Birth and Marriage
Use the burgerLinker again:

```
java -jar burgerLinker.jar --function Within_B_M --inputData hdt/merged-dataset.hdt --outputDir . --format CSV --maxLev 3 --fixedLev
```

## Step 6: Create links between Persons

```
java -jar burgerLinker.jar --function closure --inputData hdt/merged-dataset.hdt --outputDir .
```