#!/bin/bash

# from https://docs.geoserver.org/latest/en/user/installation/linux.html
sudo amazon-linux-extras install java-openjdk11
cd ~
wget http://sourceforge.net/projects/geoserver/files/GeoServer/2.5.2/geoserver-2.5.2-war.zip
sudo unzip geoserver-2.5.2-war.zip *.war –d /var/www/html/

# sudo rm -rf /usr/share/tomcat
# sudo mkdir /usr/share/tomcat
# cd /usr/share/tomcat
# sudo wget https://dlcdn.apache.org/tomcat/tomcat-10/v10.0.26/bin/apache-tomcat-10.0.26.tar.gz
# sudo tar xvzf apache-tomcat-10.0.26.tar.gz

# cd apache-tomcat-10.0.26
# ./configure
# make
# sudo make install

# sudo rm -rf /usr/share/geoserver
# sudo mkdir /usr/share/geoserver
# cd /usr/share/geoserver
# sudo wget https://ixpeering.dl.sourceforge.net/project/geoserver/GeoServer/2.21.1/geoserver-2.21.1-bin.zip 
# sudo unzip geoserver-2.21.1-bin.zip
# echo "export GEOSERVER_HOME=/usr/share/geoserver" >> ~/.profile
# . ~/.profile
# sudo chown -R ec2-user /usr/share/geoserver/
# sh ./bin/startup.sh