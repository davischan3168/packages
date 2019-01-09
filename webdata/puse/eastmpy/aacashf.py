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
import webdata.puse.eastmpy.aafinance as wf

today=time.strftime('%Y-%m-%d',time.localtime())

ss=re.compile(r'(-?\d+.?\d*)%')

quarter={1:'%s-03-31',2:'%s-06-30',3:'%s-09-30',4:'%s-12-31'}

def get_cashf_alltoday_EM():
    """主力资金流入排名
    Main.R.T:主力净占比,
    Rank.T  ：今日排名
    Chg%.T  ：今日涨跌
    """
    url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(FFRank)&sr=1&p=1&ps=50000&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITAM'
    #print(url)
    
    r=requests.get(url,headers=hds())
    text=r.text.replace('(["','').replace('"])','')
    text=text.replace('","','\n')
    df=pd.read_csv(StringIO(text),header=None)
    df=df.drop([0],axis=1)
    df.columns=['code','name','price','Main.R.T','Rank.T','Chg%.T','Main.R.5','Rank.5','Chg%.5','Main.R.10','Rank.10','Chg%.10','industry','indu.ID','date']
    df=df.applymap(lambda x:wt._tofl(x))
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    df=df.set_index('code')
    #df=df.replace('-',np.nan)
    return df

def get_cashf_sharehist_EM(code):
    """个股的历史资金流向,资金流入金额的单位均为万元
    --------------------------------------
    Main.I.net ：今日主力净流入净额
    Main.I.R  ：今日主力净流入净占比
    """
    if code[0] in ['6','9']:
        code=code+'1'
    if code[0] in ['0','2','3']:
        code=code+'2'
        
    url='http://ff.eastmoney.com//EM_CapitalFlowInterface/api/js?type=hff&rtntype=2&check=TMLBMSPROCR&acces_token=1942f5da9b46b069953c873404aad4b5&id={0}'.format(code)

    r=requests.get(url,headers=hds())
    text=r.text.replace('(["','').replace('"])','')
    text=text.replace('","','\n')
    df=pd.read_csv(StringIO(text),header=None)
    df.columns=['date','Main.I.net','Main.I.R','Su.I.net','Su.I.R','Big.I.net','Big.I.R','Mid.I.net','Mid.I.R','Sm.I.net','Sm.I.R','price','Chg%']

    df=df.applymap(lambda x:wt._tofl(x))
    df=df.set_index('date')
    return df

def get_cashf_concepthist_EM(bkname):
    """板块的历史资金流向,资金流入金额的单位均为万元
    --------------------------------------
    Main.I.net ：今日主力净流入净额
    Main.I.R  ：今日主力净流入净占比
    """
    try:
        df=pd.read_pickle('output/eastmsource/bk.pkl')
    except:
        df=pd.read_csv('output/eastmsource/bk.csv',encoding='gbk')
    idd=df[df['name']==bkname]['id'].tolist()[0]
    #idd=df.loc[bkname,'id']
    url='http://ff.eastmoney.com//EM_CapitalFlowInterface/api/js?type=hff&rtntype=2&js={1}&cb=var%20aff_data=&check=TMLBMSPROCR&acces_token=1942f5da9b46b069953c873404aad4b5&id={0}1&_=1502340432743'.format(idd,'{%22data%22:(x)}')

    r=requests.get(url,headers=hds())
    text=r.text.split('{"data":["')[1].replace('(["','').replace('"])','')
    text=text.replace('"]}','')
    text=text.replace('","','\n')
    #print(text)
    df=pd.read_csv(StringIO(text),header=None)
    df.columns=['date','Main.I.net','Main.I.R','Su.I.net','Su.I.R','Big.I.net','Big.I.R','Mid.I.net','Mid.I.R','Sm.I.net','Sm.I.R','price','Chg%']

    df=df.applymap(lambda x:wt._tofl(x))
    df=df.set_index('date')
    return df


