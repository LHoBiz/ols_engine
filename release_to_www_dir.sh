#!/bin/bash
git pull
rm -rf /usr/share/tomcat9/webapps/ols_engine/src
rm -f /usr/share/tomcat9/webapps/ols_engine/index.html

mkdir -p /usr/share/tomcat9/webapps/ols_engine/src
cd /usr/share/ols_engine
cp ./src/* /usr/share/tomcat9/webapps/ols_engine/src/
cp ./index.html /usr/share/tomcat9/webapps/ols_engine/
