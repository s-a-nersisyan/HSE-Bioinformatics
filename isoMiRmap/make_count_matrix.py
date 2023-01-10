from bio import *
import time

IN_PATH = sys.argv[1]  # Folder with the isoMiRmap results
OUT_PATH = sys.argv[2]  # Where the output file should be placed

samples = np.unique([fn.split("-IsoMiRmap")[0] for fn in os.listdir(IN_PATH)])
# TODO: add snps mode
for type_ in ["ambiguous", "exclusive"]:
    dfs = []
    for sample in samples:
        df = rt(f"{IN_PATH}/{sample}-IsoMiRmap_v5-{type_}-isomiRs.expression.txt", i=1, comment="#")
        df = df[[
            "Unnormalized read counts",
            "Mature meta-data (bracket delimited per hairpin)",
            "Hairpin locations (comma delimited)",
            "RepeatMaskerClassIsland where fragment is fully contained (comma delimited)"
        ]]
        df.columns = [sample, "mature", "hairpin", "repeat"]
        
        mature_new = []
        for mature in df["mature"].tolist():
            unique_isomiRs = set()
            for part in mature.split(","):
                part = part.strip(" []")
                if not part.startswith("MIMAT"):
                    continue

                parts = part.split("&")
                isomiR = parts[1] + parts[2][7:]
                unique_isomiRs.add(isomiR)
            
            unique_isomiRs = ", ".join(sorted(list(unique_isomiRs)))
            mature_new.append(unique_isomiRs.strip())
        
        df["mature"] = mature_new

        df = df.fillna("")
        df.index = df.index + ";" + df["mature"] + ";" + df["hairpin"] + ";" + df["repeat"]
        df = df[[sample]]
        dfs.append(df)
    
    df = pd.concat(dfs, axis=1)
    df = df.fillna(0).astype("int64")
    df["mature"] = df.index.str.split(";").str[1]
    df["hairpin"] = df.index.str.split(";").str[2]
    df["repeat"] = df.index.str.split(";").str[3]
    df.index = df.index.str.split(";").str[0]
    df.index.name = "sequence"
    df.to_csv(f"{OUT_PATH}/isoMiRmap_{type_}_counts.tsv", sep="\t")
