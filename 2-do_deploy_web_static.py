#!/usr/bin/python3
"""
Fabric script to distribute an archive to web servers
"""

from fabric.api import env, put, run
from os.path import exists
from datetime import datetime

env.hosts = ['18.210.33.153', '54.236.27.119']


def do_deploy(archive_path):
    """
    Distributes an archive to web servers

    Args:
        archive_path (str): Path to the archive to deploy.

    Returns:
        bool: True if all operations have been done correctly, otherwise False.
    """
    try:
        # Check if the archive_path exists locally
        if not exists(archive_path):
            return False

        # Upload the archive to the temporary directory on the server
        put(archive_path, '/tmp/')

        # Extract the archive to a specific folder
        file_name = archive_path.split('/')[-1]
        filename = file_name.split('.')[0]
        folder_name = f'/data/web_static/releases/{filename}'
        run(f'mkdir -p {folder_name}')
        run(f'tar -xzf /tmp/{file_name} -C {folder_name}')

        # Delete the temporary archive
        run(f'rm /tmp/{file_name}')

        # Move the contents of the extracted folder to the release folder
        run(f"mv {folder_name}/web_static/* {folder_name}/")

        # Remove the symbolic link to the current release
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link to the latest release
        run(f'ln -s {folder_name} /data/web_static/current')

        return True
    except Exception:
        return False
