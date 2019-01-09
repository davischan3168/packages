#!/usr/bin/env python3
# -*-coding:utf-8-*-

import pandas as pd
import numpy as np
import sys,os
import lxml.html
from lxml import etree
import requests,json
import re
import time
import datetime
from bs4 import BeautifulSoup
today=time.strftime('%Y-%m-%d')
from io import StringIO
import webdata.puse.sinapy.cons as ws

def holders(year,quarter,mytype):
    """
    mytype:主要有四种类型,jgcg,jjzc,sbzc,qfii
    year: 年份
    quarter:季度,分为1,2,3,4
    -----------------
    Return:
        DataFrame
    """
    
    pn=1
    DF=pd.DataFrame()
    ws._write_head()
    while True:
        try:
            ws._write_console()
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/{3}/index.phtml?symbol=%D6%A4%C8%AF%BC%F2%B3%C6%BB%F2%B4%FA%C2%EB&reportdate={0}&quarter={1}&p={2}'.format(year,quarter,pn,mytype)
            r=requests.get(url)
            r=r.content.decode('gbk')
            html=BeautifulSoup(r,'lxml')
            text=html.find(id='dataTable')
            df=pd.read_html(str(text),header=0)[0]
            #print(df)
            if df.empty is True:
                break
            else:
                pn = pn + 1
                DF =DF.append(df)
        except:
            break
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.drop_duplicates()
    print(DF)
    if mytype in ['jjzc','sbzc','qfii']:
        DF=DF.drop([1,2],axis=0)
    try:
        DF=DF.set_index('证券代码')
        DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))
    except:
        DF=DF.set_index('代码')
        DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))
    finally:
        pass
    return DF

def holders_share(code,year,quarter,mytype):
    """
    mytype:主要有四种类型,jgcg,jjzc,sbzc,qfii
    year: 年份
    quarter:季度,分为1,2,3,4
    -----------------
    Return:
        DataFrame
    """    
    ws._write_head()
    try:
        ws._write_console()
        url='http://vip.stock.finance.sina.com.cn/q/go.php/vComStockHold/kind/{3}/index.phtml?symbol={0}&reportdate={1}&quarter={2}'.format(code,year,quarter,mytype)
        r=requests.get(url)
        r=r.content.decode('gbk')
        html=BeautifulSoup(r,'lxml')
        text=html.find(id='dataTable')
        DF=pd.read_html(str(text),header=0)[0]
    except:
        pass

    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.drop_duplicates()
    #print(DF)
    if mytype in ['jjzc','sbzc','qfii']:
        DF=DF.drop([1,2],axis=0)
    try:
        DF=DF.set_index('证券代码')
        DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))
    except:
        DF=DF.set_index('代码')
        DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))
    finally:
        pass
    return DF

if __name__=="__main__":
    year=2017
    quarter=1
    code='600497'
    df=holders(year,quarter,'sbzc')
    #dd=holders_share(code,year,quarter,'jgcg')
