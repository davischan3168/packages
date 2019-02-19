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
#,start=1990,end=dt.datetime.today().year,mtype='bs')
def HK_trademin_qq(tick):
    """
    获取某家上市公司的财务数据，资产负债表，利润表、现金流量表
    -------------------------------
    tick: 五位数的香港上市公司代码，如00005
    --
    return ：
        DataFrame
           price:价格
           volume:累计成交量
           dvolume:5min 的成交量
    """
    tick='hk%s'%tick
    url='http://web.ifzq.gtimg.cn/appstock/app/hkMinute/query?_var=min_data_{0}&code={0}'.format(tick)

    r=requests.get(url,headers=hds())
    text=r.text.split("=")[1]
    
    data=json.loads(text)
    lines=data['data'][tick]['data']['data']
    dataset=[]
    for l in lines:
        dataset.append(l.split(' '))
        
    df=pd.DataFrame(dataset)

    df.columns=['time','price','volume']
    df['time']=df['time'].map(lambda x:'%s:%s'%(x[:2],x[2:]))
    
    df=df.set_index('time')
    df=df.applymap(lambda x:float(x))
    df['dvolume']=df['volume'] - df['volume'].shift()
    return df
    

if __name__=="__main__":
    #tick='01203'
    dd=HK_trademin_qq(sys.argv[1])
