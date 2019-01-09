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

def HK_inst_qq(tick):
    """
    获取某家上市公司的机构持股信息
    -------------------------------
    tick: 五位数的香港上市公司代码，如00005
    --
    return ：
        DataFrame
    """
    page=1
    url=wt.inst_hk.format(tick,page)
    r=requests.get(url,headers=hds())
    text=r.content.decode('utf8')
    #print(text)

    #text=text.split('=')[1]
    data=json.loads(text)
    df=pd.DataFrame(data['data']['data'])

    try:
        df=df.set_index('CHANGE_DATE')
    except:
        pass
    
    return df
    

def HK_dividen_qq(tick):
    """
    获取某家上市公司的分红信息
    -------------------------------
    tick: 五位数的香港上市公司代码，如00005
    --
    return ：
        DataFrame
    """
    page=1
    url=wt.inst_hk.format(tick,page)
    r=requests.get(url,headers=hds())
    text=r.content.decode('utf8')
    #print(text)

    #text=text.split('=')[1]
    data=json.loads(text)
    df=pd.DataFrame(data['data']['data'])

    
    return df

def HK_Invest_Rating_qq(code):
    """投资评级
    --------------------
    AIM_PRICE:目标价(港币元)
    DEPARTMENT_CODE：评价机构代码
    DEPARTMENT_NAME：投行名称
    ENTRY_TIME：公布时间
    EVA_RANK：评价等级，1是持有，2是买进，3是卖出
    FORE_IS_INCRES: 目标价变化
    FORE_RANK_IS_INCRES:同投行上次评级
    HIBRR_ID：
    SEC_CODE:证券代码
    SEC_NAME证券名称
    """
    
    url='http://web.ifzq.gtimg.cn/appstock/hk/HkInfo/getInvestBankRating?p=1&c={0}&max=50000&o=0&_callback='.format(code)
    r=requests.get(url,headers=hds())

    text=r.content.decode('utf8')

    data=json.loads(text)
    df=pd.DataFrame(data['data']['data'])
    
    try:
        del df['DEPARTMENT_CODE']
        df=df.set_index('ENTRY_TIME')
        df.index=df.index.map(lambda x:x[:10])
        df['AIM_PRICE']=df['AIM_PRICE'].map(lambda x: float(x))
    except Exception as e:
        print(e)
        
    return df

if __name__=="__main__":
    tick='01203'
    dd=dividen_qqhk(sys.argv[1])
    #dd=inst_qqhk(sys.argv[1])
