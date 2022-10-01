#!/bin/bash

# from https://docs.geoserver.org/latest/en/user/installation/linux.html
sudo amazon-linux-extras install java-openjdk11
cd ~
sudo rm -rf /usr/share/geoserver
sudo mkdir /usr/share/geoserver
cd /usr/share/geoserver
sudo wget https://ixpeering.dl.sourceforge.net/project/geoserver/GeoServer/2.21.1/geoserver-2.21.1-bin.zip 
sudo unzip geoserver-2.21.1-bin.zip
echo "export GEOSERVER_HOME=/usr/share/geoserver" >> ~/.profile
. ~/.profile
sudo chown -R ec2-user /usr/share/geoserver/
sh ./bin/startup.sh