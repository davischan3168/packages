#!/usr/bin/env python3
# -*-coding:utf-8-*-
"""
获得公司的基本信息和财务信息
"""
import requests
from io import StringIO
import re,sys,os
from bs4 import BeautifulSoup
import pandas as pd
import lxml.html
from lxml import etree
import webdata.puse.aastockpy.cont as wt
from webdata.util.hds import user_agent as hds

def _basic(url):
    r=requests.get(url,headers=hds())
    html=lxml.html.parse(StringIO(r.text))
    res=html.xpath('//table[starts-with(@class,"cnhk-cf")]//tr')
    try:
        if wt.PY3:
            sarr = [etree.tostring(node).decode('utf-8') for node in res]
        else:
            sarr = [etree.tostring(node) for node in res]
        sarr = ''.join(sarr)
    
        sarr = '<table>%s</table>'%sarr
        df = pd.read_html(sarr,header=0)[0]
        return df
    except Exception as e:
        print(e)
        return

def HK_basic_info_AAS(code,mtype='basic-information'):
    """
    code:为在香港连交所上市的股票代码，like 00005
    mtype:为公司的资料的类型
          company-profile：公司的概括资料
          company-information：公司资料
          basic-information：公司的基本数据
          dividend-history：  分红记录
          securities-buyback：证券回购
    """
    url='http://www.aastocks.com/tc/stocks/analysis/company-fundamental/{1}?symbol={0}'.format(code,mtype)
    df=_basic(url)
    if df is not None:
        if df.empty is False:
            df=df.applymap(lambda x:wt._tofl(x))
    return df

def HK_finance_info_AAS(code,mtype='financial-ratios',p=4):
    """
    code:为在香港连交所上市的股票代码，like 00005
    mtype:为公司的资料的类型
          financial-ratios： 财务比率
          profit-loss：     损益表
          cash-flow：        现金流量表
          balance-sheet：    资产负债表
          earnings-summary：  盈利摘要
    p:表示中期或全年的数据,若p为4则为全年，p=2则为中期数据
    """
    url='http://www.aastocks.com/tc/stocks/analysis/company-fundamental/{1}?symbol={0}&period={2}'.format(code,mtype,p)
    df=_basic(url)
    if df is not None:
        if df.empty is False:
            df=df.applymap(lambda x:wt._tofl(x))
    df=df.dropna(how='all',axis=1)
    df=df.set_index('截止日期')
    df=df.T
    return df

if __name__=="__main__":
    code='00005'
    df=HK_basic_info('00005')
    dd=HK_finance_info(code)
