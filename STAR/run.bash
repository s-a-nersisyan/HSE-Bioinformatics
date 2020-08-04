# This script runs STAR mapper on all fastq files in given folder
# 1st argument - path with input fastq files
# 2nd argument - path to indexed genome
# 3rd argument - folder in which output should be written
# 4th argument - number of threads
# Example: path_to_this_script.bash /folder/with/fastq/files /path/to/genome /output/folder 8

IN_PATH=$1
GENOME_PATH=$2
OUT_PATH=$3
N_THREADS=$4
STAR_PATH=~/huge/software/STAR/bin/Linux_x86_64/STAR

${STAR_PATH} \
	--genomeLoad LoadAndExit \
	--genomeDir ${GENOME_PATH} \
	--outFileNamePrefix ${OUT_PATH}/

for filename in ${IN_PATH}/*_1.fastq; do
	sample_name=$(basename -s "_1.fastq" ${filename})
	mkdir -p ${OUT_PATH}/${sample_name}/
	${STAR_PATH} \
		--genomeDir ${GENOME_PATH} \
		--genomeLoad LoadAndKeep \
		--readFilesIn ${IN_PATH}/${sample_name}_1.fastq ${IN_PATH}/${sample_name}_2.fastq \
		--outFileNamePrefix ${OUT_PATH}/${sample_name}/ \
		--quantMode GeneCounts \
		--runThreadN ${N_THREADS}
	
	cat ${OUT_PATH}/${sample_name}/ReadsPerGene.out.tab | tail -n +5 | cut -f 1,2 > ${OUT_PATH}/${sample_name}.counts
done

${STAR_PATH} \
	--genomeLoad Remove \
	--genomeDir ${GENOME_PATH} \
	--outFileNamePrefix ${OUT_PATH}/
