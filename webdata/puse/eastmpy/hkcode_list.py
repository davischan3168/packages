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

def HK_List_EM():
    """
    获取香港上市公司的股票列表
    """
    url=wt.hk_list
    r=requests.get(url,headers=hds())
    text=r.text

    text=text.split('rank:[')[1].split('],')[0]
    text=text.replace('",','\n').replace('"','')

    df=pd.read_csv(StringIO(text),header=None)
    df=df.drop([12,13],axis=1)
    df.columns=wt.hk_ls_name
    df.loc[:,'code']=df.loc[:,'code'].map(lambda x:str(x).zfill(5))
    df=df.set_index('code')
    return df

if __name__=="__main__":
    df=get_HK_List_EM()
