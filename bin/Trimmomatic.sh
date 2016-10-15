#!/bin/bash

###################################################################3
#ILLUMINACLIP:<fastaWithAdaptersEtc>:<seed mismatches>:<palindrome clip threshold>:<simple clip threshold>:<minAdapterLength>:<keepBothReads>
#SLIDINGWINDOW:<windowSize>:<requiredQuality> 
#LEADING:<quality>
####################################################################

path_to_trimmo="../tools/trimmomatic-0.36/trimmomatic-0.36.jar"
path_to_adapters="../tools/trimmomatic-0.36/adapters/"
path_to_res="../data/first_try/trimmed_seqs/"
path_to_inp_data="../data/first_try/sequences/"
if [ ! -d "$path_to_res" ]; then #!!!! SymLink will also pass this condition
    mkdir $path_to_res
fi


adapter="TruSeq3-SE.fa"
res_file_name="trimmed_seq"
full_path_to_adapter="$path_to_adapters$adapter"
full_path_to_res="$path_to_res$res_file_name"
echo "!!!$full_path_to_res"
#path_to_inp_data=$1

p="$path_to_inp_data*R1*.fastq.gz"
echo "!!!!$p"
for file in $p
do
    echo "Processing $file file..."
    java -jar $path_to_trimmo PE -basein $file -baseout $full_path_to_res ILLUMINACLIP:$full_path_to_adapter:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36 > /dev/null
done
