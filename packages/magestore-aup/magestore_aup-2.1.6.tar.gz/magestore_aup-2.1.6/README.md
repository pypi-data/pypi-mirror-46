## Original 
This repo has been moved from [auto_upload_site_package](https://gitlab.com/general-oil/infrastructure/tree/master/Tool/auto_upload_site_package)

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
<ul>
    <li><i>repo_info</i>: (type:dict)
        <ul>
            <li><i>repo_owner</i>: (type:str)</li>
            <li><i>repo_name</i>: (type:str)</li>
            <li><i>tag_name</i>: (type:str)</li>
            <li><i>access_token</i>: (type:str) github personal access token that have permission to acces 6 Magestore product lines</li>
        </ul>
    </li>
    <li><i>instance_info</i>: (type:dict)
        <ul>
            <li><i>ip</i>: (type:str) server ip address</li>
            <li><i>user</i>: (type:str) server username</li>
            <li><i>password</i>: (type:str) server username's password</li>
            <li><i>local_key_file_path</i>: (type:str) path to the private key file on local machine (required when no password provided)</li>
            <li><i>source_folder</i>: (type:str)absolute path to magento source</li>
            <li><i>web_container_id</i>: (type:str) web container id (installed by [magento-apache](https://gitlab.com/general-oil/infrastructure/tree/master/Environment/Magento/DemoPortalApache) docker)</li>
        </ul>
    </li>
</ul>
