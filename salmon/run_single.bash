# This script runs salmon quasi-mapper on all fastq files in given folder
# 1st argument - path with input fastq files
# 2nd argument - path to indexed genome
# 3rd argument - folder in which output should be written
# 4th argument - number of threads
# Example: path_to_this_script.bash /folder/with/fastq/files /path/to/salmon_index (~/huge/bulk/GENCODE_human_34/gencode.v34.transcripts.fa) /output/folder 8

IN_PATH=$1
GENOME_PATH=$2
OUT_PATH=$3
N_THREADS=$4

for filename in ${IN_PATH}/*.fastq; do
	sample_name=$(basename -s ".fastq" ${filename})
	mkdir -p ${OUT_PATH}/${sample_name}/
	salmon quant -i ${GENOME_PATH} \
		-l A \
		-r ${IN_PATH}/${sample_name}.fastq \
		-p ${N_THREADS} \
		--validateMappings \
		-o ${OUT_PATH}/${sample_name}/

	#cat ${OUT_PATH}/${sample_name}/ReadsPerGene.out.tab | tail -n +5 | cut -f 1,2 > ${OUT_PATH}/${sample_name}.counts
done
