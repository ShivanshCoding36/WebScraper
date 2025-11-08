#!/usr/bin/env bash
set -eux

apt-get update

# Install Google Chrome
curl -fsSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /tmp/chrome.deb
apt-get install -y /tmp/chrome.deb || apt-get --fix-broken install -y

# Get Chrome version
CHROME_VERSION=$(google-chrome --version | awk '{print $3}')
echo "Detected Chrome version: $CHROME_VERSION"

# Install exact matching ChromeDriver
CHROMEDRIVER_URL="https://chromedriver.storage.googleapis.com/$(curl -s https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION%.*})/chromedriver_linux64.zip"

echo "Downloading driver: $CHROMEDRIVER_URL"
curl -Lo /tmp/chromedriver.zip $CHROMEDRIVER_URL

apt-get install -y unzip
unzip /tmp/chromedriver.zip -d /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

echo "✅ Chrome + ChromeDriver installed"
