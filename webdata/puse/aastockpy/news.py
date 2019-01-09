#!/usr/bin/env python3
# -*-coding:utf-8-*-

import requests
from io import StringIO
import re,sys,os
from bs4 import BeautifulSoup
import pandas as pd
import lxml.html
from lxml import etree
import webdata.puse.aastockpy.cont as wt
from webdata.util.hds import user_agent as hds

def HK_news_AAS(code):
    url='http://www.aastocks.com/tc/stocks/analysis/stock-aamm/{0}/0/aamm-all-category'.format(code)
    r=requests.get(url,headers=hds())
    html=lxml.html.parse(StringIO(r.text))
    res=html.xpath('//div[starts-with(@class,"common_box")]/div[@class="content_box"]')
    dataset=[]
    for i in res:
        title=i.xpath('div[1]/a/@title')
        time=i.xpath('div[2]/text()')
        text=i.xpath('div[3]//text()')
        try:
            title=title[0]
            time=time[0]
            if len(text)>0:
                text=text[0].replace('[大手成交]','')
            else:
                text=''
            dataset.append([title,text,time])    
            print(title,time,text)
        except Exception as e:
            print(e)
            pass

    return dataset

    
    
if __name__=="__main__":
    code='00005'
    df=news(code)
