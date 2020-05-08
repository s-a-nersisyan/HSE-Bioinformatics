library(affy)

argv = commandArgs(trailingOnly=TRUE)

d = ReadAffy(celfile.path=argv[1])

eset <- rma(d)
write.exprs(eset, file=paste(argv[2], "/rma_normalized.tsv", sep=""), sep="\t")
