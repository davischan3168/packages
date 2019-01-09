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


def HK_TradeLog_AAS(url):
    """
    获取香港联交所股票的近2天的历史交易数据
    ----------------------
    url:解析得到
    -------------
    Time：时间
    Amount:交易金额，单位港元
    Volume：交易单位，股
    Type:   交易类型，A为买入，B为卖出，U为其他
    """
    df=pd.DataFrame()

    s=requests.Session()
    r=s.get(url)
    #r=requests.get(url,headers=hds(),stream=True)
    text=r.text
    text=text.split('#')[1]
    text=text.replace('|','\n')

    df=pd.read_csv(StringIO(text),header=None,sep=';')
    df=df.drop(2,axis=1)
    df.columns=['Time','Volume','Price','Type']
    df['Time']=df['Time'].map(lambda x: wc._i2t(x))
    df=df.set_index('Time')
    return df

    
if __name__=="__main__":
    #url='http://tldata.aastocks.com/TradeLogServlet/getTradeLog?id=01988.HK&date=20170705&u=13&t=20170705162119&d=4288CD3A'
    df=HK_TradeLog(sys.argv[1])
    #dff=TradeLog(url)
