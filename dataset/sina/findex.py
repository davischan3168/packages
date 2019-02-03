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
from webdata.util.hds import user_agent as hds

def profit(year,quarter):
    pn=1
    DF=pd.DataFrame()
    ws._write_head()
    while True:
        try:
            ws._write_console()
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vFinanceAnalyze/kind/profit/index.phtml?s_i=&s_a=&s_c=&reportdate={0}&quarter={1}&p={2}'.format(year,quarter,pn)
            r=requests.get(url,headers=hds())
            r=r.content.decode('gbk')
            html=BeautifulSoup(r,'lxml')
            text=html.find(id='dataTable')
            df=pd.read_html(str(text),header=0)[0]
            if df.empty is True:
                break
            else:
                pn = pn + 1
                DF =DF.append(df)
        except:
            break
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.set_index('股票代码')
    DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))
    DF['date']=str(year)+'_'+str(quarter).zfill(2)
    name=list(DF.columns)
    name.remove('股票名称')
    name.remove('date')
    for label in name:
        DF[label]=DF[label].astype(float)    
    return DF

def operation(year,quarter):
    pn=1
    DF=pd.DataFrame()
    ws._write_head()
    while True:
        try:
            ws._write_console()
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vFinanceAnalyze/kind/operation/index.phtml?s_i=&s_a=&s_c=&reportdate={0}&quarter={1}&p={2}'.format(year,quarter,pn)
            r=requests.get(url,headers=hds())
            r=r.content.decode('gbk')
            html=BeautifulSoup(r,'lxml')
            text=html.find(id='dataTable')
            df=pd.read_html(str(text),header=0)[0]
            if df.empty is True:
                break
            else:
                pn = pn + 1
                DF =DF.append(df)
        except:
            break
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.set_index('股票代码')
    DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))
    DF['date']=str(year)+'_'+str(quarter).zfill(2)
    name=list(DF.columns)
    name.remove('股票名称')
    name.remove('date')
    for label in name:
        DF[label]=DF[label].astype(float)      
    return DF

def grow(year,quarter):
    pn=1
    DF=pd.DataFrame()
    ws._write_head()
    while True:
        try:
            ws._write_console()
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vFinanceAnalyze/kind/grow/index.phtml?s_i=&s_a=&s_c=&reportdate={0}&quarter={1}&p={2}'.format(year,quarter,pn)
            r=requests.get(url,headers=hds())
            r=r.content.decode('gbk')
            html=BeautifulSoup(r,'lxml')
            text=html.find(id='dataTable')
            df=pd.read_html(str(text),header=0)[0]
            if df.empty is True:
                break
            else:
                pn = pn + 1
                DF =DF.append(df)
        except:
            break
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.set_index('股票代码')
    DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))
    DF['date']=str(year)+'_'+str(quarter).zfill(2)
    name=list(DF.columns)
    name.remove('股票名称')
    name.remove('date')
    for label in name:
        DF[label]=DF[label].astype(float)     
    return DF

def debtpaying(year,quarter):
    pn=1
    DF=pd.DataFrame()
    ws._write_head()
    while True:
        try:
            ws._write_console()
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vFinanceAnalyze/kind/debtpaying/index.phtml?s_i=&s_a=&s_c=&reportdate={0}&quarter={1}&p={2}'.format(year,quarter,pn)
            r=requests.get(url,headers=hds())
            r=r.content.decode('gbk')
            html=BeautifulSoup(r,'lxml')
            text=html.find(id='dataTable')
            df=pd.read_html(str(text),header=0)[0]
            if df.empty is True:
                break
            else:
                pn = pn + 1
                DF =DF.append(df)
        except:
            break
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.set_index('股票代码')
    DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))
    DF['date']=str(year)+'_'+str(quarter).zfill(2)
    name=list(DF.columns)
    name.remove('股票名称')
    name.remove('date')
    for label in name:
        DF[label]=DF[label].astype(float)     
    return DF

def cashflow(year,quarter):
    pn=1
    DF=pd.DataFrame()
    ws._write_head()
    while True:
        try:
            ws._write_console()
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vFinanceAnalyze/kind/cashflow/index.phtml?s_i=&s_a=&s_c=&reportdate={0}&quarter={1}&p={2}'.format(year,quarter,pn)
            r=requests.get(url,headers=hds())
            r=r.content.decode('gbk')
            html=BeautifulSoup(r,'lxml')
            text=html.find(id='dataTable')
            df=pd.read_html(str(text),header=0)[0]
            if df.empty is True:
                break
            else:
                pn = pn + 1
                DF =DF.append(df)
        except:
            break
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.set_index('股票代码')
    DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))
    DF['date']=str(year)+'_'+str(quarter).zfill(2)
    name=list(DF.columns)
    name.remove('股票名称')
    name.remove('date')
    for label in name:
        DF[label]=DF[label].astype(float)     
    return DF

