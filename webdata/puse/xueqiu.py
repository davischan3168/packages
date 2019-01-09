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

def _tofl(x):
    try:
        return float(x)
    except:
        return x
def get_finance_index_XQ(code):
    """
    获取股票的历史交易数据
    """
    
    if code[0] in ['6','9']:
        code='SH'+code
    if code[0] in ['0','2','3']:
        code='SZ'+code

    url='https://xueqiu.com/stock/f10/finmainindex.json?symbol={0}&page=1&size=400'.format(code)
    
    r=requests.get(url,headers=hds())
    text=r.text
    data=json.loads(text)
    df=pd.DataFrame(data["list"])

    #df=df.drop(0,axis=0)
    #df=df.set_index('日期')
    #df=df.sort_index()
    #df=df.applymap(lambda x: _tofl(x))
    return df
                

    
if __name__=="__main__":
    #df=get_mk_data('600160')
    #f=get_cf('600160')
    df=get_finance_index_XQ(sys.argv[1])
