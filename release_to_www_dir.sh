#!/bin/bash
git pull
rm -rf /var/www/html/src
rm -f /var/www/html/index.html

mkdir /var/www/html/src/
cp ~/ols_engine/src/* /var/www/html/src/
cp ~/ols_engine/index.html /var/www/html
