# This script runs BCGSC pipeline on fastq files in given folder
# 1st argument - path with input .fastq files. Absolute path should be specified!
# 2nd argument - path to indexed reference genome (with .fa extension)
# 3rd argument - species ID (e.g. hsa, mmu, cel)
# 4nd argument - folder in which output should be written. Absolute path should be specified!
# 5th argument - number of threads
# Example: path_to_this_script.bash /folder/with/fastq/files /path/to/reference.genome hsa /output/folder 8

IN_PATH=$1
REFERENCE_GENOME=$2
SPECIES=$3
OUT_PATH=$4
N_THREADS=$5

# Iterate through all .fastq files in IN_PATH and run mapping
mkdir -p ${OUT_PATH}/results/pool
cd ${OUT_PATH}
for file in ${IN_PATH}/*.fastq; do
	FILE_ID=$(basename $file ".fastq")
	bwa aln ${REFERENCE_GENOME} ${file} -t ${N_THREADS} > ${FILE_ID}.sai
	bwa samse -n 10 ${REFERENCE_GENOME} ${FILE_ID}.sai ${file} > results/pool/pool_${FILE_ID}.sam
	rm ${FILE_ID}.sai
	samtools view results/pool/pool_${FILE_ID}.sam | \
			awk '{arr[length($10)]+=1} END {for (i in arr) {print i" "arr[i]}}' | \
			sort -t " " -k1n > results/pool/pool_${FILE_ID}_adapter.report
done

annotate.pl -m mirbase -u hg38 -o $SPECIES -p results
alignment_stats.pl -p results
expression_matrix.pl -m mirbase -o $SPECIES -p results
tcga.pl -m mirbase -o $SPECIES -g hg38 -p results
graph_libs.pl -p results
