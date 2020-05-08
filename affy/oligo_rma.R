library(oligo)

argv = commandArgs(trailingOnly=TRUE)

celFiles <- list.celfiles(argv[1], full.names=TRUE)
rawData <- read.celfiles(celFiles)
eset <- rma(rawData)
write.exprs(eset, file=paste(argv[2], "/rma_normalized.tsv", sep=""), sep="\t")
