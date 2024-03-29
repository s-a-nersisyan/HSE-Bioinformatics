# This script runs salmon quasi-mapper on all fastq files in given folder
# 1st argument - path with input fastq files
# 2nd argument - path to indexed genome
# 3rd argument - folder in which output should be written
# 4th argument - number of threads
# Example: path_to_this_script.bash /folder/with/fastq/files /path/to/salmon_index /output/folder 8

IN_PATH=$1
GENOME_PATH=$2
OUT_PATH=$3
N_THREADS=$4

for filename in ${IN_PATH}/*_1.fastq; do
	sample_name=$(basename -s "_1.fastq" ${filename})
	mkdir -p ${OUT_PATH}/${sample_name}/
	salmon quant -i ${GENOME_PATH} \
		-l A \
		-1 ${IN_PATH}/${sample_name}_1.fastq \
		-2 ${IN_PATH}/${sample_name}_2.fastq \
		-p ${N_THREADS} \
		--validateMappings \
		-o ${OUT_PATH}/${sample_name}/
	
	#cat ${OUT_PATH}/${sample_name}/ReadsPerGene.out.tab | tail -n +5 | cut -f 1,2 > ${OUT_PATH}/${sample_name}.counts
done
