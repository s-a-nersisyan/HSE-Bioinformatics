library(edgeR)

argv <- commandArgs(trailingOnly = TRUE)

# Read counts matrix
counts <- read.table(argv[1], sep = "\t", header = TRUE, row.names = "Gene", check.names = FALSE)
gene_lengths <- read.table(argv[2], sep = "\t", header = TRUE, row.names = "Gene")

# Remove low expressed genes and calculate normalization factors
model <- DGEList(counts = counts)
keep <- filterByExpr(model)
model <- model[keep, , keep.lib.sizes = FALSE]
model <- calcNormFactors(model)

m <- match(rownames(model), rownames(gene_lengths))
gene.lengths <- gene_lengths$Length[m]

fpkm <- rpkm(model, gene.lengths)
fpkm <- log2(fpkm + 1)

gene_types = read.table(argv[3], sep = "\t", header = TRUE)
gene_types <- gene_types[, c("Gene", "Type")]
gene_types <- gene_types[!duplicated(gene_types$Gene), ]

fpkm <- merge(fpkm, gene_types, by.x = 0, by.y = "Gene", all.y = FALSE)
colnames(fpkm)[1] <- "Gene"

write.table(fpkm, file = argv[4], sep = "\t", quote = FALSE, row.names = FALSE)
