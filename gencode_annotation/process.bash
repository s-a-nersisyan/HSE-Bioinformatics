IN_GTF=$1
OUT_PREFIX=$2

# EnsemblID -> Gene Symbol
echo -e "EnsemblID\tGene\tType" > ${OUT_PREFIX}.types.tsv
cat ${IN_GTF} | awk '$3 == "gene"' | cut -f 9 | awk -F '; ' '{print $1"\t"$3"\t"$2}' | \
	sed -e 's/gene_id //g' | sed -e 's/gene_type //g' | sed -e 's/gene_name //g' | sed -e 's/"//g' >> ${OUT_PREFIX}.types.tsv

## Calculate gene lengths
## Don't forget to rename MT to M in GTFtools!!!
/home/steve/huge/software/GTFtools_0.6.9/gtftools.py -c 1-22,X,Y,M -l ${OUT_PREFIX}.lengths.tmp.tsv ${IN_GTF}
# EnsemblID -> Gene Symbol
python3 -c "
import pandas as pd
import sys
df1 = pd.read_csv(sys.argv[1], sep='\t', index_col=0)
df2 = pd.read_csv(sys.argv[2], sep='\t', index_col=0)
df = df1.join(df2)[['Gene', 'merged']].drop_duplicates('Gene').set_index('Gene')
df = df.rename(columns={'merged': 'Length'})
df.to_csv(sys.argv[3], sep='\t')
" ${OUT_PREFIX}.lengths.tmp.tsv ${OUT_PREFIX}.types.tsv ${OUT_PREFIX}.lengths.tsv

rm "${IN_GTF}.ensembl"
rm ${OUT_PREFIX}.lengths.tmp.tsv
