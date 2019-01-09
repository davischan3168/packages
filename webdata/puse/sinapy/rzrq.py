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

name=['date','rzye','rzmre','rzche','rqylje','rqye','rqmce','rqche','rqye']

def marginall(begin,end):
    """
    datetime:日期 如2017-06-16
    -----------------
    Return:
        DataFrame
    """
    days=pd.date_range(begin,end,freq='B')
    DF=pd.DataFrame()
    ws._write_head()
    for day in days:
        try:
            ws._write_console()
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/rzrq/index.phtml?tradedate={0}'.format(day.strftime('%Y-%m-%d'))
            r=requests.get(url)
            #print(url)
            r=r.content.decode('gbk')
            html=lxml.html.parse(StringIO(r))
            res=html.xpath("//div[@class='list']/table[1]//tr[position()>1]")
            sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(str(sarr))
            sarr='<table>%s</table>'%sarr
            df=pd.read_html(sarr,header=0)[0]
            df['day']=day
            #print(df)
            if df.empty is False:
                DF =DF.append(df)
        except:
            pass
        
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.drop_duplicates()
    #print(DF)

    return DF

def margindetail(begin,end):
    """
    datetime:日期 如2017-06-16
    -----------------
    Return:
        DataFrame
    """
    days=pd.date_range(begin,end,freq='B')
    DF=pd.DataFrame()
    ws._write_head()
    for day in days:
        try:
            ws._write_console()
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/rzrq/index.phtml?tradedate={0}'.format(day.strftime('%Y-%m-%d'))
            r=requests.get(url)
            r=r.content.decode('gbk')
            html=lxml.html.parse(StringIO(r))
            res=html.xpath("//div[@class='list']/table[2]//tr[position()>3]")
            sarr = [etree.tostring(node) for node in res]
            #sarr = ''.join(sarr)
            #print(sarr)
            sarr = ''.join(str(sarr))
            sarr='<table>%s</table>'%sarr
            df=pd.read_html(sarr,header=None)[0]
            df['day']=day            
            #print(df)
            if df.empty is False:
                DF =DF.append(df)
        except:
            pass
        
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.drop_duplicates()
    name.append('date')
    name.insert(0,'code')
    DF.columns=name
    DF['code']=DF['code'].map(lambda x: str(x).split('.')[0].zfill(6))
    DF=DF.set_index(['code','date'])
    
    #print(DF)

    return DF

def margin_share(code,begin,end):
    """
    datetime:日期 如2017-06-16
    -----------------
    Return:
        DataFrame
    """
    DF=pd.DataFrame()
    ws._write_head()
    
    try:
        ws._write_console()
        url='http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/rzrq/index.phtml?symbol={0}&bdate={1}&edate={2}'.format(code,begin,end)
        #print(url)
        r=requests.get(url)
        r=r.content.decode('gbk')
        
        html=BeautifulSoup(r,'lxml')
        sarr=html.find(id='dataTable')
        df=pd.read_html(str(sarr),header=None,skiprows=3)[0]
        df=df.applymap(lambda x:np.where(x=='--',np.nan,x))
        df=df.drop(0,axis=1)
        #print(df.head())
        
        df.columns=name
        df=df.set_index('date')
        return df
    except Exception as e:
        print(e)
        pass
        
    #print(DF)

    


if __name__=="__main__":
    begin='2017-06-10'
    end='2017-06-17'
    #df=marginall('2017-06-10',end)
    #dd=margindetail(begin,end)
    ds=margin_share('600160',begin,end)
