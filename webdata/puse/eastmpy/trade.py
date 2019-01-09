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


def HK_trade_data_EM(code):
    """
    查询香港股票的每日交易统计数据
    http://hkf10.eastmoney.com/html_HKStock/index.html?securitycode=00005&name=dailyData
    --------------------------
    code:为香港的股票代码，为5位数
    """
    url='http://hkf10.eastmoney.com/F9HKStock/GetStockDailyMarketDataList.do?securityCode={0}.HK&yearList=2017,2016,2015,2014,2013&dateSearchType=1&rotate=1&seperate=0&order=desc&cashType=0&exchangeValue=1&customSelect=0&CurrencySelect=0'.format(code)
    #print(url)
    r=requests.get(url,headers=hds())
    text=r.text
    data=json.loads(text)
    df=pd.DataFrame(data)
    df=df.set_index('TRADEDATE')
    df=df.sort_index()
    df.index.name='date'
    df=df.applymap(lambda x: wt._tofl(x))
    return df

def HK_AH_data_EM(code,start='1990-01-01',end=wt.today.strftime('%Y-%m-%d')):
    """
    查询香港股票的每日交易统计数据
    http://hkf10.eastmoney.com/html_HKStock/index.html?securitycode=00005&name=dailyData
    --------------------------
    code:为香港的股票代码，为5位数
    """
    url=wt.AH_url.format(code,start,end)
    #print(url)
    
    r=requests.get(url,headers=hds())
    text=r.text
     
    #print(text)
    data=json.loads(text)

    df=pd.DataFrame(data['list'])
    df=df.set_index('TRADEDATE')
    df.index.name='date'
    df=df.sort_index()
    return df

def HK_Value_Ass_EM(code):
    """
    查询香港股票的每日交易统计数据
    http://hkf10.eastmoney.com/html_HKStock/index.html?securitycode=00005&name=dailyData
    --------------------------
    code:为香港的股票代码，为5位数
    """
    url=wt.VA_url.format(code,wt.yearl)

    r=requests.get(url,headers=hds())
    text=r.text

    data=json.loads(text)
    data=json.loads(data)
    df=pd.DataFrame(data)

    del df['Indent']
    del df['IsBold']
    del df['IsShowChart']

    name=list(df.iloc[0,:])
    d=name.pop(0)
    name.insert(0,'IndexName')
    df.columns=name
    df=df.drop(0,axis=0)

    df.iloc[44,0]=df.iloc[44,0][:9]
    df.iloc[43,0]=df.iloc[43,0][:6]
    df.iloc[42,0]=df.iloc[42,0][:4]
    df.iloc[41,0]=df.iloc[41,0][:3]

    df=df.reset_index(drop=True)
    df=df.drop(0,axis=0)

    for i in range(8):
        df.iloc[5*i+1:5*i+5,0]=df.iloc[5*i,0]+df.iloc[5*i+1:5*i+5,0]

    df=df.reset_index(drop=True)
    df=df.drop([0,5,10,15,20,25,30,35,44,45],axis=0)
    df=df.iloc[0:-2,:]
    df=df.set_index('IndexName')
    return df

def get_realtime_EM(code):
    if code[0] in ['6','9']:
        code=code+'1'
    elif code[0] in ['0','2','3']:
        code=code+'2'
    
    url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd={0}&sty=DCRRB&st=z&sr=&p=&ps=&cb=&js=var%20zjlx_hq={1}&token=3a965a43f705cf1d9ad7e1a3e429d622&rt=50167288'.format(code,'{%22quotation%22:[(x)]}')

    r=requests.get(url)
    text=r.text.split('hq=')[1]
    data=json.loads(text)
    s=data['quotation']
    dd=pd.read_csv(StringIO(s[0]),header=None)
    dd=dd.drop(0,axis=1)
    dd.columns=['code','name','close','chg','chg%','amplitude','volume','amount','pre.close','open','high','low','turnover','LB','PE']
    return dd
    
if __name__=="__main__":
    #df=HK_trade_data_EM(sys.argv[1])
    #df=HK_AH_data_EM(sys.argv[1])
    #dd=HK_Value_Ass_EM(sys.argv[1])
    df=get_realtime_EM(sys.argv[1])
