#!/usr/bin/env bash


package_file_name="<package_file_name>"
unique_name="<unique_name>"
package_folder="/tmp/package-$unique_name"
source_folder="<source_folder>"
web_container_id="<web_container_id>"

#************************* Extract package **************************
cd $package_folder
tar -xf $package_file_name


#************************* Install package **************************

# copy backend module to source
magestore_extension_folder="$source_folder/app/code/Magestore"
# do we need to delete old extensions and replace them with new version ?
mkdir -p $magestore_extension_folder
yes | cp -r $package_folder/pos*/server/app/code/Magestore/* $magestore_extension_folder

# copy built package to app/pos
mkdir -p $source_folder/app/code/Magestore/Webpos/build/apps/
yes | cp -rf $package_folder/pos*/client/pos/build $source_folder/app/code/Magestore/Webpos/build/apps/pos
rm -rf $package_folder

if [ -z "$web_container_id" ]; then
    # magento running on normal server
    cd $source_folder
    php bin/magento setup:upgrade
    php bin/magento setup:di:compile
    php bin/magento setup:static-content:deploy -f
    php bin/magento indexer:reindex
    php bin/magento webpos:deploy
    php bin/magento cache:flush
else
    # magento running on docker engine
    docker exec -u www-data -i $web_container_id php bin/magento setup:upgrade
    docker exec -u www-data -i $web_container_id php bin/magento setup:di:compile
    docker exec -u www-data -i $web_container_id php bin/magento setup:static-content:deploy -f
    docker exec -u www-data -i $web_container_id php bin/magento indexer:reindex
    docker exec -u www-data -i $web_container_id php bin/magento webpos:deploy
    docker exec -u www-data -i $web_container_id php bin/magento cache:flush
fi
