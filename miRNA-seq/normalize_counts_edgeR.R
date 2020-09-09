library(edgeR)

argv <- commandArgs(trailingOnly = TRUE)

# Read counts matrix
counts <- read.table(argv[1], sep = "\t", header = TRUE, row.names = 1, check.names = FALSE)

# Remove low expressed genes and calculate normalization factors
model <- DGEList(counts = counts)
keep <- filterByExpr(model)
model <- model[keep, , keep.lib.sizes = FALSE]
model <- calcNormFactors(model)

cpm <- log2(cpm(model) + 1)

write.table(cpm, file = argv[2], sep = "\t", quote = FALSE, col.names = NA)
