# This script runs cutadapt on all fastq files in given folder
# 1st argument - path with input fastq files
# 2nd argument - folder in which output should be written
# 3nd argument - number of threads
# Example: path_to_this_script.bash /folder/with/fastq/files /output/folder 8

IN_PATH=$1
OUT_PATH=$2
N_THREADS=$3

# Create output folder if not already created
mkdir -p ${OUT_PATH}

# Iterate through all fastq files in IN_PATH and run fastqc
for filename in ${IN_PATH}/*.fastq; do
	sample_name=$(basename $filename)
	echo "Started cutadapt for ${filename}"
	cutadapt -a "TGGAATTCTCGGGTGCCAAGG" \
		 -m 18 -j ${N_THREADS} -o "${OUT_PATH}/${sample_name}" ${filename} > "${OUT_PATH}/${sample_name}.log"
	echo "Finished cutadapt for ${filename}"
done
