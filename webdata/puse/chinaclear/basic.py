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
import datetime as dt

def stock_pledge():
    """
    Return:
    -----------------------
        code:证券代码	
        name:证券简称	
        pledge_no:质押笔数(笔)	
        volume_free:无限售股份质押数量(万)	
        volume_unfr:有限售股份质押数量(万)	
        total_shares:A股总股本(万)	
        pledge_ratio:质押比例（%）

    """
    url='http://www.chinaclear.cn/cms-rank/downloadFile?queryDate=%s&type=proportion'

    today=dt.datetime.today()
    if today.isoweekday() in [6,7]:
        day=dt.datetime.strftime(today,'%Y.%m.%d')
    else:
        lsd=today-dt.timedelta(days=(today.isoweekday()+1))
        day=dt.datetime.strftime(lsd,'%Y.%m.%d')

    urll=url%day

    df=pd.read_excel(urll,sheet_name="Sheet1",skiprows=2)
    df=df.dropna(axis=1)
    df.columns=['code','name','pledge_no','volume_free','volume_unf','totall_shares','pledge_ratio']
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    for label in ['pledge_no','volume_free','volume_unf','totall_shares','pledge_ratio']:
        df[label]=df[label].map(lambda x:float(x))
    df=df.sort_values(by='pledge_ratio',ascending=False)
    return df

if __name__=="__main__":
    df=stock_pledge()

