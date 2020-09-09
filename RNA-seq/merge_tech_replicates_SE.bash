IN_PATH=$1
OUT_PATH=$2

mkdir -p $OUT_PATH

for filename in ${IN_PATH}/*_L001_R1_001.fastq; do
	sample_id=$(basename -s "_L001_R1_001.fastq" ${filename})
	cat ${IN_PATH}/${sample_id}_* > ${OUT_PATH}/${sample_id}.fastq &
done
wait
