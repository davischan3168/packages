#!/usr/bin/env python3
# -*-coding:utf-8-*-
"""
大宗交易数据 的查询
"""

import pandas as pd
import numpy as np
import sys,os
import lxml.html
from lxml import etree
import requests,json
import re
import time
import datetime as dt
from bs4 import BeautifulSoup
today=time.strftime('%Y-%m-%d')
from io import StringIO
import webdata.puse.sinapy.cons as ws

name=['date','rzye','rzmre','rzche','rqylje','rqye','rqmce','rqche','rqye']

def dzjy():
    """
    查询大宗交易的数据,主要是当前数据的前20页的数据
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
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml?num=60&p={0}'.format(pn)
            r=requests.get(url)
            #print(url)
            r=r.content.decode('gbk')
            html=BeautifulSoup(r,'lxml')
            sarr=html.find(id='dataTable')
            df=pd.read_html(str(sarr),header=0)[0]
            DF =DF.append(df)
            pn=pn+1
            if pn > 20:
                break
            if df.empty is True:
                break
        except:
            break
        
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.drop_duplicates()
    return DF

def dzjy_share(code,begin=None,end=None):
    """
    查询某一区间的股票的大宗交易情况和相关数据.
    datetime:日期 如2017-06-16
    -----------------
    Return:
        DataFrame
    """
    if code[0] in ['0','2','3']:
        code='sz'+code
    if code[0] in ['6','9']:
        code = 'sh'+code

    if end == None or (dt.datetime.strptime(end, '%Y-%m-%d')< dt.datetime.strptime(begin, '%Y-%m-%d')):
        end=dt.datetime.strftime(dt.datetime.today(),'%Y-%m-%d')
        if begin == None:
            begin=dt.datetime.strftime(dt.datetime.today()-dt.timedelta(days=360),'%Y-%m-%d')

    pn=1
    DF=pd.DataFrame()
    ws._write_head()
    while True:
        try:
            ws._write_console()
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/dzjy/index.phtml?symbol={0}&bdate={1}&edate={2}&p={3}'.format(code,begin,end,pn)
            #print(url)
            r=requests.get(url)
            r=r.content.decode('gbk')
            html=BeautifulSoup(r,'lxml')
            sarr=html.find(id='dataTable')
            df=pd.read_html(str(sarr),header=0)[0]
            DF =DF.append(df)
            pn=pn+1
            if pn > 20:
                break
            if df.empty is True:
                break
        except:
            break
        
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.drop_duplicates()
    return DF



if __name__=="__main__":
    begin='2015-06-10'
    end='2017-06-17'
    code='000333'
    #ds=dzjy_share(code,begin,end)
    df=dzjy()
