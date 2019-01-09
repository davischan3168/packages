#!/usr/bin/env python3
# -*-coding:utf-8-*-
"""
限售解禁数据 的查询
"""

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

name=['date','rzye','rzmre','rzche','rqylje','rqye','rqmce','rqche','rqye']

def xsjj(begin,end):
    """
    查询限售解禁的数据,主要是当前数据的前20页的数据
    -----------------
    Return:
        DataFrame
    """
    pn=1
    DF=pd.DataFrame()
    ws._write_head()
    while True:
        try:
            ws._write_console()
            url='http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/xsjj/index.phtml?bdate={0}&edate={1}&showall=%CF%D4%CA%BE%C8%AB%B2%BF&p={2}'.format(begin,end,pn)
            r=requests.get(url)
            #print(url)
            r=r.content.decode('gbk')
            html=BeautifulSoup(r,'lxml')
            sarr=html.find(id='dataTable')
            df=pd.read_html(str(sarr),header=0)[0]
            DF =DF.append(df)
            pn=pn+1
            if pn > 50:
                break
            if df.empty is True:
                break
        except:
            break
        
    DF=DF.applymap(lambda x:np.where(x=='--',np.nan,x))
    DF=DF.drop_duplicates()
    DF['代码']=DF['代码'].map(lambda x:str(x).split('.')[0].zfill(6))
    return DF

if __name__=="__main__":
    begin='2015-06-10'
    end='2017-06-17'
    #code='000333'
    #ds=dzjy_share(code,begin,end)
    df=xsjj(begin,end)
