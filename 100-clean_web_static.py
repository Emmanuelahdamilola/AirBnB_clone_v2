#!/usr/bin/python3
"""Deploy web static package and clean outdated archives
"""
from fabric.api import *
from datetime import datetime
from os import path

env.hosts = ['18.210.33.153', '54.236.27.119']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """Function to compress directory
    Return: path to archive on success; None on fail
    """
    try:
        # Get current time
        now = datetime.now()
        now = now.strftime('%Y%m%d%H%M%S')
        archive_path = 'versions/web_static_' + now + '.tgz'

        # Create archive
        local('mkdir -p versions/')
        result = local('tar -cvzf {} web_static/'.format(archive_path))

        # Check if archiving was successful
        if result.succeeded:
            return archive_path
        return None
    except:
        return None


def do_deploy(archive_path):
    """Deploy web files to server
    """
    try:
        # Check if the archive_path exists
        if not (path.exists(archive_path)):
            return False

        # Upload the archive to the /tmp/ directory on the server
        put(archive_path, '/tmp/')

        # Create the target directory with a timestamp
        file_name = archive_path.split('/')[-1]
        time_stamp = file_name.split('.')[0]
        target_directory = '/data/web_static/releases/web_static_{}/'.format(time_stamp)
        run('sudo mkdir -p {}'.format(target_directory))

        # Uncompress the archive and delete the .tgz file
        run('sudo tar -xzf /tmp/{} -C {}'.format(file_name, target_directory))

        # Remove the uploaded archive
        run('sudo rm /tmp/{}'.format(file_name))

        # Move contents into the host web_static directory
        run('sudo mv {}/web_static/* {}/'.format(target_directory, target_directory))

        # Remove the extraneous web_static directory
        run('sudo rm -rf {}/web_static'.format(target_directory))

        # Delete pre-existing symbolic link
        run('sudo rm -rf /data/web_static/current')

        # Re-establish symbolic link to the new deployment
        run('sudo ln -s {} /data/web_static/current'.format(target_directory))
    except:
        # Return False on failure
        return False

    # Return True on success
    return True


def do_clean(number=0):
    """Clean outdated archives
    """
    try:
        number = int(number)
        if number < 0:
            return False

        # Delete unnecessary archives in the versions folder
        local('cd versions; ls -1t | tail -n +{} | xargs rm -f'.format(number + 1))

        # Delete unnecessary archives in the /data/web_static/releases folder on remote servers
        run('cd /data/web_static/releases; ls -1t | tail -n +{} | xargs rm -rf'
            .format(number + 1))
    except:
        return False

    # Return True on success
    return True


def deploy():
    """Deploy web static
    """
    # Perform deployment by calling do_pack and do_deploy
    return do_deploy(do_pack())
