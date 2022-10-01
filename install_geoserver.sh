#!/bin/bash

# from https://docs.geoserver.org/latest/en/user/installation/linux.html
sudo amazon-linux-extras install java-openjdk11
sudo mkdir /usr/share/geoserver
wget https://ixpeering.dl.sourceforge.net/project/geoserver/GeoServer/2.21.1/geoserver-2.21.1-bin.zip -P /usr/share/geoserver -y
echo "export GEOSERVER_HOME=/usr/share/geoserver" >> ~/.profile
. ~/.profile
sudo chown -R ec2-user /usr/share/geoserver/
sh /usr/share/geoserver/bin/startup.sh