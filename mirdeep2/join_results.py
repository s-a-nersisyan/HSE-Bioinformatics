import sys
import os
from natsort import natsorted
import pandas as pd


in_path = sys.argv[1]
out_path = sys.argv[2]

dfs = []
for fn in natsorted(os.listdir(in_path)):
    if not fn.endswith(".tsv"):
        continue

    df = pd.read_csv("{}/{}".format(in_path, fn), sep="\t")
    df["miRNA"] = df["#miRNA"]
    df = df[["miRNA", "read_count"]].set_index("miRNA")
    df.columns = [fn.rstrip(".tsv")]
    dfs.append(df)

df = pd.concat(dfs, axis=1)
df = df.loc[df.median(axis=1).sort_values(ascending=False).index]
df = df.loc[~df.index.duplicated()].astype(int)
df.to_csv("{}/miRNA_counts_miRDeep2.tsv".format(out_path), sep="\t")
