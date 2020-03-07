# This script runs cutadapt on all fastq files in given folder
# 1st argument - path with input fastq files
# 2nd argument - folder in which output should be written
# 3nd argument - number of threads
# Example: path_to_this_script.bash /folder/with/fastq/files /output/folder 8

IN_PATH=$1
OUT_PATH=$2
N_THREADS=$3

TRIMMOMATIC_PATH="/home/steve/software/Trimmomatic-0.39/"

# Create output folder if not already created
mkdir -p ${OUT_PATH}

# Iterate through all fastq files in IN_PATH and run fastqc
for filename in ${IN_PATH}/*.fastq; do
	sample_name=$(basename $filename)
	echo "Started Trimmomatic for ${filename}"
	java -jar ${TRIMMOMATIC_PATH}/trimmomatic-0.39.jar SE -threads ${N_THREADS} ${filename} \
				    "${OUT_PATH}/${sample_name}" ILLUMINACLIP:${TRIMMOMATIC_PATH}/adapters/TruSeq3-SE.fa:2:30:10 LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
	
	echo "Finished Trimmomatic for ${filename}"
done
