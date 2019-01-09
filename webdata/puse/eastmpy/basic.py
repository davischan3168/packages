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

def HK_Basic_info_EM(code):
    """
    查询香港股票的每日交易统计数据
    http://hkf10.eastmoney.com/html_HKStock/index.html?securitycode=00005&name=dailyData
    --------------------------
    code:为香港的股票代码，为5位数
    """
    url=wt.Review_url.format(code,wt.yearl)

    'http://hkf10.eastmoney.com/F9HKStock/GetStockBussinessViewList.do?securityCode={0}.HK&yearList=2017,2016,2015,2014,2013&dateSearchType=1&=0&rotate=0&seperate=0&order=desc&cashType=0&exchangeValue=0'.format(code)
    #print(url)
    r=requests.get(url,headers=hds())
    text=r.text
    #print(text)
    data=json.loads(text)
    df=pd.DataFrame(data)
    return df

def HK_Preview_EM(code):
    """
    查询香港股票的每日交易统计数据
    http://hkf10.eastmoney.com/html_HKStock/index.html?securitycode=00005&name=dailyData
    --------------------------
    code:为香港的股票代码，为5位数
    """
    url=wt.Future_url.format(code,wt.yearl)

    r=requests.get(url,headers=hds())
    text=r.text
    #print(text)
    data=json.loads(text)
    df=pd.DataFrame(data)
    return df
    
if __name__=="__main__":
    df=HK_Basic_info_EM(sys.argv[1])
