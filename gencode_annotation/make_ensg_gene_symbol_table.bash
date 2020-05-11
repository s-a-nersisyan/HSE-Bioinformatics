IN_GTF=$1

echo -e "EnsemblID\tGene Symbol\tType"
cat ${IN_GTF} | awk '$3 == "gene"' | cut -f 9 | awk -F '; ' '{print $1"\t"$3"\t"$2}' | \
	sed -e 's/gene_id //g' | sed -e 's/gene_type //g' | sed -e 's/gene_name //g' | sed -e 's/"//g'
