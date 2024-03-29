IN_PATH=$1
GROUPS_FILE=$2
EXPR_GROUP=$3
CTRL_GROUP=$4
FC_THRESHOLD=$5
OUT_PATH=$6

BASEDIR=$(dirname "$0")
Rscript ${BASEDIR}/DESeq2.R ${IN_PATH}/isomiR_5prime_counts.tsv $GROUPS_FILE $EXPR_GROUP $CTRL_GROUP $FC_THRESHOLD $OUT_PATH "isomiR_5prime"
Rscript ${BASEDIR}/DESeq2.R ${IN_PATH}/isomiR_counts.tsv $GROUPS_FILE $EXPR_GROUP $CTRL_GROUP $FC_THRESHOLD $OUT_PATH "isomiR"
Rscript ${BASEDIR}/DESeq2.R ${IN_PATH}/miRNA_counts_BCGSC.tsv $GROUPS_FILE $EXPR_GROUP $CTRL_GROUP $FC_THRESHOLD $OUT_PATH "miRNA_BCGSC"
Rscript ${BASEDIR}/DESeq2.R ${IN_PATH}/miRNA_counts_miRDeep2.tsv $GROUPS_FILE $EXPR_GROUP $CTRL_GROUP $FC_THRESHOLD $OUT_PATH "miRNA_miRDeep2"
