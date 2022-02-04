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
