# you.com
# Please write a python script to automate the installation of the 
# "swift package manager" in the linux subsytem of Windows 10 Ubuntu

import os

# Update apt package index
os.system('sudo apt-get update')

# Install dependencies for Swift
os.system('sudo apt-get install -y clang libicu-dev libcurl4-openssl-dev libssl-dev')

# Download and install Swift
os.system('wget https://swift.org/builds/swift-5.5-release/ubuntu2004/swift-5.5-RELEASE/swift-5.5-RELEASE-ubuntu20.04.tar.gz')
os.system('tar xzf swift-5.5-RELEASE-ubuntu20.04.tar.gz')
os.system('sudo mv swift-5.5-RELEASE-ubuntu20.04 /usr/local/swift')

# Add Swift to PATH
os.system('echo "export PATH=/usr/local/swift/usr/bin:$PATH" >> ~/.bashrc')

# Verify the installation by printing the version number
os.system('swift --version')