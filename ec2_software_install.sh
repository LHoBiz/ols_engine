#!/bin/bash
sudo yum update -y
sudo yum install git -y
cd /usr/share/


# conda env export > environment.yml
git clone https://github.com/LHoBiz/ols_engine.git
git fetch
git checkout aws-linux
sudo chown -R ec2-user /home/ec2-user/*
sudo rm /home/ec2-user/ols_engine/v0.2/ -rf


sudo amazon-linux-extras install java-openjdk11 -y

sudo wget https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.67/bin/apache-tomcat-9.0.67.tar.gz
sudo tar xvzf apache-tomcat-9.0.67.tar.gz
sudo mv apache-tomcat-9.0.67 tomcat9
echo "export CATALINA_HOME="/usr/share/tomcat9"" >> ~/.bashrc
source ~/.bashrc

sudo cp ./ols_engine/tomcat9/conf/server.xml ./tomcat9/conf/server.xml 
sudo cp ./ols_engine/tomcat9/conf/tomcat-users.xml ./tomcat9/conf/tomcat-users.xml 


sudo wget https://ixpeering.dl.sourceforge.net/project/geoserver/GeoServer/2.21.1/geoserver-2.21.1-war.zip 
sudo mv geoserver-2.21.1-war.zip  geoserver.zip
sudo unzip ./geoserver.zip *.war
sudo cp geoserver.war ./tomcat9/webapps/
echo "export GEOSERVER_HOME=/usr/share/geoserver" >> ~/.profile
sudo ./tomcat9/bin/startup.sh