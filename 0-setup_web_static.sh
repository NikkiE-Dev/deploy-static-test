#!/usr/bin/env bash
# Making server to deploy

#Updating/upgrading server
sudo apt-get -y update 
sudo apt-get -y upgrade 

#Installing nginx
sudo apt-get -y install nginx
sudo service nginx start

#Making directories
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

#Creating file and writing cntent in file
sudo echo "This file is so fake" | sudo tee /data/web_static/releases/test/index.html
sudo ln -sfn /data/web_static/releases/test/ /data/web_static/current

#Giving ownership to specific user
sudo chown ubuntu:ubuntu -hR /data

#Edit nginx config file
search="^\tlocation / {"
replace="\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}\n\n\tlocation / {"
sudo sed -i "s@${search}@${replace}@" /etc/nginx/sites-available/default

sudo service nginx restart

exit 0