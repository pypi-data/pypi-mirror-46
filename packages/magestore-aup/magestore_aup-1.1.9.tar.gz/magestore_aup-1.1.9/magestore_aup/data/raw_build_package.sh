#!/usr/bin/env bash


package_file_name="<package_file_name>"
repo_owner="Magestore"
repo_name="<repo_name>"
access_token="<access_token>"
unique_name="<unique_name>"
package_folder="/tmp/package-$unique_name"
source_folder="<source_folder>"

#************************ Downloading package ************************

rm -rf $package_folder/*
mkdir -p $package_folder
curl -s -H 'Authorization: token '"$access_token"'' -H 'Accept: application/vnd.github.v3.raw' -Lo  $package_folder/$package_file_name https://github.com/$repo_owner/$repo_name/archive/$package_file_name
cd $package_folder && tar -xf $package_file_name

#************************* Building package **************************

cd $package_folder && cd pos*/client/pos
npm install > /dev/null 2>&1
npm run-script build > /dev/null 2>&1

#************************* Packing package **************************

cd $package_folder
rm -rf *.tar.gz
tar --exclude='./pos*/client/pos/node_modules' --exclude='./pos*/client/pos/public' --exclude='./pos*/client/pos/src' -cf $package_file_name pos*