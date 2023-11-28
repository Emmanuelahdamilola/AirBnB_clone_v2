#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

# Ensure Nginx is installed
if ! [ -x "$(command -v nginx)" ]; then
  sudo apt-get update
  sudo apt-get -y install nginx
fi

# Create /data/ directory if it doesn't exist
if ! [ -d "/data/" ]; then
  sudo mkdir /data/
fi

# Create /data/web_static/ directory if it doesn't exist
if ! [ -d "/data/web_static/" ]; then
  sudo mkdir /data/web_static/
fi

# Create /data/web_static/releases/ directory if it doesn't exist
if ! [ -d "/data/web_static/releases/" ]; then
  sudo mkdir /data/web_static/releases/
fi

# Create /data/web_static/shared/ directory if it doesn't exist
if ! [ -d "/data/web_static/shared/" ]; then
  sudo mkdir /data/web_static/shared/
fi

# Create /data/web_static/releases/test/ directory if it doesn't exist
if ! [ -d "/data/web_static/releases/test/" ]; then
  sudo mkdir /data/web_static/releases/test/
fi

# Create a fake HTML file for testing Nginx configuration
echo "<html><head></head><body>Holberton School</body></html>" > /data/web_static/releases/test/index.html

# Create or recreate symbolic link /data/web_static/current
#if [ -L "/data/web_static/current" ]; then
#  sudo rm /data/web_static/current
#fi
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Set ownership of /data/ to the ubuntu user and group, recursively
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve content from /data/web_static/current/ to /hbnb_static
printf %s 'server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root /var/www/html;
    index index.html index.htm;

    location /hbnb_static {
        alias /data/web_static/current/;
	index index.html index.htm;
    }

    error_page 404 /404.html;
    location /404 {
    root /var/www/html;
    internal;
    }
}' > /etc/nginx/sites-available/default

# Restart Nginx to apply the changes
sudo service nginx restart

