# repo2charliecloud
Wrapper around repo2docker producing charliecloud compatible tarballs

# Building a git repo to an image with no Dockerfile
# Running on my laptop
# docker is installed & accessible to our user
groups

# Create a venv & install repo2charliecloud into it

python3 -m venv v
cd v
source bin/activate

pip install repo2charliecloud

# Charliecloud is now installed

repo2charliecloud --help

# Build this repository: https://github.com/yuvipanda/requirements/tree/98744e8f91132a5f875da6fa08d7e6595da8ce9e

# apt.txt specifies emacs installation
# requirements.txt specifies numpy, with Python 3.7

repo2charliecloud https://github.com/yuvipanda/requirements --ref 98744e8f91132a5f875da6fa08d7e6595da8ce9e