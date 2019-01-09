#!/usr/bin/env python3
# -*-coding:utf-8-*-

import datetime as dt
import sys

PY3 = (sys.version_info[0] >= 3)

def _i2t(x):
    d1=str(x)
    d1=dt.datetime.strptime(d1,'%H%M%S')
    return d1.strftime("%H:%M:%S")

def _tofl(x):
    try:
        if ',' in x:
            x=x.replace(',','')
            x=float(x)
        if 'B' in x:
            x=x.replace('B','')
            x=float(x)*1000000000
        if 'M' in x:
            x=x.replace('M','')
            x=float(x)*1000000
        if 'K' in x:
            x=x.replace('K','')
            x=float(x)*1000           
        if '%' in x:
            x=x.replace('%','')
            x=float(x)            
        return x
    except:
        return x
