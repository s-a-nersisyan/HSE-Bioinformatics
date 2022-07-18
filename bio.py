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
from parallelize import Parallelizator

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
