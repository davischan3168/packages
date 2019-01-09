#!/usr/bin/env python3
# -*-coding:utf-8-*-
from webdata.util.hds import user_agent as hds
import lxml.html
from io import StringIO
import sys,os,json,time
import requests
import pandas as pd
import numpy as np
from webdata.util.chrome_cookies import firefox_cookies as gcookies

def finance_xueqiu(code,host='.xueqiu.com'):
    if code[0] in ['6','9']:
        code='SH'+code
    elif code[0] in ['0','2','3']:
        code='SZ'+code
    else:
        sys.exit()

    exlist=[]
    s=requests.Session()
    url='https://xueqiu.com/stock/f10/finmainindex.json?symbol={0}&page=1&size=60'.format(code)
    
    r=s.get(url,cookies=gcookies(host),headers=hds())
    data=json.loads(r.text)
    df=pd.DataFrame(data['list'])
    df=df.set_index('reportdate')
    df.index=pd.to_datetime(df.index)
    df['symbol']=code
    df=df.where(df.notnull(),np.nan)
    df=df.drop(['compcode','name'],axis=1)
    df=df.dropna(axis=1,how='all')
    return df


def div_xueqiu(code,host='.xueqiu.com'):
    if code[0] in ['6','9']:
        code='SH'+code
    elif code[0] in ['0','2','3']:
        code='SZ'+code
    else:
        sys.exit()

    exlist=[]
    s=requests.Session()
    #    https://xueqiu.com/stock/f10/bonus.json?symbol=SZ200869&page=1&size=60
    url='https://xueqiu.com/stock/f10/bonus.json?symbol={0}&page=1&size=60'.format(code)
    
    r=s.get(url,cookies=gcookies(host),headers=hds())
    data=json.loads(r.text)
    df=pd.DataFrame(data['list'])
    df=df.set_index('bonusimpdate')
    df.index=pd.to_datetime(df.index)
    df['symbol']=code
    #df=df.where(df.notnull(),np.nan)
    df=df.drop(['secode'],axis=1)
    df=df.dropna(axis=1,how='all')
    return df
        
        
        
        
    
    
    
if __name__=="__main__":
    #df=get_searchjson_xueqiu(sys.argv[1])
    dd=finance_xueqiu(sys.argv[1])
    #text=get_text('/2395350277/105331151')
    df=div_xueqiu(sys.argv[1])
