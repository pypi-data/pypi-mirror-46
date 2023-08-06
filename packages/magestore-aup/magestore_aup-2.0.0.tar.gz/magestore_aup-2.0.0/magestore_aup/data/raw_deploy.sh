#!/usr/bin/env bash


repo_name="<repo_name>"
repo_owner="<repo_owner>"
tag_name="<tag_name>"
access_token="<access_token>"
package_file_name="${repo_name}-${tag_name}.tar.gz"
unique_str="<unique_str>"
package_folder="/tmp/${unique_str}-package"
source_folder="<source_folder>"
web_container_id="<web_container_id>"

# **************************** Download built package ***************************
mkdir -p ${package_folder}
curl -s -H 'Authorization: token '"${access_token}"'' -H 'Accept: application/vnd.github.v3.raw' \
     -Lo  ${package_folder}/${package_file_name} \
      https://github.com/Magestore/go-built-packages/releases/download/${tag_name}/${package_file_name}


# **************************** Extract package **************************
cd ${package_folder}
tar -xf ${package_file_name}


# **************************** Install package **************************

yes | cp -rf ${package_folder}/server/app/code/Magestore/* ${source_folder}/app/code/Magestore/
rm -rf ${package_folder}

if [-z "${web_container_id}"]; then
    # magento running on normal server
    cd ${source_folder}
    php bin/magento setup:upgrade
    php bin/magento setup:di:compile
    php bin/magento setup:static-content:deploy -f
    php bin/magento indexer:reindex
    php bin/magento webpos:deploy
    php bin/magento cache:flush
else
    # magento running on docker engine
    docker exec -u www-data -i ${web_container_id} php bin/magento setup:upgrade
    docker exec -u www-data -i ${web_container_id} php bin/magento setup:di:compile
    docker exec -u www-data -i ${web_container_id} php bin/magento setup:static-content:deploy -f
    docker exec -u www-data -i ${web_container_id} php bin/magento indexer:reindex
    docker exec -u www-data -i ${web_container_id} php bin/magento webpos:deploy
    docker exec -u www-data -i ${web_container_id} php bin/magento cache:flush
fi
