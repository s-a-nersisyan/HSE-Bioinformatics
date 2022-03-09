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
