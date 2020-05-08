# This script runs cutadapt on all fastq files in given folder
# 1st argument - path with input CEL files
# 2nd argument - path to GPL annotation file from GEO
# 3rd argument - folder in which output should be written

CWD=$(realpath $0 | xargs dirname)
IN_PATH=$1
GPL_PATH=$2
OUT_PATH=$3

mkdir -p ${OUT_PATH}
Rscript ${CWD}/affy_rma.R ${IN_PATH} ${OUT_PATH}
python3 ${CWD}/annotate.py ${OUT_PATH}/rma_normalized.tsv ${GPL_PATH} ${OUT_PATH}
rm ${IN_PATH}/rma_normalized.tsv
