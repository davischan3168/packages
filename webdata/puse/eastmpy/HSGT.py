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

def HK_HSGT_EM(mtype='HGT',pageno=1):
    """
    mtype: HGT沪港通，SGT深港通，GHT港沪通，GST港深通
    return:
        DRCJJME:当日成交净买额（单位：万元）
        DRYE:   当日余额（单位：万元）
        DRZJLR: 当日资金流入（单位：万元）
        LCG:    领涨股
        LCGCode:领涨股股票代码
        LCGZDF:领涨股涨跌幅%
        LSZJLR:历史资金累计流入（单位：万元）
        MCCJE: 卖出成交额（单位：万元）
        MRCJE: 买入成交额（单位：万元）
        MarketType:
        SSEChange:交易所指数
        SSEChangePrecent： 指数涨跌幅
    """
    url=wt.HSGT_url[mtype].format(pageno,'{%22data%22:(x),%22pages%22:(tp)}')
    r=requests.get(url,headers=hds())
    text=r.text

    text=text.split('=')[1]
    data=json.loads(text)

    df=pd.DataFrame(data['data'])
    df.loc[:,'DetailDate']=df.loc[:,'DetailDate'].map(lambda x:x[:10])
    df=df.set_index('DetailDate')
    df=df.sort_index()
    return df

def _hk_ggt(url):
    r=requests.get(url,headers=hds())
    text=r.text.split('123=')[1]
    data=json.loads(text)
    s='\n'.join(data['rank'])
    df=pd.read_csv(StringIO(s),header=None)

    return df
    
def HK_GGT_EM():
    """
    获取港股通的股票数据，即通过国内交易系统可以购买香港市场的股票
    """
    urlh='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C.mk0144&sty=CTF&sortType=C&sortRule=-1&page=1&pageSize=20000&js=var%20quote_123%3d{%22rank%22:[(x)],%22pages%22:(pc)}&token=44c9d251add88e27b65ed86506f6e5da&jsName=quote_123&_g=0.5358432093635201'
    urls='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C.mk0146&sty=CTF&sortType=C&sortRule=-1&page=1&pageSize=20000&js=var%20quote_123%3d{%22rank%22:[(x)],%22pages%22:(pc)}&token=44c9d251add88e27b65ed86506f6e5da&jsName=quote_123&_g=0.15627210377715528'

    uls=[urls,urlh]
    df=pd.DataFrame()
    for url in uls:
        #print(url)
        df=df.append(_hk_ggt(url))

    df=df.drop([0,6,7],axis=1)
    df.columns=['code','name','close','chg','chg%','unk','volume','amount','open','pre.close','high','low','turnover','PE']    
    df=df.drop_duplicates()
    df=df.applymap(lambda x: wt._tofl(x))
    df['code']=df['code'].map(lambda x:str(x).zfill(5))
    #df=df.sort_values(by='chg%',ascending=False)
    return df

def HK_HSG_EM():
    hurl='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C.BK07071&sty=FCOIATA&sortType=C&sortRule=-1&page=1&pageSize=20000&js=var%20quote_123%3d{%22rank%22:[(x)],%22pages%22:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.785481323255226'
    surl='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C.BK08041&sty=FCOIATA&sortType=C&sortRule=-1&page=1&pageSize=20000&js=var%20quote_123%3d{%22rank%22:[(x)],%22pages%22:(pc)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c&jsName=quote_123&_g=0.03943358431570232'
    
    uls=[surl,hurl]
    df=pd.DataFrame()
    for url in uls:
        #print(url)
        df=df.append(_hk_ggt(url))

    df=df.drop([0,13,14,15,16,17,18,19,20],axis=1)
    df.columns=['code','name','close','chg','chg%','apmature','volume','amount','pre.close','open','high','low','chg_5m','LB','turnover','PE']    
    df=df.drop_duplicates()
    df=df.applymap(lambda x: wt._tofl(x))
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    #df=df.sort_values(by='chg%',ascending=False)
    return df

def HK_comp2indu_EM(code):
    url='http://quote.eastmoney.com/hk/{0}.html?'.format(code)
    print(url)
    r=requests.get(url,headers=hds())
    text=r.content.decode('gbk')

    soup=BeautifulSoup(text,'lxml')
    tb=soup.find(id='financial_analysis')
    df=pd.read_html(str(tb))[0]
    df.iloc[2,0]=0
    return df



    
if __name__=="__main__":
    #df=get_HK_HSGT_EM()
    #dd=get_HK_HSGT_EM(mtype='SGT')
    #df=HK_GGT_EM()
    #df=HK_HSG_EM()
    dff=HK_comp2indu_EM(sys.argv[1])
