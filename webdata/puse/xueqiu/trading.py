#!/usr/bin/env python3
# -*-coding:utf-8-*-
from webdata.util.hds import user_agent as hds
import lxml.html
from io import StringIO
import sys,os,json
import requests
import pandas as pd
import numpy as np
from webdata.util.chrome_cookies import firefox_cookies as gcookies
import webdata.util.mktime as mk
import time
import datetime

def get_kdata_xueqiuv(code,begin=None,end=None,ktype='day',fq='N',host='.xueqiu.com'):

    if (code[0] in ['0','2','3','6','9']) and len(code)==6:
        if code[0] in ['6','9']:
            code='SH'+code
        elif code[0] in ['0','2','3']:
            code='SZ'+code
        else:
            sys.exit()

    s=requests.Session()
    kline={'day':'1day','week':'1week','month':'1month'}
    fqtype={'qfq':'before','N':'normal'}
    
    if end==None:
        end=int(time.time()*1000)
    else:
        end=mk.str2timestamp(end)*1000
    if begin==None:
        begin=datetime.datetime.now()-datetime.timedelta(days=360*3)
        begin=int(time.mktime(begin.timetuple())*1000)
    else:
        begin=mk.str2timestamp(begin)*1000
    
    url='https://xueqiu.com/stock/forchartk/stocklist.json?symbol={0}&period={1}&type={2}&begin={3}&end={4}'.format(code,kline[ktype],fqtype[fq],begin,end)
    r=s.get(url,cookies=gcookies(host),headers=hds())
    data=json.loads(r.text)
    df=pd.DataFrame(data['chartlist'])
    df['timestamp']=df['timestamp'].map(lambda x:mk.timestamp2str(x,mtype='t'))
    df=df.dropna(axis=1,how='all')
    df=df.set_index('timestamp')
    df=df.drop('time',axis=1)
    return df

def get_kdata_xueqiu(code,begin=None,ktype='day',fq='N',host='.xueqiu.com'):
    """
    code:
    """

    if (code[0] in ['0','2','3','6','9']) and len(code)==6:
        if code[0] in ['6','9']:
            code='SH'+code
        elif code[0] in ['0','2','3']:
            code='SZ'+code
        else:
            sys.exit()

    s=requests.Session()
    kline={'day':'day','week':'week','month':'month','quarter':'quarter','120m':'120m','60m':'60m','30m':'30m','15m':'15m','5m':'5m','1m':'1m'}
    fqtype={'qfq':'before','N':'normal','hfq':'after'}
    

    if begin==None:
        begin=datetime.datetime.now()
        begin=int(time.mktime(begin.timetuple())*1000)
    else:
        begin=mk.str2timestamp(begin)*1000
        
    url='https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={0}&begin={1}&period={2}&type={3}&count=-3260&indicator=kline,ma,macd,kdj,boll,rsi,wr,bias,cci,psy'.format(code,begin,kline[ktype],fqtype[fq])
    r=s.get(url,cookies=gcookies(host),headers=hds())
    data=json.loads(r.text)
    df=pd.DataFrame(data['data']['item'])
    df.columns=data['data']['column']
    df['timestamp']=df['timestamp'].map(lambda x:mk.timestamp2str(x,mtype='t'))
    df=df.dropna(axis=1,how='all')
    df=df.set_index('timestamp')
    return df

def get_dadan_xueqiu(code,host='.xueqiu.com'):

    if (code[0] in ['0','2','3','6','9']) and len(code)==6:
        if code[0] in ['6','9']:
            code='SH'+code
        elif code[0] in ['0','2','3']:
            code='SZ'+code
        else:
            sys.exit()    

    s=requests.Session()
    
    url='https://xueqiu.com/stock/forchart/stocklist.json?symbol={0}&period=1d&one_min=1'.format(code)
    r=s.get(url,cookies=gcookies(host),headers=hds())
    data=json.loads(r.text)
    df=pd.DataFrame(data['chartlist'])
    df=df.dropna(axis=1)
    df['timestamp']=df['timestamp'].map(lambda x:mk.timestamp2str(x,mtype='t'))
    return df
        
if __name__=="__main__":
    df=get_kdata_xueqiu(sys.argv[1])
