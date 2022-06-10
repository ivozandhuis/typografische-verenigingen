rm hdt/*

java -jar burgerLinker.jar --function ConvertToHDT --inputData transformed/huwelijksaktes.nt --outputDir hdt
java -jar burgerLinker.jar --function ConvertToHDT --inputData transformed/overlijdensaktes.nt --outputDir hdt
java -jar burgerLinker.jar --function ConvertToHDT --inputData transformed/geboorteaktes.nt --outputDir hdt

java -jar burgerLinker.jar --function ConvertToHDT --inputData hdt/huwelijksaktes.hdt,hdt/geboorteaktes.hdt,hdt/overlijdensaktes.hdt --outputDir hdt

java -jar burgerLinker.jar --function ShowDatasetStats --inputData hdt/merged-dataset.hdt

java -jar burgerLinker.jar --function Within_B_M --inputData hdt/merged-dataset.hdt --outputDir . --format CSV --maxLev 3 --fixedLev

java -jar burgerLinker.jar --function closure --inputData hdt/merged-dataset.hdt --outputDir .
