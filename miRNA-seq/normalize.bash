IN_PATH=$1
OUT_PATH=$2

BASEDIR=$(dirname "$0")
Rscript ${BASEDIR}/normalize_counts_edgeR.R ${IN_PATH}/isomiR_5prime_counts.tsv ${OUT_PATH}/isomiR_5prime_CPM.tsv
Rscript ${BASEDIR}/normalize_counts_edgeR.R ${IN_PATH}/isomiR_counts.tsv ${OUT_PATH}/isomiR_CPM.tsv
Rscript ${BASEDIR}/normalize_counts_edgeR.R ${IN_PATH}/miRNA_counts_BCGSC.tsv ${OUT_PATH}/miRNA_CPM_BCGSC.tsv
Rscript ${BASEDIR}/normalize_counts_edgeR.R ${IN_PATH}/miRNA_counts_miRDeep2.tsv ${OUT_PATH}/miRNA_CPM_miRDeep2.tsv
