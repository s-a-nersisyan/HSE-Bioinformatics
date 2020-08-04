# This script runs fastqc on all fastq files in given folder
# 1st argument - path with input fastq files
# 2nd argument - folder in which output should be written
# 3nd argument - number of threads
# Example: path_to_this_script.bash /folder/with/fastq/files /output/folder 8

IN_PATH=$1
OUT_PATH=$2
N_THREADS=$3

# Create output folder if not already created
mkdir -p ${OUT_PATH}

INPUT_FILES=$(ls ${IN_PATH}/*.fastq)
fastqc -o ${OUT_PATH} -t ${N_THREADS} ${INPUT_FILES}
