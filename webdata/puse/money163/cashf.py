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

def get_cashf_today_m163(code):
    """
    获得单日的现金流入情况
    """
    url=wc.cashf_url.format(code)
    r=requests.get(url)
    data=json.loads(r.text)
    print("大单主买量手：",data['dd_buy'])
    print("大单主卖量手：",data['dd_sell'])
    print("实时资金净流入(万元）：",data['jlr_shishi'])
    print("大单成交占比(%)：",data['percent'])
    dadan=data['jlr_json']
    for i in dadan:
        print(i['key'],':',i['value'])
    return data

def get_cashf_thy_m163(code,mytype='zc'):
    """
    获取同行业的资金流入情况
    """
    url=wc.cash_thy_url.format(code,mytype)
    r=requests.get(url)
    df=pd.read_html(str(r.text),header=0)[0]
    df=df.drop(0,axis=0)
    return df


    
if __name__=="__main__":
    code='002182'
    #df=cashf_today(code)
    df=cashf_thy(code)
