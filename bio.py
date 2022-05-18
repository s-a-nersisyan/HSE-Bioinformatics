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


def rc(path, i=0, h="infer"):
    return pd.read_csv(path, index_col=i, header=h)


def rt(path, i=0, h="infer"):
    return pd.read_csv(path, sep="\t", index_col=i, header=h)


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
