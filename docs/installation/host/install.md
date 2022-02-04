# SSO Shell Host
[toc]
## Introduction
The ssosh_host scripts are intended for use on the servers that an individual user is going to connect to. You can also use your own scripts for this if preferred, check the developer documentation for the full specification of the communication between host and server.

## Getting started
```bash
# Clone the ssosh_host repository from Github to your server
git clone https://github.com/scheibling/ssosh_host.git

# Enter the directory
cd ssosh_host

# Start the script for more information on how to bootstrap a new host
python3 ssosh_host.py register --help

usage: ssosh_host.py register [-h] -u DEST_URL [-H HOSTNAME] [-k KEY] [-s HOSTKEY] [-p PRINCIPALS_LOCATION] [-c CA_LOCATION] [-i INTERVAL]

optional arguments:
  -h, --help            show this help message and exit
  -u DEST_URL, --server-url DEST_URL
                        The URL to the SSOShell server
  -H HOSTNAME, --hostname HOSTNAME
                        The server hostname (default: my-server-hostname)
  -k KEY, --key KEY     The registration key displayed on the SSOShell server for this host
  -s HOSTKEY, --hostkey HOSTKEY
                        Manually add the host with an existing hostkey from the administration interface
  -p PRINCIPALS_LOCATION, --principals-location PRINCIPALS_LOCATION
                        Custom location for the principals file, default is /etc/ssosh/principals
  -c CA_LOCATION, --ca-location CA_LOCATION
                        Custom location for the SSH CA public key, default is /etc/ssosh/ssh-ca.pub
  -i INTERVAL, --interval INTERVAL
                        The cron interval to update the CA Public Key and principals file, default is 0,30 * * * *

# To register a host with the system hostname, use the below command.
# The key is the configuration key detailed in the server configuration, by default "custom-key"
python3 ssosh_host.py register --server-url https://ca.my-server.com --key custom-key

# To register a host with a custom hostname, use the below command
python3 ssosh_host.py register --server-url https://ca.my-server.com --hostname custom-hostname --key custom-key

# If you have already created the host in the administration interface, you can use the --hostkey option to get the configuration automatically
python3 ssosh_host.py register --server-url https://ca.my-server.com --hostname custom-hostname --key custom-key --hostkey ffffffff-ffff-ffff-ffff-ffffffffffff
```
Once this is done, the script will automatically create a new folder at /etc/ssosh with the configuration file, script for updating the CA public key and the principals file. There will also be a file added under /etc/cron.d/ssosh with a cron job to automatically update these two files every 30 minutes.

## Configuring SSH Server
To configure OpenSSH Server to accept the SSH connections from the SSOShell CA, you need to add the following to the /etc/ssh/sshd_config file:
```bash
# Authorized principals file contains the hostname of the server, the hostgroups the server is a part of and the user groups that have access to the server
# This currently gives all users in either of those categories access to all accounts within the server.
AuthorizedPrincipalsFile /etc/ssosh/principals

# The SSH CA Certificate for verifying the validity of the user SSH Certificates
TrustedUserCAKeys /etc/ssosh/ssh-ca.pub
```
Save the file, restart the SSH service, and you should be good to go! You just need to make sure that the server is able to reach the SSO Shell server to be able to retrieve the CA public key and the principals file.

## What does it do?
There are two parts to the host script, the registration and update parts

### Registration
On registration, given only the URL of the SSO Shell server, the script will do the following:

1. Get the system hostname
2. Make a request to the SSO Shell server to register the host with the following parameters:
    - System hostname
    - Configuration key
3. The server will then create the host if it doesn't already exists, and return the hostname and hostkey. If the host is already configured and no hostkey is provided, the registration will fail and prompt you to enter your hostkey to retrieve the configuration automatically.
4. The following is saved to the configuration file:
    {
        "hostname": "system-hostname",
        "server": "https://ca.my-server.com",
        "hostkey": "ffffffff-ffff-ffff-ffff-ffffffffffff",
        "cert_location": "/etc/ssosh/ssh-ca.pub",
        "principals_location": "/etc/ssosh/principals"
    }
5. The script is copied to /etc/ssosh/ssosh.py
6. A file is created in /etc/cron.d/ssosh with a cron job to update the CA public key and principals file every 30 minutes.

### Update
Without the --ca-only and/or --principals-only-flags, the script will do the following:
1. Open the configuration file and read the values
2. Make a request to the SSO Shell server with the hostname and hostkey to retrieve the allowed principal list
3. Make another request to the server with the hostkey to retrieve the SSH CA Certificate
4. Write the content of those requests to /etc/ssosh/principals and /etc/ssosh/ssh-ca.pub respectively