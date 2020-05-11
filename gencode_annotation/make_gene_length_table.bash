IN_GTF=$1
OUT_FILE=$2

/home/steve/software/GTFtools_0.6.9/gtftools.py -l ${OUT_FILE} ${IN_GTF}
rm "${IN_GTF}.ensembl"
