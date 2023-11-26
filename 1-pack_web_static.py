#!/usr/bin/python3
# This is a Bash script for packaging a web application using Fabric.
# It creates a compressed archive of the 'web_static' directory and stores it in the 'versions' directory.

# Import necessary modules
import os
from datetime import datetime
from fabric.api import local

# Function to create a compressed archive of the 'web_static' directory
def do_pack():
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

