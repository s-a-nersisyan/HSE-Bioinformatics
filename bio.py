import sys
import os
import pickle

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import *
from tqdm import tqdm


def rc(path, i=0):
    return pd.read_csv(path, index_col=i)


def rt(path, i=0):
    return pd.read_csv(path, sep="\t", index_col=i)
