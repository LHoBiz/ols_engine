#!/bin/bash

# from https://docs.geoserver.org/latest/en/user/installation/linux.html
sudo amazon-linux-extras install java-openjdk11 -y

cd ~
sudo wget https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.67/bin/apache-tomcat-9.0.67.tar.gz
sudo tar xvzf apache-tomcat-9.0.67.tar.gz
sudo mv apache-tomcat-9.0.67 tomcat9
sudo echo "export CATALINA_HOME="/home/ec2-user/tomcat9"" >> ~/.bashrc
sudo source ~/.bashrc
# sudo chown -R ec2-user ~/*
sudo cp ~/ols_engine/tomcat9/conf/server.xml ~/tomcat9/conf/server.xml 
sudo cp ~/ols_engine/tomcat9/conf/tomcat-users.xml ~/tomcat9/conf/tomcat-users.xml 



sudo wget http://sourceforge.net/projects/geoserver/files/GeoServer/2.5.2/geoserver-2.5.2-war.zip
sudo unzip geoserver-2.5.2-war.zip *.war
sudo cp geoserver.war ~/tomcat9/webapps/
sudo ~/tomcat9/bin/startup.sh

# sudo rm -rf /usr/share/geoserver
# sudo mkdir /usr/share/geoserver
# cd /usr/share/geoserver
# sudo wget https://ixpeering.dl.sourceforge.net/project/geoserver/GeoServer/2.21.1/geoserver-2.21.1-bin.zip 
# sudo unzip geoserver-2.21.1-bin.zip
# echo "export GEOSERVER_HOME=/usr/share/geoserver" >> ~/.profile
# . ~/.profile
# sudo chown -R ec2-user /usr/share/geoserver/
# sh ./bin/startup.sh