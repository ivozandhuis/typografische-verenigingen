# data from civil registries

Python 3 script harvestOpenarchRDF.py harvests data from the [Open Archives](https://openarch.nl/). Input is the list of certificates listed in '\*.csv'. transformOpenarchRDF.py uses a SPARQL CONSTRUCT query to transform the data according to the specification to be used in the [burgerLinker](https://github.com/CLARIAH/burgerLinker).

## Usage

Get the data from OpenArch defined in CSV files.
```
./harvestOpenarchRDF.py
```

Transform harvested data into datastructure needed for burgerLinker.
```
./transformOpenarchRDF.py
```

Put the burgerLinker.jar in this directory.

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

Create links between Birth and Marriage:
```
java -jar burgerLinker.jar --function Within_B_M --inputData hdt/merged-dataset.hdt --outputDir . --format CSV --maxLev 3 --fixedLev
```

```
java -jar burgerLinker.jar --function closure --inputData hdt/merged-dataset.hdt --outputDir .
```