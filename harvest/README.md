# data from civil registries

Python 3 script harvestOpenarch.py harvests data from the [Open Archives API](https://api.openarch.nl/). Input is the list of certificates listed in 'aktes.csv'. In the script the function 'createGraph' in openarchLib.py is used, which creates a RDF graph according to the specification to be used in the [burgerLinker](https://github.com/CLARIAH/burgerLinker).

## Usage

```
./harvestOpenarch.py
```

Put the burgerLinker.jar in this directory.

Make HDT: 
```
java -jar burgerLinker.jar --function ConvertToHDT --inputData aktesdata.ttl --outputDir .
```

```
java -jar burgerLinker.jar --function ShowDatasetStats --inputData aktesdata.hdt
```

```
java -jar burgerLinker.jar --function Within_B_M --inputData aktesdata.hdt --outputDir . --format CSV --maxLev 3 --fixedLev
```

This last step does not seem to work (yet).