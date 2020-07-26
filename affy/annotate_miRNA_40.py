import sys
import pandas as pd

df1 = pd.read_csv(sys.argv[1], sep="\t", index_col=0).sort_index()  # Raw expression table
df2 = pd.read_csv(sys.argv[2], sep="\t", index_col=1).sort_index()  # GPL annotation table

num_samples = len(df1.columns)

df = df1.join(df2)
df = df.rename(columns={coln: coln.replace(".CEL", "") for coln in df.columns[0:num_samples]})
df = df[df.columns[0:num_samples].to_list() + ["Transcript ID(Array Design)"]]
df = df.rename(columns={"Transcript ID(Array Design)": "miRNA"})

df.to_csv("{}/expression_table.tsv".format(sys.argv[3]), sep="\t")
