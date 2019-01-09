#!/usr/bin/env python3
# -*-coding:utf-8-*-

import pandas as pd
import numpy as np
import sys,requests,os
import lxml.html
from lxml import etree
import json
import re,time
import datetime as dt
from webdata.util.hds import user_agent as hds
from io import StringIO
from bs4 import BeautifulSoup
import webdata.puse.eastmpy.cont as wt

def _basic(url):
    r=requests.get(url,headers=hds())
    content=r.text

    content=content.split('123=')[1]
    data=json.loads(content)
    dataset='\n'.join(data['rank'])
    df=pd.read_csv(StringIO(dataset),header=None)
    df=df.drop([0,14],axis=1)
    df.columns=['code','name','price','chg%','chg','buy_volume','sell_volume','pre.cloes','ChCang','volume','open','low','high','Un']
    return df

basic='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C.{0}&sty=FCFL4O&sortType=C&sortRule=-1&page=1&pageSize=2000&js=var%20quote_123%3d{1}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123'
future={
    'sqs':basic.format('SHFE','{%22rank%22:[(x)],%22pages%22:(pc)}'),
    'dss':basic.format('DCE','{%22rank%22:[(x)],%22pages%22:(pc)}'),
    'zjs':basic.format('_168_FO','{%22rank%22:[(x)],%22pages%22:(pc)}'),
    'glb':basic.format('_UF','{%22rank%22:[(x)],%22pages%22:(pc)}'),
    'lme':basic.format('lme','{%22rank%22:[(x)],%22pages%22:(pc)}'),
    'ipe':basic.format('ipe','{%22rank%22:[(x)],%22pages%22:(pc)}'),
    'cobot':basic.format('cobot','{%22rank%22:[(x)],%22pages%22:(pc)}'),
    'nybot':basic.format('nybot','{%22rank%22:[(x)],%22pages%22:(pc)}'),
    'nymex':basic.format('nymex','{%22rank%22:[(x)],%22pages%22:(pc)}'),
    'tocom':basic.format('tocom','{%22rank%22:[(x)],%22pages%22:(pc)}')
    }
def get_Future_info_EM(mtype='sqs'):
    """
    核心题材
    --------------------------
    mtype:为股票代码，为6位数
    """
    url=future[mtype]
    df=_basic(url)
    df=df.applymap(lambda x:wt._tofl(x))
    df=df.replace('-',np.nan)
    return df

def get_Future_comparetoGlobal():
    url='http://hq2data.eastmoney.com/qhbj/index.aspx?param=RmbLatestPrice&sort=0'

    r=requests.get(url,headers=hds())
    content=r.text

    content=content.split('futures:["')[1].replace('"]}','').replace('","','\n')
    df=pd.read_csv(StringIO(content),header=None)
    df=df.drop([2,3,4,7,8,15,16,17],axis=1)
    df.columns=['name','Exchange','M_name','G_name','M_price','M_chg','G_price','G_chg','ToRMB','spread']
    del df['Exchange']
    df=df.set_index('name')
    df=df.applymap(lambda x:wt._tofl(x))
    df=df.replace('-',np.nan)    
    return df
    
if __name__=="__main__":
    #df=get_Future_info_EM(sys.argv[1])
    df=get_Future_comparetoGlobal()
