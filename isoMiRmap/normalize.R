library(DESeq2)

argv <- commandArgs(trailingOnly = TRUE)
IN_PATH = argv[1]
OUT_PATH = argv[2]

for (type in c("ambiguous", "exclusive")) {
	df <- read.table(
		paste(IN_PATH, "/isoMiRmap_", type, "_counts.tsv", sep=""),
		sep = "\t", header = TRUE, row.names = 1, check.names = FALSE
	)
	counts <- df[, 1:(ncol(df) - 3)]

	groups <- data.frame(something = rep("x", ncol(counts)))  # "x" is arbitrary
	rownames(groups) = colnames(counts)

	dds <- DESeqDataSetFromMatrix(countData = counts, colData = groups, design = ~ 1)
	dds <- estimateSizeFactors(dds)

	normalized_counts <- fpm(dds, robust = TRUE)
	df[, 1:(ncol(df) - 3)] <- log2(normalized_counts + 1)

	write.table(
		df, file = paste(OUT_PATH, "/isoMiRmap_", type, "_log2_RPM_DESeq2.tsv", sep=""),
		sep = "\t", quote = FALSE, col.names = NA
	)
}
