#!/bin/bash
sudo yum update -y
sudo yum install git -y
cd /home/ec2-user
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash ./Miniconda3-latest-Linux-x86_64.sh -b
# /miniconda3/bin/conda init
# source ~/.bashrc
# conda create -n "ols_engine" python=3.8 gdal -y
# source ~/.bashrc
# conda activate ols_engine
# source ~/.bashrc
# conda install gdal=3.3.x django -y && conda install -c conda-forge postgresql -y && conda install -c conda-forge/label/gcc7 postgresql -y && conda install -c conda-forge/label/broken postgresql -y && conda install -c conda-forge/label/cf201901 postgresql -y && conda install -c conda-forge/label/cf202003 postgresql -y

# conda env export > environment.yml
git clone https://github.com/LHoBiz/ols_engine.git
git checkout aws-linux

amazon-linux-extras install -y lamp-mariadb10.2-php7.2 php7.2
yum install -y httpd mariadb-server
systemctl start httpd
systemctl enable httpd
usermod -a -G apache ec2-user
chown -R ec2-user:apache /var/www
chmod 2775 /var/www
find /var/www -type d -exec chmod 2775 {} \;
find /var/www -type f -exec chmod 0664 {} \;
echo "<?php phpinfo(); ?>" > /var/www/html/phpinfo.php