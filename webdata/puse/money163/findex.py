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


def get_mainindex_m163(code,mytype='report'):
    """
    """    
    url=wc.mainindex_url %(code,mytype)
    r=requests.get(url,stream=True)
    text=r.text.replace('\r\n','\n')
    #f=open('mainindex_%s_%s.csv'%(code,mytype),'w')
    #f.write(text)
    #f.close()
    df=pd.read_csv(StringIO(text),header=0)
    df=df.dropna(how='all',axis=1)
    df=df.set_index('报告日期')
    df=df.T
    df=df.applymap(lambda x: np.where(x=='--',np.nan,wc._tofl(x)))
    return df
                
def get_finance_index_m163(code,mytype='report',ids='ylnl'):
    """
    """
    url=wc.finance_analysis_url.format(code,mytype,ids)
    r=requests.get(url,stream=True)
    text=r.text.replace('\r\n','\n')
    #f=open('financeindex_%s_%s_%s.csv'%(code,mytype,ids),'w')
    #f.write(text)
    #f.close()
    df=pd.read_csv(StringIO(text),header=0)
    df=df.dropna(how='all',axis=1)
    df=df.set_index('报告日期')
    df=df.T
    df=df.applymap(lambda x: np.where(x=='--',np.nan,wc._tofl(x)))
    return df

def get_finance_summary_m163(code,mytype='report'):
    """
    """
    url=wc.finace_summary_url[mytype].format(code)
    r=requests.get(url,stream=True)
    text=r.text.replace('\r\n','\n')
    #f=open('financesummary_%s_%s.csv'%(code,mytype),'w')
    #f.write(text)
    #f.close()
    df=pd.read_csv(StringIO(text),header=0)
    df=df.dropna(how='all',axis=1)
    df=df.set_index('报告期')
    df=df.T
    df=df.applymap(lambda x: np.where(x=='--',np.nan,wc._tofl(x)))
    return df
    
if __name__=="__main__":
    #df=mainindex_data('002182')
    #dd=finance_index_data(code='002182',ids='yynl')
    sd=finance_summary_data('002182')
