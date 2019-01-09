#!/usr/bin/env python3
# -*-coding:utf-8-*-

"""
获取在美国NasdaQ上市股票的历史交易数据。
"""
from selenium import webdriver
import time,sys
import pandas as pd
from bs4 import BeautifulSoup
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.select import Select
"""
import re
from io import StringIO
import webdriver.mydriver as dr
driver=dr.Firefox_hdless()
"""
if sys.platform=="linux":
    driver=webdriver.Chrome('/usr/bin/chromedriver')
else:
    driver=webdriver.Chrome()
data=pd.DataFrame()
driver.set_window_size(480, 800)
"""
#driver = webdriver.PhantomJS()
#driver=webdriver.Chrome()
#driver=dr.Firefox_hdless()
def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return
def _str2fl(x):
    if u'万' in x:
        x=x.replace(u'万','')
        x=float(x)
    elif u'亿' in x:
        x=x.replace(u'亿','')
        x=float(x)*10000
    elif '%' in x:
        x=x.replace('%','')
        x=float(x)
    elif u'千' in x:
        x=x.replace(u'千','')
        x=float(x)/10
    elif x.strip()=='-':
        x=x.replace('-','')
    return x


def driver_share_cashflow(code):
    """
    获取某只股票近100个交易日的现金流量数据
    Parameter:
      code:上海深圳交易所的股票代码，like 000039
    -------------------------------------------  
     Return:
       DATAFRAME:
       -----------------------------------------
          收盘价:收盘价，单位元
          涨跌幅：与上一交易日涨跌幅，% 
          主力净流入：单位万元
          主力净流入占比：单位%
          超大单净流入：单位万元
          超大单净流入占比：单位%
          大单净流入：单位万元
          大单净流入占比：单位%
          中单净流入：单位万元
          中单净流入占比：单位%
          小单净流入：单位万元
          小单净流入占比：单位%
    """
    url='http://data.eastmoney.com/zjlx/%s.html'%code
    driver.get(url)
    waitForLoad(driver)
    ts=BeautifulSoup(driver.page_source,'lxml')
    tb=ts.find(id="dt_1")
    df=pd.read_html(str(tb))[0]
    df=df.dropna(how='all',axis=1)
    names=['日期', '收盘价', '涨跌幅', '主力净流入', \
               '主力净流入占比', '超大单净流入', '超大单净流入占比',\
               '大单净流入','大单净流入占比', '中单净流入','中单净流入占比',\
               '小单净流入', '小单净流入占比']
    name=[ '涨跌幅', '主力净流入', \
               '主力净流入占比', '超大单净流入', '超大单净流入占比',\
               '大单净流入','大单净流入占比', '中单净流入','中单净流入占比',\
               '小单净流入', '小单净流入占比']
    df.columns=names

    for label in name:
        df[label]=df[label].map(lambda x: _str2fl(x))

    df=df.set_index('日期')
    df=df.sort_index()
    df=df.replace('',0)
    df=df.applymap(lambda x:float(x))
    df.index=pd.to_datetime(df.index,format='%Y-%m-%d')
    return df        

def dapan_cashflow():
    """
    获取某只股票近100个交易日的现金流量数据
    Parameter:
      code:上海深圳交易所的股票代码，like 000039
    -------------------------------------------  
     Return:
       DATAFRAME:
       -----------------------------------------
          收盘价:收盘价，单位元
          涨跌幅：与上一交易日涨跌幅，% 
          主力净流入：单位万元
          主力净流入占比：单位%
          超大单净流入：单位万元
          超大单净流入占比：单位%
          大单净流入：单位万元
          大单净流入占比：单位%
          中单净流入：单位万元
          中单净流入占比：单位%
          小单净流入：单位万元
          小单净流入占比：单位%
    """
    url='http://data.eastmoney.com/zjlx/dpzjlx.html'
    driver.get(url)
    waitForLoad(driver)
    ts=BeautifulSoup(driver.page_source,'lxml')
    tb=ts.find(id="dt_1")
    df=pd.read_html(str(tb))[0]
    df=df.dropna(how='all',axis=1)
    names=['日期', '上证收盘价', '上证涨跌幅','深证收盘价', '深证涨跌幅', '主力净流入', \
               '主力净流入占比', '超大单净流入', '超大单净流入占比',\
               '大单净流入','大单净流入占比', '中单净流入','中单净流入占比',\
               '小单净流入', '小单净流入占比']
    name=[  '上证涨跌幅', '深证涨跌幅','主力净流入', \
               '主力净流入占比', '超大单净流入', '超大单净流入占比',\
               '大单净流入','大单净流入占比', '中单净流入','中单净流入占比',\
               '小单净流入', '小单净流入占比']
    df.columns=names

    for label in name:
       df[label]=df[label].map(lambda x: _str2fl(x))

    df=df.set_index('日期')
    df=df.sort_index()
    df=df.replace('',0)
    df=df.applymap(lambda x:float(x))    
    df.index=pd.to_datetime(df.index,format='%Y-%m-%d')
    return df            

if __name__=="__main__":
    #df=driver_share_cashflow('000039')
    dd=dapan_cashflow()