def get_cashf_concept_EM(mtype='hy',day=''):
    """获取板块的现金流入情况
    mtype:hy--行业板块；gn--概念板块；dy--地域板块
    day： 分为当日的数据，5日的数据，10日的数据
    ===========================================
    Main.I.net ：今日主力净流入净额
    Main.I.R  ：今日主力净流入净占比
    """
    day='BalFlowMain'+day
    
    if mtype == 'gn':
        url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C._BKGN&type=ct&st=({0})&sr=-1&p=1&ps=5000&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITABK&rt=50054963'.format(day)
    if mtype=='hy':
        url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C._BKHY&type=ct&st=({0})&sr=-1&p=1&ps=50000&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITABK&rt=50054967'.format(day)
    if mtype=='dy':
        url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C._BKDY&type=ct&st=({0})&sr=-1&p=1&ps=50&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITABK'.format(day)

    #print(url)
    r=requests.get(url,headers=hds())
    text=r.text.replace('(["','').replace('"])','')
    text=text.replace('","','\n')
    df=pd.read_csv(StringIO(text),header=None)
    df=df.drop([0],axis=1)
    df.columns=['id','name','Chg%','Main.I.net','Main.I.R','Su.I.net','Su.I.R','Big.I.net','Big.I.R','Mid.I.net','Mid.I.R','Sm.I.net','Sm.I.R','Sec_name','code']

    df=df.applymap(lambda x:wt._tofl(x))
    df['code']=df['code'].map(lambda x:str(x).zfill(7))
    df['code']=df['code'].map(lambda x:x[:6])
    return df

def get_cashf_conceptshares_EM(bkname,day=''):
    """获取同行业的股票涨跌信息
    """
    try:
        df=pd.read_pickle('output/eastmsource/bk.pkl')
    except:
        df=pd.read_csv('output/eastmsource/bk.csv',encoding='gbk')
    idd=df[df['name']==bkname]['id'].tolist()[0]
    #idd=df.loc[bkname,'id']
    #print(idd)
    if len(day)==0:
        day='BalFlowMain'
    elif len(day)>0:
        day='BalFlowMainNet'+day
    
    url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C.{0}1&type=ct&st=({1})&sr=-1&p=1&ps=5000&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITA'.format(idd,day)

    #print(url)
    r=requests.get(url,headers=hds())
    text=r.text.replace('(["','').replace('"])','')
    text=text.replace('","','\n')
    df=pd.read_csv(StringIO(text),header=None)
    df=df.drop(0,axis=1)
    df=df.applymap(lambda x:wt._tofl(x))
    try:
        df.columns=['code','name','price','chg','Main.I.net','Main.I.R','Su.I.net','Su.I.R','Big.I.net','Big.I.R','Mid.I.net','Mid.I.R','Sm.I.net','Sm.I.R','date']
        df['code']=df['code'].map(lambda x:str(x).zfill(6))
        df['date']=df['date'].map(lambda x:x[:10])
    except:
        pass
    df=df.replace('-',np.nan)
    return df

def get_cashf_concepthist_min_EM(bkname,day=today):
    """获得某个行业的资金流入流出情况，按1min中进行统计，
    day为交易日的条数
    bkname 为板块的名称
    """
    try:
        df=pd.read_pickle('output/eastmsource/bk.pkl')
    except:
        df=pd.read_csv('output/eastmsource/bk.csv',encoding='gbk')
    idd=df[df['name']==bkname]['id'].tolist()[0]
    #idd=df.loc[bkname,'id']
    #print(idd)
    url='http://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?id={0}1&type=ff&check=MLBMS&cb=var%20aff_data={1}&js={2}&rtntype=3&acces_token=1942f5da9b46b069953c873404aad4b5'.format(idd,day,'{(x)}')

    r=requests.get(url,headers=hds())
    pc='='+day
    text=r.text.split(pc)[1]
    #print(text)
    data=json.loads(text)
    dataset=[]
    for i in data['ya']:
        dataset.append(i.split(','))

    df=pd.DataFrame(dataset)

    
    index=data['xa'].split(',')
    index=index[:df.shape[0]]
    df.index=index
    df=df.replace('',np.nan)
    df=df.dropna(how='all',axis=0)
    df.columns=['Main','Super','Big','Middle','Small']
    return df
    
