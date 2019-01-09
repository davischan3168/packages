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
try:
    from io import StringIO
except:
    from pandas.compat import StringIO
from bs4 import BeautifulSoup

def _tofl(x):
    try:
        return float(x)
    except:
        return x
def get_mk_data(code):
    """
    获取股票的历史交易数据
    """
    df=pd.DataFrame()
    ty=dt.datetime.today().year
    #years=range(1998,ty+1)
    years=range(ty-3,ty+1)
    for year in years:
        for season in [1,2,3,4]:
            url='http://quotes.money.163.com/trade/lsjysj_{2}.html?year={0}&season={1}'.format(year,season,code)
            try:
                #print(url)
                r=requests.get(url,headers=hds())
                soup=BeautifulSoup(r.text,'lxml')
                tb=soup.find(attrs={"class":"table_bg001 border_box limit_sale"})
                df=df.append(pd.read_html(str(tb))[0])
                #print(df.head())
            except:
                pass
    df=df.drop(0,axis=0)
    df=df.set_index('日期')
    df=df.sort_index()
    df=df.applymap(lambda x: _tofl(x))
    return df
                
def get_cf(code):
    """
    quotes.money.163.com
    获取股票的买卖现金流量
    """
    df=pd.DataFrame()

    url='http://quotes.money.163.com/trade/lszjlx_{0},0.html'.format(code)
    while True:
        try:
            
            r=requests.get(url,headers=hds())
            soup=BeautifulSoup(r.text,'lxml')
            
            tb=soup.find('table',attrs={'class':"table_bg001 border_box"})
            df=df.append(pd.read_html(str(tb))[0])
            df=df.drop(0,axis=0)
        
            page=soup.find('a',text='下一页')
            url='http://quotes.money.163.com'+page.get('href')
        except:
            break
        
    df=df.set_index('日期')
    df=df.sort_index()
    df=df.applymap(lambda x: _tofl(x))    
    return df
    
if __name__=="__main__":
    #df=get_mk_data('600160')
    df=get_cf('600160')
