#!/usr/bin/env python3
# -*-coding:utf-8-*-

import sys
import os
import sqlite3
try:
    from win32.win32crypt import CryptUnprotectData
except:
    from Crypto.Cipher import AES
    from Crypto.Protocol.KDF import PBKDF2
from hashlib import pbkdf2_hmac
import pathlib
import urllib.error
import urllib.parse
from typing import Any, Dict, Iterator, Union  # noqa
import keyring
import fnmatch

def get_profile_path():
    if sys.platform in [ 'linux', 'linux2', 'freebsd9']:
        s1=os.getenv("HOME")
        s2="/.mozilla/firefox"
    elif sys.platform == 'win32':
        s1=os.getenv('APPDATA')
        s2="\\Mozilla\\Firefox\\Profiles\\"        

    dir=os.listdir(s1+s2)
    for d in dir:
        if fnmatch.fnmatch(d,'*.default'):
            path=s1+s2+'/'+d+"/cookies.sqlite"
            return path

if sys.platform=='darwin':
    CHROME_CONFIG_DIR = os.path.join(os.getenv('HOME'), 'Library', 'Application Support', 'Google', 'Chrome', 'Default')
    FIREFOX_CONFIG_DIR = os.path.join(os.getenv('HOME'), 'Library', 'Application Support', 'Firefox')
elif sys.platform in [ 'linux', 'linux2', 'freebsd9']:
    CHROME_CONFIG_DIR = os.path.expanduser('~/.config/chromium/Default')
    FIREFOX_CONFIG_DIR = os.path.expanduser('~/.mozilla/firefox')
elif sys.platform == 'win32':
    CHROME_CONFIG_DIR = None
    FIREFOX_CONFIG_DIR = get_profile_path()
else:
    CHROME_CONFIG_DIR = None
    FIREFOX_CONFIG_DIR = None
