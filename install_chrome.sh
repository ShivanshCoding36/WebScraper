#!/usr/bin/env bash
set -o errexit

# Install Chrome
apt-get update
apt-get install -y wget gnupg unzip
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install -y ./google-chrome-stable_current_amd64.deb

# Install ChromeDriver matching Chrome version
CHROME_VERSION=$(google-chrome --version | awk '{print $3}')
wget https://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /usr/local/bin/
chmod +x /usr/local/bin/chromedriver
