#!/usr/bin/env python3
# -*-coding:utf-8-*-
import os
import sys
import sqlite3
import urllib
#import urllib2
import fnmatch


def kill_firefox():
    os.system("pkill firefox")

def firefox_cookies(host):
    """
    host:  .example.com
    """
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
            #print(path)

    sqlite_file = path
    conn = sqlite3.connect(sqlite_file)
    c = conn.cursor()

    c.execute("""SELECT name, value FROM moz_cookies WHERE host=?""", (host,))
    cookies = dict((c[0],c[1]) for c in c.fetchall())
    #print(cookies)
    return cookies

if __name__=="__main__":
    d=firefox_cookies(sys.argv[1])
    
