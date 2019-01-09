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
import webdata.puse.aastockpy.cont as wc
scompile=re.compile(r'(\d+).HK')


t4=['Symbol','Name','Last','Cur.R.(X)','Quick.R.(X)','ROA','ROE','GP Margin','NP Margin','Payout','Debt/Equity','Yr end']
t3= ['Symbol', 'Name', 'Last', '3-Year','1-Year','6-Month', '3-Month', '1-Month', '1-Week', 'YTD']
t5=['Symbol', 'Name', 'Last', 'Capital Adq.', 'Liq.Fund/Deposits', \
    'Deposits/Assets', 'Loans/Deposits', 'Net Int. Spr.', 'Net Int. Margin','Yr end']

def HK_peer_AAS(code,mtype=6):
    """
    获得在香港交易所上市的同行业股票的相关数据信息
    ---------------------------
    code:香港联交所股票代码
    mtype:1--为概览,2--波幅,3--股价表现,4--财务比率,
          5--财务比率（银行）,6--盈利摘要,为整数int
    
    Return:
          DataFrame:
             Name/Symbol: 股票名称和代码
             Last       ：现价
             Chg.       : 升跌
             Chg.%
             Volume     ：成交量
             Turnover   ：成交金额
             P/E
             P/B
             Yield       :收益率
             Market Cap  :市值
        
    """

    url='http://www.aastocks.com/en/stocks/analysis/peer.aspx?symbol={0}&t={1}&s=5&o=0&p=4&hk=0&export=1'.format(code,mtype)

    r=requests.get(url,headers=hds(),stream=True)

    df=pd.read_html(r.text,header=0)[0]

    if int(mtype)==3:
        df=df.drop('Unnamed: 3',axis=1)
        df.columns=t3
        df=df.drop(0,axis=0)
        pass
    elif int(mtype)==4:
        df.columns=t4
        df=df.drop(0,axis=0)
    elif int(mtype) == 5:
        df.columns=t5
        df=df.drop(0,axis=0)
        
    try:
        df.loc[:,'Symbol']=scompile.findall(df.loc[:,'Name/Symbol'].to_string())
        df=df.set_index('Symbol')
    except:
        df.loc[:,'Symbol']=scompile.findall(df.loc[:,'Symbol'].to_string())
        df=df.set_index('Symbol')
        pass
    finally:
        pass

    df=df.applymap(lambda x: wc._tofl(x))
    df=df.applymap(lambda x: wc._tofl(x))
    return df

def HK_peerall_AAS(code):
    df1=HK_peer_AAS(code,mtype=1)
    df2=HK_peer_AAS(code,mtype=2)
    df3=HK_peer_AAS(code,mtype=3)
    df4=HK_peer_AAS(code,mtype=4)
    df6=HK_peer_AAS(code,mtype=6)
    try:
        df5=HK_peer_AAS(code,mtype=5)
        df=pd.concat([df1,df2,df3,df4,df5,df6],axis=1)
    except:
        df=pd.concat([df1,df2,df3,df4,df6],axis=1)
        pass
    
    
    df=df.T
    df=df.drop_duplicates()
    df=df.T
    return df
    
if __name__=="__main__":
    #df=HK_peer_AAS('00005',1)
    df=HK_peerall_AAS(sys.argv[1])
