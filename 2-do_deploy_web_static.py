#!/usr/bin/python3
"""Compress web static package
"""
from fabric.api import *
from datetime import datetime
from os import path


env.hosts = ['18.210.33.153', '54.236.27.119']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """Deploy web files to server"""
    try:
        # Check if the archive_path exists
        if not path.exists(archive_path):
            return False

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Create the target directory with a timestamp
        file_name = archive_path.split('/')[-1]
        time_stamp = file_name.split('.')[0]
        target_dir = f'/data/web_static/releases/web_static_{time_stamp}/'
        run(f'sudo mkdir -p {target_dir}')

        # Uncompress the archive and delete the .tgz file
        run(f'sudo tar -xzf /tmp/{file_name} -C {target_dir}')

        # Remove the uploaded archive
        run(f'sudo rm /tmp/{file_name}')

        # Move contents into the host web_static directory
        run(f'sudo mv {target_dir}/web_static/* {target_dir}/')

        # Remove the extraneous web_static directory
        run(f'sudo rm -rf {target_dir}/web_static')

        # Delete pre-existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Re-establish symbolic link to the new deployment
        run(f'sudo ln -s {target_dir} /data/web_static/current')
    except Exception as e:
        # Print the exception for debugging purposes
        print(e)
        # Return False on failure
        return False

    # Return True on success
    return True
