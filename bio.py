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
