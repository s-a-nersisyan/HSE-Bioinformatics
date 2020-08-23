miRBase_version=$1

mkdir -p downloads_${miRBase_version}
cd downloads_${miRBase_version}

wget ftp://mirbase.org/pub/mirbase/${miRBase_version}/miRNA.str.zip
wget ftp://mirbase.org/pub/mirbase/${miRBase_version}/mature.fa.zip
wget ftp://mirbase.org/pub/mirbase/${miRBase_version}/hairpin.fa.zip
wget ftp://mirbase.org/pub/mirbase/${miRBase_version}/genomes/hsa.gff3

unzip \*.zip
rm *.zip
cd ..

python3 make_table.py ${miRBase_version}