def get_cashf_conceptcenter_EM(bkname):
    """获取同行业股票行情中心的涨跌信息
    """
    try:
        df=pd.read_pickle('output/eastmsource/bk.pkl')
    except:
        df=pd.read_csv('output/eastmsource/bk.csv',encoding='gbk')
        
    idd=df[df['name']==bkname]['id'].tolist()[0]
    #idd=df.loc[bkname,'id']
    
    url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C.{0}1&sty=FCOIATA&sortType=C&sortRule=-1&page=1&pageSize=2000&token=7bc05d0d4c3c22ef9fca8c2a912d779c'.format(idd)

    #print(url)
    r=requests.get(url,headers=hds())
    text=r.text.replace('(["','').replace('"])','')
    text=text.replace('","','\n')
    df=pd.read_csv(StringIO(text),header=None)
    df=df.drop([0,13,14,15,16,17,18,19,20],axis=1)
    
    df=df.applymap(lambda x:wt._tofl(x))
    
    try:
        df.columns=['code','name','price','chg','chg%','ZF','volume','amount','pre.close','open','high','low','chg.5m','LR','turnover','PE']
        df['code']=df['code'].map(lambda x:str(x).zfill(6))
    except:
        pass
    
    df=df.replace('-',np.nan)
    df=df.dropna(how='all',axis=1)
    return df    
    
def get_cashf_sharehist_min_EM(code,day=today):
    """获得某只股票的资金流入流出情况，按1min中进行统计，
    day为交易日的条数
    bkname 为板块的名称
    """
    if code[0] in ['6','9']:
        code=code+'1'
    elif code[0] in ['0','2','3']:
        code=code+'2'
    
    url='http://ff.eastmoney.com/EM_CapitalFlowInterface/api/js?id={0}&type=ff&check=MLBMS&cb=var%20aff_data={1}&js={2}&rtntype=3&acces_token=1942f5da9b46b069953c873404aad4b5'.format(code,day,'{(x)}')

    r=requests.get(url,headers=hds())
    pc='='+day
    text=r.text.split(pc)[1]
    #print(text)
    data=json.loads(text)
    dataset=[]
    for i in data['ya']:
        dataset.append(i.split(','))

    df=pd.DataFrame(dataset)
    
    index=data['xa'].split(',')
    index=index[:df.shape[0]]
    df.index=index
    df=df.replace('',np.nan)
    df=df.dropna(how='all',axis=0)
    df.columns=['Main','Super','Big','Middle','Small']
    df=df.applymap(lambda x:wt._tofl(x))
    return df    
    
def get_conceptSelectShares_EM(bkname,year=2017,qu=2):
    """从板块中选择股票
    --------------------------------------
    bkname:板块名称，主要是按照Eastmoney网站的分类
    year:  年度，为整数型，如2017年
    qu：    季度，为整数型。如第二季度为2
    """
    dff=get_cashf_conceptcenter_EM(bkname)
    #print(dff.head())
    #print(len(dff.columns))
    
    codeset=dff.iloc[:,0].tolist()

    fs=wf.get_finance_index_EM(year,qu)

    dtset=pd.DataFrame()
    for code in codeset:
            try:
                dtset=dtset.append(fs.loc[code,:])
            except Exception as e:
                pass
            
    dtset=dtset.sort_values(by=['roe','profit_yoy'],ascending=False)
    dtset=dtset.dropna(how='all',axis=1)            
    return dtset

if __name__=="__main__":
    #df=get_finance_index_EM(2016,2)
    #df=get_cashf_today_EM()
    #df=get_cashf_sharehist_EM(sys.argv[1])
    #df=get_cashf_concept(sys.argv[1])
    #df=get_cashf_concept_shares_EM(sys.argv[1])
    #dd=get_cashf_concept_hist_min_EM
    #df=get_cashf_concept_center_EM(sys.argv[1])
    #df=get_cashf_share_hist_min_EM(sys.argv[1],day=today)
    #dd=get_cashf_concepthist_EM(sys.argv[1])
    df=get_conceptSelectShares_EM(sys.argv[1])
