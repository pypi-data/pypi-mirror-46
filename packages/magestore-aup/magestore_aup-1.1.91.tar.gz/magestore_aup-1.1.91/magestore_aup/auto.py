# -*- coding: utf-8 -*-

from datetime import datetime
import json
import getpass
from random import randint
import os
import sys
from fabric import Connection, Config, transfer
from github import Github
from github.GithubException import UnknownObjectException


#################################### General functions ##########################################

def get_absolute_path(relative_path):
    """
    :param relative_path: relative path of the file to the current directory of auto.py file
    :return:
    """
    # current directory path that contain this file
    dir_path = os.path.dirname(os.path.realpath(__file__))
    return "{0}/{1}".format(dir_path, relative_path)


def get_connection(host, user, su_pass='', key_path=''):
    if key_path:
        c = Connection(host, user, connect_kwargs={'key_filename': key_path})
    else:
        config = Config(overrides={'sudo': {'password': su_pass, "prompt": "[sudo] password: \n"}})
        c = Connection(host, user, connect_kwargs={"password": su_pass}, config=config)
    return c


def get_current_time():
    current_time = '{:%H%M%S_%d%m%Y}'.format(datetime.today())
    return current_time


def send_files_to_remote_server(connection, source_path, dest_path):
    """
    :param connection: connection to remote server
    :param source_path: path to file on local server
    :param dest_path: path to folder will be contain file on remote server
    :return: None
    """
    transfer_obj = transfer.Transfer(connection)
    transfer_obj.put(source_path, dest_path)


#################################### Prepare scripts ##########################################


def get_install_prerequisite_path(unique_name):
    raw_install_prerequisite_path = get_absolute_path('data/raw_install_prerequisite.sh')
    install_prerequisite_path = get_absolute_path('data/install_prerequisite_%s.sh' % unique_name)
    local_user = os.environ['USER']

    with open(raw_install_prerequisite_path) as f:
        content = f.read()
        content = content.replace('<username>', local_user)

    with open(install_prerequisite_path, 'w') as f:
        f.write(content)

    return install_prerequisite_path


def get_build_script_path(repo_name, tag_name, github_access_token, instance_info, unique_name):
    """
    :param current_time: this param for create unique folder when build package
    """
    package_file_name = '{tag_name}.tar.gz'.format(tag_name=tag_name)
    raw_build_file_path = get_absolute_path('data/raw_build_package.sh')
    build_file_path = get_absolute_path('data/build_package_%s.sh' % unique_name)

    with open(raw_build_file_path, 'r') as f:
        content = f.read()
        content = content.replace("<access_token>", github_access_token)
        content = content.replace("<repo_name>", repo_name)
        content = content.replace("<package_file_name>", package_file_name)
        content = content.replace("<source_folder>", instance_info.get("source_folder"))
        content = content.replace("<unique_name>", unique_name)

    with open(build_file_path, 'w') as f:
        f.write(content)

    return build_file_path


def get_deploy_script_path(tag_name, instance_info, unique_name):
    package_file_name = '{tag_name}.tar.gz'.format(tag_name=tag_name)
    raw_deploy_file_path = get_absolute_path('data/raw_deploy.sh')
    deploy_file_path = get_absolute_path('data/deploy_%s.sh' % unique_name)

    with open(raw_deploy_file_path, 'r') as f:
        content = f.read()
        content = content.replace("<package_file_name>", package_file_name)
        content = content.replace("<source_folder>", instance_info.get("source_folder"))
        content = content.replace("<web_container_id>", instance_info.get("web_container_id"))
        content = content.replace("<unique_name>", unique_name)

    with open(deploy_file_path, 'w') as f:
        f.write(content)

    return deploy_file_path


################################# Build package (on local machine) #######################################


def install_prerequisite(unique_name):
    local_install_prerequisite_path = get_install_prerequisite_path(unique_name)
    os.system('sudo bash %s > /dev/null' % local_install_prerequisite_path)
    os.system('rm -rf %s' % local_install_prerequisite_path)


def build_package(repo_name, tag_name, github_access_token, instance_info, unique_name):
    local_build_script_path = get_build_script_path(repo_name, tag_name, github_access_token, instance_info,
                                                    unique_name)
    os.system('bash %s > /dev/null' % local_build_script_path)
    os.system('rm -rf %s' % local_build_script_path)


################################# Deploy built package (on remote machine) #######################################

def send_built_package_to_server(connection, tag_name, package_folder):
    package_file_name = '{tag_name}.tar.gz'.format(tag_name=tag_name)
    local_package_file_path = package_folder + '/' + package_file_name
    connection.run('mkdir -p %s' % package_folder, hide='both')
    send_files_to_remote_server(connection, local_package_file_path, package_folder)


def deploy_package_to_remote_server(tag_name, instance_info, unique_name):
    connection = get_connection(
        host=instance_info.get('ip'),
        user=instance_info.get('user'),
        su_pass=instance_info.get('password'),
        key_path=instance_info.get('local_key_file_path')
    )
    package_folder = "/tmp/package-%s" % unique_name
    send_built_package_to_server(connection, tag_name, package_folder)

    local_deploy_file_path = get_deploy_script_path(tag_name, instance_info, unique_name)
    remote_deploy_file_path = '/tmp/demo%s' % local_deploy_file_path
    remote_deploy_folder_path = '/'.join(remote_deploy_file_path.split('/')[:-1])
    connection.run('mkdir -p %s' % remote_deploy_folder_path, hide='both')
    send_files_to_remote_server(connection, local_deploy_file_path, remote_deploy_folder_path)

    connection.run('bash %s > /dev/null' % remote_deploy_file_path, hide='both')
    connection.run('rm -rf %s %s' % (remote_deploy_folder_path, package_folder), hide='both')
    os.system('rm -rf %s %s' % (local_deploy_file_path, package_folder))


def deploy(repo_name, tag_name, github_access_token, instance_info):
    unique_name = get_current_time() + str(randint(1, 100))
    install_prerequisite(unique_name)
    build_package(repo_name, tag_name, github_access_token, instance_info, unique_name)
    deploy_package_to_remote_server(tag_name, instance_info, unique_name)
    return True
