#!/usr/bin/env python3
import os
import sys
import json
import requests
import shutil
from socket import gethostname
from argparse import ArgumentParser

IS_WINDOWS = True if os.name == 'nt' else False

CONFIG_LOCATION = os.path.join('C:', 'ProgramData', 'SSOSH', 'config.json') if IS_WINDOWS else os.path.join('/etc', 'ssosh')
CONFIG_FILENAME = 'settings.json'
SCRIPT_FILENAME = 'ssosh.py' 
CERT_LOCATION = os.path.join('C:', 'ProgramData', 'SSOSH', 'ssh-ca.pub') if IS_WINDOWS else os.path.join('/etc', 'ssosh', 'ssh-ca.pub')
PRINCIPALS_LOCATION = os.path.join('C:', 'ProgramData', 'SSOSH', 'principals.txt') if IS_WINDOWS else os.path.join('/etc', 'ssosh', 'principals')
CRON_LOCATION = False if IS_WINDOWS else os.path.join('/etc', 'cron.d', 'ssosh')
UPDATE_INTERVAL = "0,30 * * * *"
LOG_LOCATION = os.path.join('C:', 'ProgramData', 'SSOSH', 'run.log') if IS_WINDOWS else os.path.join

PARSER = ArgumentParser(description='SSO Shell')
SUBP = PARSER.add_subparsers(dest='action')

registration_parser = SUBP.add_parser('register', help='Register a new host')

registration_parser.add_argument('-u', '--server-url',
                                 action='store',
                                 dest='dest_url',
                                 required=True,
                                 help='The URL to the SSOShell server')

registration_parser.add_argument('-H', '--hostname',
                                 action='store',
                                 dest='hostname',
                                 help=f'The server hostname (default: {gethostname()})',
                                 default=gethostname())

registration_parser.add_argument('-k', '--key',
                                 action='store',
                                 dest='key',
                                 help='The registration key displayed on the SSOShell server for this host')

registration_parser.add_argument('-s', '--hostkey',
                                 action='store',
                                 dest='hostkey',
                                 help='Manually add the host with an existing hostkey from the administration interface'
                                 )

registration_parser.add_argument('-p', '--principals-location',
                                 action='store',
                                 dest='principals_location',
                                 default=PRINCIPALS_LOCATION,
                                 help=f'Custom location for the principals file, default is {PRINCIPALS_LOCATION}')

registration_parser.add_argument('-c', '--ca-location',
                                 action='store',
                                 dest='ca_location',
                                 default=CERT_LOCATION,
                                 help=f'Custom location for the SSH CA public key, default is {CERT_LOCATION}')

registration_parser.add_argument('-i', '--interval', 
                                 action='store',
                                 dest='interval',
                                 default=UPDATE_INTERVAL,
                                 help=f'The cron interval to update the CA Public Key and principals file, default is {UPDATE_INTERVAL}')

update_parser = SUBP.add_parser('update', help='Update the principal list and the SSH CA public key')

update_parser.add_argument('-c', '--ca-only', 
                           action='store_true',
                           dest='ca_only',
                           default=False,
                           help='Only update the SSH CA public key')

update_parser.add_argument('-p', '--principals-only',
                           action='store_true',
                           dest='principals_only',
                           default=False,
                           help='Only update the principal list')

ARGS = PARSER.parse_args()

def load_config():
    try:
        with open(CONFIG_LOCATION, 'r') as config_file:
            return json.loads(config_file.read())
    except FileNotFoundError:
        print('Configuration file not found. Please run `ssosh config` to register this host with a server and create a configuration file.')
        exit(0)

