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
import webdata.puse.money163.cons as wc


def get_BCISCF_m163(code,bic='xjllb',mytype='report'):
    """
    code:股票代码
    bic:zcfzb（资产负债表）,lrb（利润表）,xjllb（现金流量表）三个参数
    mytype:report, year,两个参数
    """    
    url=wc.bic_url[mytype].format(code,bic)
    #print(url)
    r=requests.get(url,stream=True)
    text=r.text.replace('\r\n','\n')
    
    #f=open('bic_%s_%s_%s.csv'%(code,bic,mytype),'w')
    #f.write(text)
    #f.close()
    
    df=pd.read_csv(StringIO(text),header=0)
    df=df.dropna(how='all',axis=1)
    #print(df.head())
    
    name=list(df.columns)
    name=[s.strip() for s in name]
    df.columns=name
    
    df=df.set_index('报告日期')
    df=df.T
    df=df.applymap(lambda x: np.where(x=='--',np.nan,wc._tofl(x)))
    return df
    
if __name__=="__main__":
    code='002182'
    #df=BCISCF_data(code)
    df=get_BCISCF_m163(sys.argv[1])
