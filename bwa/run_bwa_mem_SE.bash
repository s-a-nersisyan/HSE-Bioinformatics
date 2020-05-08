# This script runs cutadapt on all fastq files in given folder
# 1st argument - path with input fastq files
# 2nd argument - folder in which output should be written
# 3nd argument - number of threads
# Example: path_to_this_script.bash /folder/with/fastq/files /output/folder 8

IN_PATH=$1
OUT_PATH=$2
GENOME_PATH=$3
N_THREADS=$4

# Create output folder if not already created
mkdir -p ${OUT_PATH}

# Iterate through all fastq files in IN_PATH and run fastqc
for filename in ${IN_PATH}/*.fastq; do
	sample_name=$(basename -s ".fastq" $filename)
	echo "Started bwa mem for ${filename}"
	bwa mem -t ${N_THREADS} ${GENOME_PATH} ${filename} > "${OUT_PATH}/${sample_name}.sam"
	echo "Finished bwa mem for ${filename}"
	
	echo "Started sam -> bam conversion for ${filename}"
	samtools sort "${OUT_PATH}/${sample_name}.sam" -o "${OUT_PATH}/${sample_name}.sorted.bam" -@ ${N_THREADS}
	samtools index "${OUT_PATH}/${sample_name}.sorted.bam" -@ ${N_THREADS}
	echo "Finished sam -> bam conversion for ${filename}"
done