def register_host(cli_args):
    if getattr(cli_args, 'key', False) in [False, None, '', ' '] and getattr(cli_args, 'hostkey', False) in [False, None, '', ' ']:
        print('No key provided. Please run `ssosh config help` to see the options for for bootstrapping a host.')
        sys.exit(1)
     
    if getattr(cli_args, 'hostname', False) in [False, '', ' ']:
        print(f"Invalid hostname (args['hostname'])")
        sys.exit(1)
    
    uri = f"{cli_args.dest_url}/host/bootstrap/"
    
    body = {
        'hostname': cli_args.hostname,
        'key': cli_args.key
    }
    
    resp = requests.post(url=uri, json=body)
    
    if resp.status_code > 499:
        print("Server error occured while bootstrapping host")
        sys.exit(1)
    
    try:
        body_json = resp.json()
    except json.decoder.JSONDecodeError:
        print("Error decoding response from server")
    
    if resp.status_code != 201 and body_json.get('error_code', False):
        if body_json['error_code'] == 1:
            print(body_json['error'])
            sys.exit(1)
        if body_json['error_code'] == 2:
            if getattr(cli_args, 'hostkey', False) is False:
                print('Host is already registered with server. You need to provide the hostkey to get the configuration from the server.')    
                sys.exit(1)
            body['hostkey'] = cli_args.hostkey
            resp = requests.post(url=uri, json=body)
            body_json = resp.json()
    
    if resp.status_code != 201 and resp.status_code != 200:
        print("An unspecified error occured: ")
        print(body_json)
        sys.exit(1)
        
    config = {
        'hostname': cli_args.hostname,
        'server': cli_args.dest_url,
        'hostkey': body_json['hostkey'],
        'cert_location': CERT_LOCATION,
        'principals_location': PRINCIPALS_LOCATION
    }
    
    if not os.path.isdir(CONFIG_LOCATION):
        os.mkdir(CONFIG_LOCATION)
        
    with open(os.path.join(CONFIG_LOCATION, CONFIG_FILENAME), 'w') as config_file:
        json.dump(config, config_file, indent=4)
    
    shutil.copy(os.path.abspath(__file__), os.path.join(CONFIG_LOCATION, SCRIPT_FILENAME))
    
    if not CRON_LOCATION:
        print(f"Host registered with server and updates are scheduled. You can now run ")
        print("You now need to schedule the updates for the CA Public Key and Principals file. Please consult the documentation at https://docs.ssosh.io for Windows host installation.")
        sys.exit(0)
    
    with open(CRON_LOCATION, 'w') as cron_file:
        cron_file.write('SHELL=/bin/bash\n')
        cron_file.write('MAILTO=root\n')
        cron_file.write('PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin\n')
        cron_file.write('\n')
        cron_file.write(f'{cli_args.interval} root {os.path.join(CONFIG_LOCATION, SCRIPT_FILENAME)} update \n')
    
    
def update_principals(config):
    url = f"{config['server']}/host/{config['hostname']}/principals"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Host-Key': config['hostkey']
    }
    
    resp = requests.get(url=url, headers=headers)
    
    if resp.status_code != 200:
        print('An error occured while updating the principal list')
        print(resp.text)
        sys.exit(1)
        
    with open(config['principals_location'], 'w') as principals_file:
        principals_file.write(resp.text)

def update_ssh_ca(config):
    url = f"{config['server']}/host/ca_public_key"
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Host-Key': config['hostkey']
    }
    
    resp = requests.get(url=url, headers=headers)
    
    if resp.status_code != 200:
        print('An error occured while updating the SSH CA Certificate list')
        print(resp.text)
        sys.exit(1)
        
    with open(config['cert_location'], 'w') as principals_file:
        principals_file.write(resp.text)
        
def load_config(path):
    try:
        with open(path, 'r') as config_file:
            config = json.loads(config_file.read())
            return config
    except FileNotFoundError:
        return False
        

if __name__ == '__main__':
    if ARGS.action is None:
        PARSER.print_help()
        sys.exit(0)
    
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    
    if not is_admin:
        print("You need to run this script with privileges, exiting...")
        sys.exit(1)
    
    config = load_config(os.path.join(CONFIG_LOCATION, CONFIG_FILENAME))
    
    if ARGS.action == 'update':
        if config not in [False, None]:
            if not ARGS.ca_only:
                update_principals(config)
            
            if not ARGS.principals_only:
                update_ssh_ca(config)
        else:
            print("An error occured while loading the configuration file")

    if config is False and ARGS.action != 'register':
        print("You need to run ssosh register to register this host with a server.")
        print("Type ssosh register --help for more information.")
        sys.exit(1)
        
    if config is not False and ARGS.action == 'register':
        print("A configuration file already exists. Please remove this manually at {CONFIG_LOCATION}/{CONFIG_FILENAME} if you want to re-register this host.")
        sys.exit(1)
        
    if ARGS.action == 'register':
        register_host(ARGS)
