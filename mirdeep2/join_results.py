import sys
import os
import pandas as pd


in_path = sys.argv[1]
out_path = sys.argv[2]

dfs = []
for fn in os.listdir(in_path):
    if not fn.endswith(".tsv"):
        continue

    df = pd.read_csv("{}/{}".format(in_path, fn), sep="\t")
    df["miRNA"] = df[["precursor", "#miRNA"]].agg(".".join, axis=1)
    df = df[["miRNA", "read_count"]].set_index("miRNA")
    df.columns = [fn.rstrip(".tsv")]
    dfs.append(df)

df = pd.concat(dfs, axis=1)
df = df.loc[~df.index.duplicated()]
df.to_csv("{}/miRNA_expression.tsv".format(out_path), sep="\t")
