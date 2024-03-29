library(DESeq2)

argv <- commandArgs(trailingOnly = TRUE)

counts <- read.table(argv[1], sep = "\t", header = TRUE, row.names = 1, check.names = FALSE)
groups <- read.table(argv[2], sep = "\t", header = TRUE)
expr_group <- argv[3]
ctrl_group <- argv[4]

groups <- groups[groups$Group %in% c(ctrl_group, expr_group),]
groups$Group <- relevel(factor(groups$Group), ref = ctrl_group)
rownames(groups) <- groups$Sample
groups$Sample <- NULL
counts <- counts[, rownames(groups)]

dds <- DESeqDataSetFromMatrix(countData = counts,
                              colData = groups,
                              design = ~ Group)

dds <- DESeq(dds)

res <- as.data.frame(results(dds))
#res <- as.data.frame(lfcShrink(dds, coef = paste("Group_", expr_group, "_vs_", ctrl_group, sep=""), type = "apeglm"))
res <- res[order(res$padj),]
write.table(res, file = paste(argv[6], "/", argv[7], "_", expr_group, "_vs_", ctrl_group, "_all.tsv", sep=""), sep = "\t", quote = FALSE, col.names = NA)

res <- lfcShrink(dds, coef = paste("Group_", expr_group, "_vs_", ctrl_group, sep=""), type = "apeglm", lfcThreshold = log2(as.numeric(argv[5])))
res <- as.data.frame(subset(res, svalue < 0.005))
res <- res[order(res$svalue),]
write.table(res, file = paste(argv[6], "/", argv[7], "_", expr_group, "_vs_", ctrl_group, "_", argv[5], "_strict.tsv", sep=""), sep = "\t", quote = FALSE, col.names = NA)
