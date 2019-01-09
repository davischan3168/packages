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

def get_reportlist_EM(code):
    """
    查询公司的分析报告
    --------------------------
    code:为6位数的股票代码,all表示查收前12500份报告
    """
     
    if code == 'all':
        url='http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20slnxALgp={%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}&ps=11500&p=1&mkt=0&stat=0&cmd=2&code=&rt=50017589'
    else:
        uu="{%22data%22:[(x)],%22pages%22:%22(pc)%22,%22update%22:%22(ud)%22,%22count%22:%22(count)%22}"
        url="http://datainterface.eastmoney.com//EM_DataCenter/js.aspx?type=SR&sty=GGSR&js=var%20slnxALgp={1}&ps=500&p=1&mkt=0&stat=0&cmd=2&code={0}&rt=50017589".format(code,uu)

    r=requests.get(url,headers=hds())
    text=r.text.split("=")[1]
    data=json.loads(text)
    df=pd.DataFrame(data['data'])

    try:
        df=df[["secuFullCode","secuName","rate","change","title","sys","syls","sy","newPrice","insName","author","datetime"]]
        df["datetime"]=df["datetime"].map(lambda x:x[:10])
        df=df.set_index("datetime")
        df=df.sort_index()
    except:
        pass

    return df

def get_holder_change_EM(code):
    url='http://data.eastmoney.com/DataCenter_V3/gdhs/GetDetial.ashx?code={0}&js=var%20wDmaHnNC&pagesize=5000&page=1&sortRule=-1&sortType=EndDate&param=&rt=50019973'.format(code)

    r=requests.get(url,headers=hds())
    text=r.text.split("wDmaHnNC=")[1]
    data=json.loads(text)
    df=pd.DataFrame(data['data'])

    #df['NoticeDate']=df['NoticeDate'].map(lambda x:x[:10])
    df['EndDate']=df['EndDate'].map(lambda x:x[:10])

    df=df.set_index('EndDate')
    df=df.sort_index()

    try:
        del df['NoticeDate']
        del df['CapitalStockChange']
        del df['CapitalStockChangeEvent']
    except:
        pass

    df=df.applymap(lambda x: wt._tofl(x))
    
    return df

def get_tick_today_EM(code,mtype=0):

    if code[0] in ['0','2','3']:
        code=code+'2'
    elif code[0] in ['6','9']:
        code=code+'1'

    df=pd.DataFrame()
    for i in range(1,20):
        url='http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/CompatiblePage.aspx?Type=OB&stk={0}&Reference=xml&limit={1}&page={2}'.format(code,mtype,i)
        #print(url)
        r=requests.get(url,headers=hds())
        text=r.text

        text=text.split('["')[1].replace(']};','')
        text=text.replace(',"','\n')
        text=text.replace('"','')
        
        #print(dd)
        try:
            dd=pd.read_csv(StringIO(text),header=None)
            #dd=pd.read_csv(StringIO(text))
            df=df.append(dd)
        except:
            print(i)
            break
    df=df.drop_duplicates()
    return df
        
        

if __name__=="__main__":
    #df=get_reportlist_EM(sys.argv[1])
    #dd=get_holder_change_EM(sys.argv[1])
    df=get_tick_today_EM(sys.argv[1])
