import sys
import os
import pickle

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import *
from tqdm import tqdm
from pprint import pprint
from natsort import natsorted
from multiprocessing import Pool

import plots


TCGA_PATH = "/home/steve/huge/bulk/TCGA/update"


def rc(path, *args, i=0, h="infer", **kwargs):
    return pd.read_csv(path, *args, index_col=i, header=h, **kwargs)


def rt(path, *args, i=0, h="infer", **kwargs):
    return pd.read_csv(path, *args, sep="\t", index_col=i, header=h, **kwargs)


def fdr(p_values):
    return p_values * len(p_values) / rankdata(p_values)


def loc(df, index, return_in=False):
    if return_in:
        return df.loc[set(df.index)&set(index)], set(df.index)&set(index)

    return df.loc[set(df.index)&set(index)]


def col(df, cols, return_in=False):
    if return_in:
        return df[set(df.columns)&set(cols)], set(df.columns)&set(cols)

    return df[set(df.columns)&set(cols)]


def parallelize(func, args_list, n_processes, multiple_args=False):
    args_chunks = np.array_split(args_list, n_processes)
    
    def process_chunk(args_chunk):
        results = []
        for arg in args_chunk:
            results.append(func(*arg if multiple_args else arg))
            
        return results
    
    with Pool(n_processes) as p:
        if multiple_args:
            results = p.starmap(
                process_chunk,
                args_chunks,
            )
        else:
            results = p.map(
                process_chunk,
                args_chunks,
            )
        
    return results


"""
TCGA functions
"""

def tcga_load_isoMiRmap(project, dtype="exclusive_log2_FPM_DESeq2", sample_type="any"):
    types_mapping = {
        "pt": "Primary Tumor",
        "stn": "Solid Tissue Normal",
        "m": "Metastatic"
    }
    df = pd.read_pickle(f"{TCGA_PATH}/{project}/isoMiRmap_{dtype}.pkl")
    if sample_type == "any":
        return df

    ann = rt(f"{TCGA_PATH}/samples_annotation.tsv")
    ann["Sample ID"] = ann["Sample ID"].str[:-1]
    ann = ann.loc[ann["Sample Type"] == types_mapping[sample_type]]

    return df[df.columns[:3].tolist() + [c for c in df.columns if c in ann["Sample ID"].tolist()]]


def tcga_load_RSEM_transcript(project, dtype="log2_FPKM_DESeq2", sample_type="any"):
    types_mapping = {
        "pt": "Primary Tumor",
        "stn": "Solid Tissue Normal",
        "m": "Metastatic"
    }
    df = pd.read_pickle(f"{TCGA_PATH}/{project}/RSEM_transcript_{dtype}.pkl")
    if sample_type == "any":
        return df

    ann = rt(f"{TCGA_PATH}/samples_annotation.tsv")
    ann["Sample ID"] = ann["Sample ID"].str[:-1]
    ann = ann.loc[ann["Sample Type"] == types_mapping[sample_type]]

    return df[df.columns[:1].tolist() + [c for c in df.columns if c in ann["Sample ID"].tolist()]]


def tcga_match_samples(df1, df2):
    tech_cols1 = [c for c in df1.columns if not c.startswith("TCGA")]
    tech_cols2 = [c for c in df2.columns if not c.startswith("TCGA")]
    common_samples = sorted(list(set(df1.columns) & set(df2.columns)))
    return df1[tech_cols1 + common_samples], df2[tech_cols2 + common_samples]


def tcga_top_n_expressed(df, n):
    samples = [c for c in df.columns if c.startswith("TCGA")]
    df = df.loc[df[samples].median(axis=1).sort_values(ascending=False).iloc[:n].index]
    return df
