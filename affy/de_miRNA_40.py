import sys

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, rankdata

import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv(sys.argv[1], sep="\t", index_col=0)

group1_name = "CD24 knockdown"
group1_cols = ["CD24_kd1", "CD24_kd1", "CD24_kd3"]
group2_name = "Control"
group2_cols = ["ctrl1", "ctrl2", "ctrl3"]

noise_quantile = 0.75
FC_threshold = np.log2(1.5)

# First, preserve human mature miRNAs
df = df.loc[(df.index.str.contains("MIMAT")) & (df["miRNA"].str.contains("hsa-"))]
df = df[group1_cols + group2_cols + ["miRNA"]]

maximums = df[group1_cols + group2_cols].max(axis=1)
df = df.loc[maximums.sort_values(ascending=False).index]

# Remove low-expressed miRNAs
df = df.loc[maximums >= maximums.quantile(noise_quantile)]

# Calculate means and fold changes
df[group1_name + ", mean"] = df[group1_cols].mean(axis=1)
df[group2_name + ", mean"] = df[group2_cols].mean(axis=1)
df["log2(FC)"] = df[group1_name + ", mean"] - df[group2_name + ", mean"]
df = df.loc[np.abs(df["log2(FC)"]) >= FC_threshold]

# Calculate and adjust p-values
df["p-value"] = ttest_ind(df[group1_cols], df[group2_cols], axis=1).pvalue
df["FDR"] = df["p-value"] * len(df) / rankdata(df["p-value"])
df = df.loc[df["FDR"] < 0.05]
df = df.sort_values("FDR")

df = df[["miRNA", group1_name + ", mean", group2_name + ", mean", "log2(FC)", "p-value", "FDR"]]

print(df)
