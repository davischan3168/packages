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

def _set_code(code):
    if len(code)==5:
        code='hk'+code
        return code
    elif len(code)==6:
        if code[0] in ['2','0','3']:
            code='sz'+code
            return code
        else:
            return 'sh'+code

def HK_news_qq(tick):
    """
    获取某家上市公司的新闻资讯
    -------------------------------
    tick: 五位数的香港上市公司代码，如00005
    --
    return ：
        DataFrame
    """
    tick=_set_code(tick)
    page=1
    url=wt.news_hk.format(tick,page)
    r=requests.get(url,headers=hds())
    text=r.content.decode('utf8')
    #print(text)

    text=text.split('news=')[1]
    data=json.loads(text)
    df=pd.DataFrame(data['data']['data'])
    try:
        del df['symbols']
        del df['type']
        del df['id']
    except:
        pass
    
    return df
    
def HK_notice_qq(tick):
    """
    获取某家上市公司的公告资讯
    -------------------------------
    tick: 五位数的香港上市公司代码，如00005
    --
    return ：
        DataFrame
    """
    tick=_set_code(tick)
    page=1
    url=wt.notice_hk.format(tick,page)
    #print(url)
    r=requests.get(url,headers=hds())
    text=r.content.decode('utf8')
    #print(text)

    text=text.split('notice=')[1]
    data=json.loads(text)
    df=pd.DataFrame(data['data']['data'])
    df['time']=df['time'].map(lambda x:x[:10])
    try:
        del df['symbols']
        del df['type']
        del df['url']
        del df['src']
        del df['id']
        del df['summary']
    except:
        pass
    df=df.set_index('time')
    return df    


if __name__=="__main__":
    tick='01203'
    dd=HK_news_qq(sys.argv[1])
    #dd=HK_notice_qq(sys.argv[1])
