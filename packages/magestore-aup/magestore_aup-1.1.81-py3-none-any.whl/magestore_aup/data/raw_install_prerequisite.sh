#!/usr/bin/env bash

if dpkg-query -W npm > /dev/null 2>&1; then
    exit 0
else
    #**************************** Install npm ****************************"
    sudo apt-get install curl -y
    curl -sL https://deb.nodesource.com/setup_10.x | sudo bash -
    sudo apt-get install nodejs -y
    echo sudo chown -R <username>:<username> ~/.npm
fi
