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

def _settle(url):
    r=requests.get(url,headers=hds())
    text=r.text

    data=json.loads(text)
    try:
        data=json.loads(data)
    except:
        pass
    
    df=pd.DataFrame(data)
    
    name=list(df.columns)[:4]
    name.extend(list(df.iloc[0,4:]))
    df.columns=name
    df=df.drop(0,axis=0)
    
    del df['Indent']
    del df['IsBold']
    del df['IsShowChart']
    
    df=df.set_index("IndexName")
    df=df.dropna(how='all',axis=0)
    #df=df.dropna(how='all',axis=0)
    
    df=df.applymap(lambda x: wt._tofl(x))
    df=df.T
    df=df.sort_index()
    df=df.replace('-',np.nan)
    return df

def HK_Summary_EM(code):
    """
    查询香港股票的财务分析摘要
    http://hkf10.eastmoney.com/html_HKStock/index.html?securitycode=00005&name=dailyData
    --------------------------
    code:为香港的股票代码，为5位数
    """
    url=wt.fas_url.format(code,wt.yearl)
    df=_settle(url)
    return df



def HK_EPS_Index_EM(code):
    """
    查询香港股票的每股指标
    http://hkf10.eastmoney.com/html_HKStock/index.html?securitycode=00005&name=dailyData
    --------------------------
    code:为香港的股票代码，为5位数
    """
    url=wt.eps_index.format(code,wt.yearl)
    df=_settle(url)
    return df

def HK_Profit_Quantity_EM(code):
    """
    查询香港股票的盈利能力与收益质量
    http://hkf10.eastmoney.com/html_HKStock/index.html?securitycode=00005&name=dailyData
    --------------------------
    code:为香港的股票代码，为5位数
    """
    url=wt.ylnl_sy_url.format(code,wt.yearl)
    df=_settle(url)
    return df

def HK_Captital_Repay_EM(code):
    """
    查询香港公司的资本结果与偿债能力数据
    http://hkf10.eastmoney.com/html_HKStock/index.html?securitycode=00005&name=dailyData
    --------------------------
    code:为香港的股票代码，为5位数
    """
    url=wt.zbjg_cznl_url.format(code,wt.yearl)
    df=_settle(url)
    return df

def HK_Grow_Ability_EM(code):
    """
    查询香港公司的成长能力
    http://hkf10.eastmoney.com/html_HKStock/index.html?securitycode=00005&name=dailyData
    --------------------------
    code:为香港的股票代码，为5位数
    """
    url=wt.cznl_url.format(code,wt.yearl)
    df=_settle(url)
    return df.T

def HK_dividend_EM(code):
    url=wt.div_url.format(code,wt.yearl)
    #df=_settle(url)
    r=requests.get(url,headers=hds())
    text=r.text

    data=json.loads(text)
    df=pd.DataFrame(data)
    df.columns=df.iloc[0,:].tolist()
    df=df.set_index('除权日')
    df=df.applymap(lambda x: wt._tofl(x))
    df=df.T
    df=df.sort_index()
    df=df.replace('-',np.nan)
    df=df.drop('除权日',axis=1)
    df=df.dropna(how='all',axis=1)
    #print(data)
    return df
    
if __name__=="__main__":
    #df=HK_Profit_Quantity_EM(sys.argv[1])
    #dd=HK_Grow_Ability_EM(sys.argv[1])
    df=HK_dividend_EM(sys.argv[1])
