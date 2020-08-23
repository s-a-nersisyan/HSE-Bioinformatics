import sys
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


miRBase_version = sys.argv[1]

file = open("downloads_{}/hairpin.fa".format(miRBase_version))
pre_miRNA_seq_dict = {}
MI_dict = {}
seq = ""
first_line = True

for line in file:
	line = line.rstrip()

	if line.startswith(">"):
		if first_line == True:
			first_line = False
		else:
			pre_miRNA_seq_dict[pre_miRNA] = seq

		seq = ""
		pre_miRNA = line.lstrip(">").split(" ")[0]
	else:
		seq += line

	if line.startswith(">hsa"):
		MI = line.split(" ")[1]
		MI_dict[pre_miRNA] = MI


file = open("downloads_{}/mature.fa".format(miRBase_version))
MIMAT_dict = {}
for line in file:
	if line.startswith(">hsa"):
		miRNA = line.lstrip(">").split(" ")[0]
		MIMAT = line.split(" ")[1]
		MIMAT_dict[miRNA] = MIMAT


file = open("downloads_{}/miRNA.str".format(miRBase_version))
table = []
for line in file:
	if not line.startswith(">hsa"):
		continue

	pre_miRNA = line.split("(")[0][1:-1]
	for s in line.split("[")[1:]:
		miRNA = s.split(":")[0]
		tmp = s.split(":")[1][:-2]
		start = int(tmp.split("-")[0])
		end = int(tmp.split("-")[1])

		table.append([pre_miRNA, miRNA, start, end])


df = pd.DataFrame(table)
df.columns = ["pre-miRNA", "miRNA", "Start", "End"]

df['MI'] = df['pre-miRNA'].map(MI_dict)
df['MIMAT'] = df['miRNA'].map(MIMAT_dict)
df['Sequence'] = df['pre-miRNA'].map(pre_miRNA_seq_dict)
df = df[["pre-miRNA", "MI", "miRNA", "MIMAT", "Start", "End", "Sequence"]]

df.to_csv("miRBase_{}.tsv".format(miRBase_version), index=None, sep="\t")
