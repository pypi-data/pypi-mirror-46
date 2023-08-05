## Prepare
Config visudo (run sudo without password) on local machine
```bash
sudo visudo
# add this line to end of file
# username is your current username
username  ALL=(ALL) NOPASSWD: ALL
```

## How to use

This package provided function name **deploy**, it will update Magestore pwa pos package to any remote server.  
The **deploy** function has required params:
+ *repo_name*: the name of repo that will be upload to remote server
+ *tag_name*: released package tag name
+ *github_access_token*: github personal access token that have permission to access the repo *repo_name*
+ *instance_info*: dict contains all remote server info (all required , except *web_container_id* only required when instance installed by [magento-apache](https://gitlab.com/general-oil/infrastructure/tree/master/Environment/Magento/DemoPortalApache) docker)
  + ip: server ip address
  + user: server username
  + password: username's password
  + local_key_file_path: path to private key file on local machine
  + source_folder: absolute path to magento source
  + web_container_id: web container id (installed by [magento-apache](https://gitlab.com/general-oil/infrastructure/tree/master/Environment/Magento/DemoPortalApache) docker)
