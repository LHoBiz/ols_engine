#!/bin/bash
sudo yum update -y
sudo yum install git -y
cd /home/ec2-user
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash ./Miniconda3-latest-Linux-x86_64.sh -b

# conda env export > environment.yml
git clone https://github.com/LHoBiz/ols_engine.git
git checkout aws-linux
sudo chown ec2-user /home/ec2-user/*
sudo rm /home/ec2-user/ols_engine/v0.2/ -rf

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