def mainindex(year,quarter):
    pn=1
    DF=pd.DataFrame()
    ws._write_head()
    while True:
        try:
            ws._write_console()
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vFinanceAnalyze/kind/mainindex/index.phtml?s_i=&s_a=&s_c=&reportdate={0}&quarter={1}&p={2}'.format(year,quarter,pn)
            r=requests.get(url,headers=hds())
            r=r.content.decode('gbk')
            html=BeautifulSoup(r,'lxml')
            text=html.find(id='dataTable')
            df=pd.read_html(str(text),header=0)[0]
            if df.empty is True:
                break
            else:
                pn = pn + 1
                DF =DF.append(df)
        except:
            break
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.drop('详细',axis=1)
    DF=DF.set_index('股票代码')
    DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))
    DF['date']=str(year)+'_'+str(quarter).zfill(2)
    name=list(DF.columns)
    name.remove('股票名称')
    name.remove('date')
    name.remove(name[-1])
    name.remove(name[-1])
    #print(name)
    for label in name:
        DF[label]=DF[label].astype(float)#map(lambda x: np.where(len(x)>0,float(x),x))
    return DF

def forcast(year,quarter):
    pn=1
    DF=pd.DataFrame()
    ws._write_head()
    while True:
        try:
            ws._write_console()
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vFinanceAnalyze/kind/performance/index.phtml?s_i=&s_a=&num=60&s_c=&reportdate={0}&quarter={1}&p={2}'.format(year,quarter,pn)
            r=requests.get(url,headers=hds())
            r=r.content.decode('gbk')
            html=BeautifulSoup(r,'lxml')
            text=html.find(id='dataTable')
            df=pd.read_html(str(text),header=0)[0]
            if df.empty is True:
                break
            else:
                pn = pn + 1
                DF =DF.append(df)
        except:
            break
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.set_index('股票代码')
    DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))
    return DF

def forcast_share(code):
    DF=pd.DataFrame()
    ws._write_head()
    try:
        ws._write_console()
        url='http://vip.stock.finance.sina.com.cn/q/go.php/vFinanceAnalyze/kind/performance/index.phtml?symbol={0}'.format(code)
        r=requests.get(url,headers=hds())
        r=r.content.decode('gbk')
        html=BeautifulSoup(r,'lxml')
        text=html.find(id='dataTable')
        df=pd.read_html(str(text))[0]
        if df.empty is False:
            DF =DF.append(df)
            DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
            DF=DF.drop(8,axis=1)
            DF.columns=['code','name','type','pdate','rpdate','summary','eps_l','Up_Down']
            DF=DF.set_index('code')
            DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))
        return DF
    except Exception as e:
        print(e)
        #pass

def YJKB(year,quarter):
    pn=1
    DF=pd.DataFrame()
    ws._write_head()
    while True:
        try:
            ws._write_console()
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vFinanceAnalyze/kind/news/index.phtml?s_i=&s_a=&s_c=&reportdate={0}&quarter={1}&p={2}'.format(year,quarter,pn)
            r=requests.get(url,headers=hds())
            r=r.content.decode('gbk')
            html=BeautifulSoup(r,'lxml')
            text=html.find(id='dataTable')
            df=pd.read_html(str(text),header=0)[0]
            if df.empty is True:
                break
            else:
                pn = pn + 1
                DF =DF.append(df)
        except:
            break
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.set_index('股票代码')
    DF.index=DF.index.map(lambda x: str(x).split('.')[0].zfill(6))
    name=DF.columns
    name.remove('股票名称')
    name.remove(name[-1])

    for label in name:
        DF[label]=DF[label].astype(float)
    return DF

if __name__=="__main__":
    #df=profit(2017,1)
    year=2017
    quarter=4
    code='600160'
    #df=profit(year,quarter)
    #df=operation(year,quarter)
    #dd=grow(year,quarter)
    #ds=mainindex(year,quarter)
    dfs=forcast(year,quarter)
    #d=forcast_share(code)
    #s=YJKB(year,quarter)
