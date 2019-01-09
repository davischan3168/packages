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

def notice_m163(code,mytype='zjgg'):
    """
    """
    datalist=[]
    
    url=wc.notice_url.format(code,mytype)
    r=requests.get(url)

    html=lxml.html.parse(StringIO(r.text))
    res=html.xpath('//div[@class="tabs_panel"]/table[@class="table_bg001 border_box limit_sale"]//tr')

    for r in res:
        try:
            name=r.xpath('td[1]/a/text()')[0]
            href=wc.base+r.xpath('td[1]/a/@href')[0]
            date=r.xpath('td[2]/text()')[0]
            ttype=r.xpath('td[3]/text()')[0]
            
            datalist.append([name,ttype,href,date])
        except:
            pass

    df=pd.DataFrame(datalist,columns=['name','ttype','href','date'])
    return df


def news_m163(code):

    url=wc.new_url.format(code)
    datalist=[]
    r=requests.get(url)

    html=lxml.html.parse(StringIO(r.text))
    res=html.xpath('//div[@class="tabs_panel"]/table[@class="table_bg001 border_box limit_sale"]//tr')
    #print(res)

    for r in res:
        try:
            name=r.xpath('td[1]/a/text()')[0]
            href=r.xpath('td[1]/a/@href')[0]
            date=r.xpath('td[2]/text()')[0]
            
            datalist.append([name,href,date])
        except Exception as e:
            #print(e)
            pass

    df=pd.DataFrame(datalist,columns=['name','href','date'])
    return df

def get_newstext_m163(url):
    r=requests.get(url)

    htmll=lxml.html.parse(StringIO(r.text))
    title=htmll.xpath('//div[@id="epContentLeft"]/h1/text()')[0]
    text=htmll.xpath('//div[@id="endText"]//text()')

    content="".join(text)
    return title,content


if __name__=="__main__":
    code='002182'
    df=notice(code)
    dd=news(code)
    
    
    
