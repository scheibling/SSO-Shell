#!/usr/bin/env python3
import os, requests
from socket import gethostname
from json import dumps, loads
from argparse import ArgumentParser
# This program maintains a copy of the SSH CA public key in /etc/sso-shell/ssh-ca.pub
# It also maintains the principal list at /etc/sso-shell/principals
# The settings for the parser are found in /etc/sso-shell/settings.json

PARSER = ArgumentParser(description='SSO Shell')

PARSER.add_argument('--create-config',
                    action='store_true',
                    dest='create_config',
                    help='Creates a new configuration file at /etc/sso-shell/settings.json')

PARSER.add_argument('-a', '--update-all',
                    action='store_true',
                    dest='update_all',
                    help='Updates principals and the SSH Certificate')

PARSER.add_argument('-p', '--update-principals',
                    action='store_true',
                    dest='update_principals',
                    help='Updates the principal list')

PARSER.add_argument('-c', '--update-ssh-ca',
                    action='store_true',
                    dest='update_ssh_ca',
                    help='Updates the SSH CA public key')

ARGS = PARSER.parse_args()

def load_config():
    if os.name == 'nt':
        config_file_location = 'C:\\ProgramData\\SSO-Shell\\'
    else:
        config_file_location = '/etc/sso-shell/'

    try:
        with open("%s%s" % (config_file_location, 'settings.json'), 'r') as f:
            config = loads(f.read())
    except Exception as e:
        print('An error occured while reading the configuration file: {}'.format(e))
        print('Please make sure you create a configuration file with --create-config before first run')
        exit(1)

    return config

def create_config():
    config_defaults = {
        'hostname': gethostname(),
        'address': 'https://ssoshell.io',
        'cert_location': '/etc/sso-shell/ssh-ca.pub',
        'principals_location': '/etc/sso-shell/principals'
    }

    if os.name == 'nt':
        config_file_location = 'C:/ProgramData/SSO-Shell/'
        config_defaults['cert_location'] = 'C:/ProgramData/SSO-Shell/ssh-ca.pub'
        config_defaults['principals_location'] = 'C:/ProgramData/SSO-Shell/principals'
    else:
        config_file_location = '/etc/sso-shell/'

    config = {}

    config['address'] = input('Enter the address of your SSOShell-server (default: {})'.format(config_defaults['address'])) or config_defaults['address']
    config['hostname'] = input('Enter the hostname/unique name for this server (default: {})'.format(config_defaults['hostname'])) or config_defaults['hostname']
    config['cert_location'] = input('Enter the location of the SSH CA public key as defined in sshd_config (default: {})'.format(config_defaults['cert_location'])) or config_defaults['cert_location']
    config['principals_location'] = input('Enter the location of the principal list as defined in sshd_config (default: {})'.format(config_defaults['principals_location'])) or config_defaults['principals_location']

    try:
        os.makedirs(config_file_location, exist_ok=True)
    except PermissionError:
        print('Permission denied. Please run as root.')
        exit(1)

    with open("%s%s" % (config_file_location, 'settings.json'), 'w') as f:
        f.write('{}'.format(dumps(config)))

def update_principals(config):
    url = "%s/host/%s/principals" % (config['address'], config['hostname'])
    resp = requests.get(url)

    if resp.status_code != 200:
        print('An error occured while updating the principal list: {}'.format(resp.text))
        exit(1)

    with open('%s' % config['principals_location'], 'w') as f:
        f.write('{}'.format(resp.text))

    return True

def update_ssh_ca(config):
    url = "%s/host/ca_public_key" % config['address']
    resp = requests.get(url)

    if resp.status_code != 200:
        print('An error occured while updating the SSH CA public key: {}'.format(resp.text))
        exit(1)

    with open('%s' % config['cert_location'], 'w') as f:
        f.write('{}'.format(resp.text))

    return True

if __name__ == '__main__':
    if ARGS.create_config:
        create_config()
        print("Config successfully created. You can now run or schedule the program with --update-all, --update-principals and/or --update-ssh-ca")
        exit(0)

    conf = load_config()

    if ARGS.update_principals or ARGS.update_all:
        update_principals(conf)
    if ARGS.update_ssh_ca or ARGS.update_all:
        update_ssh_ca(conf)