PATH_TO_INSTALL=$1

cd /tmp
mkdir miRBase_sql
cd miRBase_sql
wget ftp://mirbase.org/pub/mirbase/CURRENT/database_files/*
gunzip *.gz

mysql --user="bcgsc_mirna" --password="uglytool" --database="mirbase" < tables.sql
for fname in *.txt; do
	name="${fname%.*}"
	mysql --user="bcgsc_mirna" --password="uglytool" --database="mirbase" --execute="load data local infile '$fname' into table $name"
done
cd ..
rm -rf miRBase_sql

cd $PATH_TO_INSTALL
git clone https://github.com/bcgsc/mirna.git
mv mirna bcgsc_mirna
echo "mirbase localhost bcgsc_mirna uglytool" >> bcgsc_mirna/config/db_connections.cfg
