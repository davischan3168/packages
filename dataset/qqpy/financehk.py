#!/usr/bin/env python3
# -*-coding:utf-8-*-
"""
获得公司的基本信息和财务信息
"""
import requests,json
from io import StringIO
import re,sys,os
from bs4 import BeautifulSoup
import pandas as pd
import lxml.html
from lxml import etree
import datetime as dt
import webdata.puse.qqpy.cont as wt
from webdata.util.hds import user_agent as hds

def HK_Finance_qq(tick,start=1990,end=dt.datetime.today().year,mtype='bs'):
    """
    获取某家上市公司的财务数据，资产负债表，利润表、现金流量表
    -------------------------------
    tick: 五位数的香港上市公司代码，如00005
    start:开始年度，为四位数的数字
    end: 结束年度，为四位数的数字，如2017
    mtype:类型，bs:主要是资产负债表；ins:损益表；cfl:现金流量表。
    --
    return ：
        DataFrame
    """
    url=wt.fin_hk[mtype].format(tick,start,end)
    r=requests.get(url,headers=hds())
    text=r.content.decode('utf8')
    #print(text)

    #text=text.split('(')[1].replace('}})','}}')
    data=json.loads(text)
    df=pd.DataFrame(data['data']['data'])
    try:
        df=df.set_index('fd_repdate')
    except Exception as e:
        print(e)
        pass
    try:
        del df['fd_type']
        del df['fd_unit']
        del df['fd_currency_id']
    except Exception as e:
        print(e)
        pass
    
    return df
    

if __name__=="__main__":
    tick='01203'
    dd=Finance_qqhk(sys.argv[1])
