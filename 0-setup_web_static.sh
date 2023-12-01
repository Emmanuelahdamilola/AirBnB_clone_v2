#!/usr/bin/env bash
# Script to set up the server file system for deployment

#!/usr/bin/env bash
# Script to set up the server file system for deployment

# Install Nginx
sudo apt-get -y update
sudo apt-get -y install nginx
sudo service nginx start

# Configure the file system
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
# Configure the file system
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

# Create a fake HTML document
echo "<!DOCTYPE html>
<html lang=\"en\">
<head>
</head>
<body>
    <h1>Holberton School</h1>
</body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set permissions
sudo chown -R ubuntu:ubuntu /data/

# Configure Nginx
sudo sed -i '44i \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

# Restart the web server
sudo service nginx restart
