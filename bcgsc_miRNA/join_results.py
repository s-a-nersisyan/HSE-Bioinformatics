import sys
import os
from natsort import natsorted

import pandas as pd
import numpy as np


BCGSC_path = sys.argv[1]
miRBase_path = sys.argv[2]
out_path = sys.argv[3]

df_miRBase = pd.read_csv(miRBase_path, sep="\t", index_col=3)
MIMAT_miRNA = df_miRBase[["miRNA"]].drop_duplicates()

dfs_isomiR_full = []
dfs_isomiR_5prime = []
dfs_miRNA = []
for sample in natsorted(os.listdir(BCGSC_path)):
    if not sample.endswith("_features"):
        continue

    file_path = "{}/{}/tcga/isoforms.txt".format(BCGSC_path, sample)
    sample = sample.lstrip("pool_").rstrip("_features")
    
    df_BCGSC = pd.read_csv(file_path, sep="\t")
    df_BCGSC["MIMAT"] = [m.replace("mature,", "") if "MIMAT" in m else None for m in df_BCGSC["miRNA_region"]]
    df_BCGSC = df_BCGSC.loc[~df_BCGSC["MIMAT"].isna()].set_index("MIMAT")
    
    coords = df_BCGSC["isoform_coords"].str.split(":", expand=True)
    df_BCGSC["Chr"] = coords[1]
    df_BCGSC["Strand"] = coords[3]
    df_BCGSC["Start"] = coords[2].str.split("-", expand=True)[0].astype(int)
    df_BCGSC["End"] = coords[2].str.split("-", expand=True)[1].astype(int)

    df_BCGSC = df_BCGSC.join(df_miRBase, how="outer", rsuffix="_miRBase")
    df_BCGSC = df_BCGSC.loc[df_BCGSC["Chr"] == df_BCGSC["Chr_miRBase"]]
    df_BCGSC = df_BCGSC.loc[df_BCGSC["Strand"] == df_BCGSC["Strand_miRBase"]]
    df_BCGSC = df_BCGSC.loc[df_BCGSC["pre-miRNA"] == df_BCGSC["miRNA_ID"]]

    df_BCGSC["Offset 5'"] = [
        row["Start"] - row["Start_miRBase"] if row["Strand"] == "+" else row["End_miRBase"] - row["End"]
        for MIMAT, row in df_BCGSC.iterrows()
    ]
    df_BCGSC["Offset 3'"] = [
        row["End"] - row["End_miRBase"] if row["Strand"] == "+" else row["Start_miRBase"] - row["Start"]
        for MIMAT, row in df_BCGSC.iterrows()
    ]
    df_BCGSC = df_BCGSC.loc[np.abs(df_BCGSC["Offset 5'"]) <= 6]
    df_BCGSC = df_BCGSC.loc[np.abs(df_BCGSC["Offset 3'"]) <= 6]

    df_BCGSC["isomiR"] = [
        "{}|{}{}|{}{}".format(
            row["miRNA"],
            "+" if row["Offset 5'"] > 0 else "", int(row["Offset 5'"]),
            "+" if row["Offset 3'"] > 0 else "", int(row["Offset 3'"]),
        )
        for MIMAT, row in df_BCGSC.iterrows()
    ]
    df_isomiR_full = df_BCGSC[["isomiR", "read_count"]].groupby("isomiR").sum()
    df_isomiR_full.columns = [sample]

    df_isomiR_5prime = df_isomiR_full.reset_index()
    df_isomiR_5prime["isomiR"] = ["|".join(isomiR.split("|")[0:2]) for isomiR in df_isomiR_5prime["isomiR"]]
    df_isomiR_5prime = df_isomiR_5prime.groupby("isomiR").sum()
    
    df_miRNA = df_isomiR_full.reset_index()
    df_miRNA["isomiR"] = [isomiR.split("|")[0] for isomiR in df_miRNA["isomiR"]]
    df_miRNA = df_miRNA.groupby("isomiR").sum()
    df_miRNA.index.name = "miRNA"

    dfs_isomiR_full.append(df_isomiR_full)
    dfs_isomiR_5prime.append(df_isomiR_5prime)
    dfs_miRNA.append(df_miRNA)

df_isomiR_full = pd.concat(dfs_isomiR_full, axis=1).sort_index().fillna(0).astype(int)
df_isomiR_5prime = pd.concat(dfs_isomiR_5prime, axis=1).sort_index().fillna(0).astype(int)
df_miRNA = pd.concat(dfs_miRNA, axis=1).sort_index().fillna(0).astype(int)

df_isomiR_full.to_csv("{}/isomiR_counts.tsv".format(out_path), sep="\t")
df_isomiR_5prime.to_csv("{}/isomiR_5prime_counts.tsv".format(out_path), sep="\t")
df_miRNA.to_csv("{}/miRNA_counts_BCGSC.tsv".format(out_path), sep="\t")
