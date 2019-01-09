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


def get_mk_data_m163(code):
    """
    获取股票的历史交易数据
    """
    df=pd.DataFrame()
    ty=dt.datetime.today().year
    #years=range(1998,ty+1)
    years=range(ty-3,ty+1)
    for year in years:
        for season in [1,2,3,4]:
            url='http://quotes.money.163.com/trade/lsjysj_{2}.html?year={0}&season={1}'.format(year,season,code)
            try:
                #print(url)
                r=requests.get(url,headers=hds())
                soup=BeautifulSoup(r.text,'lxml')
                tb=soup.find(attrs={"class":"table_bg001 border_box limit_sale"})
                df=df.append(pd.read_html(str(tb))[0])
                #print(df.head())
            except:
                pass
    df=df.drop(0,axis=0)
    df=df.set_index('日期')
    df=df.sort_index()
    df=df.applymap(lambda x: wc._tofl(x))
    df['股票代码']= df['股票代码'].map(lambda x: x.replace("'",''))
    return df

def get_trading_data_m163(code,start='20100101',end=dt.datetime.today().strftime('%Y%m%d')):
    """
    code:股票代码
    start:开始读取的日期,like 20100101.
    end:  截止的日期，like 20170620
    
    """
    if code[0] in ['0','2']:
        url=wc.trading['sz'].format(code,start,end)
    elif code[0] in ['6','9']:
        url=wc.trading['sh'].format(code,start,end)
    elif code[0] in ['3']:
        url=wc.trading['gme'].format(code,start,end)
        
    #print(url)
    r=requests.get(url,stream=True,headers=hds())
    text=r.content.decode('gbk').replace('\r\n','\n')
    #print(text)
    
    #f=open('trading_%s_%s_%s.csv'%(code,start,end),'w')
    #f.write(text)
    #f.close()
    
    df=pd.read_csv(StringIO(text),header=0)
    df=df.dropna(how='all',axis=1)
    #print(df.head())
    
    name=list(df.columns)
    name=[s.strip() for s in name]
    df.columns=name

    try:
        df=df.set_index('日期')
        #del df['股票代码']
        #df=df.T
        df=df.sort_index()
        df=df.applymap(lambda x: np.where(x=='--',np.nan,wc._tofl(x)))
        df['股票代码']= df['股票代码'].map(lambda x: x.replace("'",''))        
    except:
        pass

    return df
                
def get_cashfl_m163(code):
    """
    quotes.money.163.com
    获取股票的买卖现金流量
    """
    df=pd.DataFrame()

    url='http://quotes.money.163.com/trade/lszjlx_{0},0.html'.format(code)
    while True:
        try:
            
            r=requests.get(url,headers=hds())
            soup=BeautifulSoup(r.text,'lxml')
            
            tb=soup.find('table',attrs={'class':"table_bg001 border_box"})
            df=df.append(pd.read_html(str(tb))[0])
            df=df.drop(0,axis=0)
        
            page=soup.find('a',text='下一页')
            url='http://quotes.money.163.com'+page.get('href')
        except:
            break
        
    df=df.set_index('日期')
    df=df.sort_index()
    df=df.applymap(lambda x: wc._tofl(x))
    
    try:
        df['股票代码']= df['股票代码'].map(lambda x: x.replace("'",''))
    except:
        pass

    return df

def get_cashflhy_m163(code):
    """
    同行业的涨跌幅前10只股票的资金流向情况
    type:jc---表示流出
         zc---表示流入
    """
    Df=pd.DataFrame()
    for mtype in ['zc','jc']:
        url="http://quotes.money.163.com/service/zjlx_table.html?symbol={0}&type={1}".format(code,mtype)

        r=requests.get(url,headers=hds())
        text=r.text

        df=pd.read_html(text)[0]
        df=df.drop(0,axis=0)
        Df=Df.append(df)

    Df=Df.drop('排名',axis=1)
    Df.columns=['name','price','chg','turnover','amount','out_amount','in_amout','net_amount']
    Df=Df.reset_index(drop=True)
    return Df
    
    
    
if __name__=="__main__":
    #df=get_mk_data('600160')
    #df=get_cf('600160')
    #code='002182'
    #start='20100101'
    #end='20170620'
    #df=trading_data(sys.argv[1],start)
    df=get_cashflhy_m163(sys.argv[1])
