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
        return float(x)
    except:
        return x

def _str2fl(x):
    try:
        if u'万' in x:
            x=x.replace('万','')
            x=float(x)
        if u'亿' in x:
            x=x.replace('亿','')
            x=float(x)*10000
        if u'%' in x:
            x=x.replace('%','')
            x=float(x)
        if u'千' in x:
            x=x.replace('千','')
            x=float(x)/10
        return float(x)
    except:
        return x


curr_last='http://d.10jqka.com.cn/v2/realhead/hs_{0}/last.js'
