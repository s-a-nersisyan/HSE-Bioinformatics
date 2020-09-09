PATH_TO_INSTALL=$1

cd $PATH_TO_INSTALL
git clone https://github.com/rajewsky-lab/mirdeep2.git
cd mirdeep2
perl install.pl
source ~/.bashrc
perl install.pl
