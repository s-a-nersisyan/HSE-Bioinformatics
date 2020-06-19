import sys
import pandas as pd

df1 = pd.read_csv(sys.argv[1], sep="\t", index_col=0).sort_index()  # Raw expression table
df2 = pd.read_csv(sys.argv[2], sep="\t", index_col=0).sort_index()  # GPL annotation table

df = df1.join(df2)

df.to_csv("{}/expression_table.tsv".format(sys.argv[3]), sep="\t")
