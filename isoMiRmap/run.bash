# This script runs isoMiRmap on all fastq files in given folder
# 1st argument - path with input fastq files
# 2nd argument - folder in which output should be written
# 3nd argument - number of processes
# Example: path_to_this_script.bash /folder/with/fastq/files /output/folder 8

IN_PATH=$1
OUT_PATH=$2
N_PROC=$3

isoMiRmap_path="~/huge/software/isoMiRmap-InitialRelease"

mkdir -p $OUT_PATH
ls -1 $IN_PATH | \
	parallel -j $N_PROC \
	"python3 $isoMiRmap_path/IsoMiRmap.py --m $isoMiRmap_path/MappingBundles/miRBase --p $OUT_PATH/{.} $IN_PATH/{}"
