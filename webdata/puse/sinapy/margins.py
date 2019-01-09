#!/usr/bin/env python3
# -*-coding:utf-8-*-
import webdata.stock.reference as ts
import pandas as pd
import numpy as np
import datetime as dt
import time
import os,sys,requests
from bs4 import BeautifulSoup

today1=dt.date.today()
today=str(today1)

start_time=str(today1-dt.timedelta(days=250))

def margins_all(start=start_time,end=today):
    """
    参数说明：
    start:开始日期 format：YYYY-MM-DD 为空时取去年今日
    end:结束日期 format：YYYY-MM-DD 为空时取当前日期

    返回值说明：

    opDate:信用交易日期
    rzye:本日融资余额(元)
    rzmre: 本日融资买入额(元)v
    rqyl: 本日融券余量(股）
    rqye: 本日融券余量金额(元)
    rqmcl: 本日融券卖出量（股）
    rzrqye:本日融资融券余额(元)
    """
    sh=ts.sh_margins(start,end)
    sh['rzrqye']=sh['rzrqjyzl']
    sh['rqye']=sh['rqylje']
    del sh['rzrqjyzl']
    del sh['rqylje']
    #print('\n',sh.head(3))
    print('\n')
    sz=ts.sz_margins(start,end)
    #print('\n',sz.head(3))
    sh=sh.set_index('opDate')
    sz=sz.set_index('opDate')
    df=sh+sz
    #df=pd.concat([sh,sz],axis=0)
    return df

def margins_share(code,start=None,end=None):
    """
    参数说明：
    code:股票代码 format: 600036,000002
    start:开始日期 format：YYYY-MM-DD 为空时取去年今日
    end:结束日期 format：YYYY-MM-DD 为空时取当前日期

    返回值说明：
    opDate:  信用交易日期
    rzye:    本日融资余额(元)
    rzmre:   本日融资买入额(元)
    rzche:   本日融资偿还额(元)
    rqylje:  本日融券余量金额（元）
    rqyl:    本日融券余量（股）
    rqmcl:   本日融券卖出量
    rqchl:   本日融券偿还量
    rqye:    本日融券余额（元)
    """
    if end == None or (dt.datetime.strptime(end, '%Y-%m-%d')< dt.datetime.strptime(begin, '%Y-%m-%d')):
        end=dt.datetime.strftime(dt.datetime.today(),'%Y-%m-%d')
        if start == None:
            start=dt.datetime.strftime(dt.datetime.today()-dt.timedelta(days=360),'%Y-%m-%d')
            
    if code[0]=='0':
        code='sz'+code
    url='http://vip.stock.finance.sina.com.cn/q/go.php/vInvestConsult/kind/rzrq/index.phtml?symbol={0}&bdate={1}1&edate={2}'.format(code,start,end)
    r=requests.get(url)
    r=r.content.decode('gbk')
    soup=BeautifulSoup(r,'lxml')
    table=soup.find('table',attrs={'id':"dataTable"})
    table=str(table)
    table=table.replace('--','')
    df=pd.read_html(table)[0]
    for i in range(0,3):
        df=df.drop(i,axis=0)
    df=df.drop(0,axis=1)
    try:
        df.columns=['date','rzye','rzmre','rzche','rqylje','rqyl','rqmcl','rqchl','rqye']
        df=df.set_index('date')
        for label in list(df.columns):
            df[label]=df[label].astype(float)
        df=df.sort_index()
    except Exception as e:
        print(u"没有融资融券数据 %s" %code)
    return df

if __name__=="__main__":
    df=margins_share('600422')
