#!/usr/bin/python3
# Bash script for packaging a web application using Fabric.
# Creates a compressed archive of 'web_static' and stores it in 'versions'.

# Import necessary modules
import os
from datetime import datetime
from fabric.api import local

def do_pack():
    """
    Create a compressed archive of the 'web_static' directory.

    Returns:
        str: Path to the created compressed archive, or None if the operation fails.
    """
    dt = datetime.now()

    file_name = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second
    )

    if not os.path.isdir("versions"):
        if local("mkdir -p versions").failed:
            return None

    # Attempt to create a compressed archive; return None if failed
    if local("tar -cvzf {} web_static".format(file_name)).failed:
        return None

    # Return the path to the created compressed archive
    return file_name

