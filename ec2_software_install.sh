#!/bin/bash
yum update -y
yum install git -y
cd /usr/share/


# conda env export > environment.yml
git clone -b aws-linux https://github.com/LHoBiz/ols_engine.git 
rm ./ols_engine/v0.2/ -rf


amazon-linux-extras install java-openjdk11 -y

wget https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.68/bin/apache-tomcat-9.0.68.tar.gz
tar xvzf apache-tomcat-9.0.68.tar.gz
mv apache-tomcat-9.0.68 tomcat9
echo "export CATALINA_HOME="/usr/share/tomcat9"" >> ~/.bashrc
source ~/.bashrc

\cp ./ols_engine/tomcat9/conf/server.xml ./tomcat9/conf/server.xml 
\cp ./ols_engine/tomcat9/conf/tomcat-users.xml ./tomcat9/conf/tomcat-users.xml 


wget https://ixpeering.dl.sourceforge.net/project/geoserver/GeoServer/2.21.1/geoserver-2.21.1-war.zip 
mv geoserver-2.21.1-war.zip  geoserver.zip
unzip ./geoserver.zip *.war
cp geoserver.war ./tomcat9/webapps/
echo "export GEOSERVER_HOME=/usr/share/geoserver" >> ~/.profile
./tomcat9/bin/startup.sh

wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
sh ./Miniconda3-latest-Linux-x86_64.sh -b

cd cd /usr/share/ols_engine
rm -rf /usr/share/tomcat9/webapps/ols_engine/src
rm -f /usr/share/tomcat9/webapps/ols_engine/index.html

mkdir -p /usr/share/tomcat9/webapps/ols_engine/src
cd /usr/share/ols_engine
cp /usr/share/ols_engine/src/* /usr/share/tomcat9/webapps/ols_engine/src/
cp /usr/share/ols_engine/index.html /usr/share/tomcat9/webapps/ols_engine/


export DJANGO_SUPERUSER_PASSWORD=d1j1kdhHj29ajafe
export DJANGO_SUPERUSER_USERNAME=admin
export DJANGO_SUPERUSER_EMAIL=magiva_aussie@hotmail.com