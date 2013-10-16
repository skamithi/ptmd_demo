# This script will run the first time the virtual machine boots
# It is ran as root.

# Install openssh-server
apt-get update
apt-get install -qqy --force-yes openssh-server