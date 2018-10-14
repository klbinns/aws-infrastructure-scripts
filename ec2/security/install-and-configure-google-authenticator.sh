#!/bin/bash

# Install Google Authenticator
sudo apt-get install -y libpam-google-authenticator

# Apply changes to sshd to enable the authenticator
sed -i \"s/ChallengeResponseAuthentication no/ChallengeResponseAuthentication yes/g\" /etc/ssh/sshd_config

# Add to end of the sshd_config file (note this text will not highlight in Vim if you review-but it is effective)
# REQUIRED to allow public key auth while using google authenticator
#echo "AuthenticationMethods   publickey,keyboard-interactive" >> /etc/ssh/sshd_config

# Uncomment out the following line ONLY if you're not using password based auth for ssh and you want to use
# the authenticator with public-key authentication
#sed -i \"s/@include common-auth/#@include common-auth/g\" /etc/pam.d/sshd

sed -i "6 a # Google Authenticator with exception for users who are not enabled\nauth required pam_google_authenticator.so nullok" /etc/pam.d/sshd

# Restart SSH
service ssh restart

