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
df.columns = ["pre-miRNA", "miRNA", "Local start", "Local end"]

df['MI'] = df['pre-miRNA'].map(MI_dict)
df['MIMAT'] = df['miRNA'].map(MIMAT_dict)
df['Sequence'] = df['pre-miRNA'].map(pre_miRNA_seq_dict)

df["Chr"] = None
df["Strand"] = None
df["Start"] = None
df["End"] = None

df = df[["pre-miRNA", "MI", "miRNA", "MIMAT", "Chr", "Strand", "Start", "End", "Sequence", "Local start", "Local end"]]

file = open("downloads_{}/hsa.gff3".format(miRBase_version))
#table = []
for line in file:
    if line.startswith("#") or "miRNA_primary_transcript" in line.split("\t")[2]:
        continue
    
    miRNA = line.split("\t")[-1].split(";")[2].lstrip("Name=")
    MI = line.split("\t")[-1].split(";")[-1].lstrip("Derives_from=").rstrip()
    
    df.loc[(df["MI"] == MI) & (df["miRNA"] == miRNA), "Chr"] = line.split("\t")[0]
    df.loc[(df["MI"] == MI) & (df["miRNA"] == miRNA), "Strand"] = line.split("\t")[6]
    df.loc[(df["MI"] == MI) & (df["miRNA"] == miRNA), "Start"] = int(line.split("\t")[3])
    df.loc[(df["MI"] == MI) & (df["miRNA"] == miRNA), "End"] = int(line.split("\t")[4])

df.to_csv("miRBase_{}.tsv".format(miRBase_version), index=None, sep="\t")
