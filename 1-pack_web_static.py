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
    # Check if 'versions' directory exists; create it if not
    if os.path.isdir("versions") is False:
        # Attempt to create the 'versions' directory; return None if failed
        if local("mkdir versions").failed is True:
            return None

    # Generate a unique file name for the compressed archive using the current date and time
    dt = datetime.now()
    file = f"versions/web-static_{dt.year}{dt.month}{dt.day}{dt.hour}{dt.minute}{dt.second}.tgz"

    # Attempt to create a compressed archive; return None if failed
    if local(f'tar -czvf {file} web_static').failed is True:
        return None

    # Return the path to the created compressed archive
    return file

