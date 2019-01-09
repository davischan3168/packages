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

today=time.strftime("%Y-%m-%d",time.localtime())

ss=re.compile(r'(-?\d+.?\d*)%')

quarter={1:'%s-03-31',2:'%s-06-30',3:'%s-09-30',4:'%s-12-31'}

def get_seniorM_holder_EM():
    """董监高及相关人员持股变动明细
    """
    url='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=GG&sty=GGMX&p=1&ps=5000'
    #print(url)
    
    r=requests.get(url,headers=hds())
    text=r.text.replace('(["','').replace('"])','')
    text=text.replace('","','\n')
    df=pd.read_csv(StringIO(text),header=None)
    df=df.drop([4,11,15],axis=1)
    df.columns=['chg','senior','code','holder','date','chg_num','num','trade_price','name','relation','reason','amount','title']
    df=df.applymap(lambda x:wt._tofl(x))
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    #df=df.set_index('code')
    #df=df.replace('-',np.nan)
    return df

def get_sharesholded_change_EM(code=None,mtype='all'):
    """股东对股票的增减持情况
    -------------------------
    mtype: all--所有的变动；jjc--减持；jzc--增持。
    """
    if code is None:
        code=''
        
    url='http://data.eastmoney.com/DataCenter_V3/gdzjc.ashx?pagesize=5000&page=1&param=&sortRule=-1&sortType=BDJZ&tabid={1}&code={0}&name='.format(code,mtype)

    r=requests.get(url,headers=hds())
    text=r.text.split(',data:["')[1].split('"] ,"url')[0]
    text=text.replace('","','\n')
    df=pd.read_csv(StringIO(text),header=None)

    tp=r.text.split(",data:[")[0].split("pages:")[1]
    tp=int(tp)

    if tp>1:
        for i in range(2,tp+1):
            url='http://data.eastmoney.com/DataCenter_V3/gdzjc.ashx?pagesize=5000&page={1}&param=&sortRule=-1&sortType=BDJZ&tabid=all&code={0}&name='.format(code,i)
            r=requests.get(url,headers=hds())
            text=r.text.split(',data:["')[1].split('"] ,"url')[0]
            text=text.replace('","','\n')
            df=df.append(pd.read_csv(StringIO(text),header=None))

    #df=df.drop(16,axis=1)
    df.columns=['code','name','price','chg','holder','type','chg_num','chg.cur.rate','source','hold_num','tt.rate','hold_cur_num','cur.rate','start','end','date','chg.tt.rate']
    df=df.applymap(lambda x:wt._tofl(x))
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    df=df.reset_index(drop=True)
    return df

def get_holdernum_change_EM(year,qu):
    """reportdate='2017-06-30'，所有股票的股东户数
    """
    if  year is None:
        reportdate=''
    else:
        reportdate=quarter[qu]%year
        
    url='http://data.eastmoney.com/DataCenter_V3/gdhs/GetList.ashx?reportdate={0}&market=&changerate==&range==&pagesize=50000&page=1&sortRule=-1&sortType=NoticeDate'.format(reportdate)

    r=requests.get(url,headers=hds())
    text=r.text
    data=json.loads(text)
    tp=data['pages']

    df=pd.DataFrame(data['data'])

    if tp>1:
        for i in range(2,tp+1):
            url='http://data.eastmoney.com/DataCenter_V3/gdhs/GetList.ashx?reportdate={0}&market=&changerate==&range==&pagesize=50000&page={1}&sortRule=-1&sortType=NoticeDate'.format(reportdate,i)
            r=requests.get(url,headers=hds())
            text=r.text
            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    return df

def get_share_holdernum_change_EM(code):
    """个股的股东户数历史详情
    """
    url='http://data.eastmoney.com/DataCenter_V3/gdhs/GetDetial.ashx?code={0}&pagesize=500&page=1&sortRule=-1&sortType=EndDate&param=&rt=50055484'.format(code)
    print(url)
    r=requests.get(url,headers=hds())
    text=r.text
    print(text)
    data=json.loads(text)
    tp=data['pages']

    df=pd.DataFrame(data['data'])

    if tp>1:
        for i in range(2,tp+1):
            url='http://data.eastmoney.com/DataCenter_V3/gdhs/GetDetial.ashx?code={0}&pagesize=500&page={1}&sortRule=-1&sortType=EndDate&param=&rt=50055484'.format(code,i)
            r=requests.get(url,headers=hds())
            text=r.text
            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    df=df.applymap(lambda x:wt._tofl(x))
    for label in [ 'EndDate', 'NoticeDate', 'PreviousEndDate']:
        df[label]=df[label].map(lambda x:x[:10])
    return df    

def get_holder_analys_EM(year,qu):
    """股东持股明细,reportdate='2017-06-30'
    """
    reportdate=quarter[qu]%year
    
    url="http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=NSHDDETAILLA&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=NDATE,SCODE,RANK&sr=1&p=1&ps=5000&js={1}&filter=(RDATE=%27^{0}^%27)".format(reportdate,'{%22pages%22:(tp),%22data%22:(x)}')

    #print(url)
    r=requests.get(url,headers=hds())
    text=r.text
    text=text.replace('pages:','"pages":').replace("data:",'"data":')
    #print(text[:30])
    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    tp=data['pages']

    if tp>1:
        for i in range(2,tp+1):
            url="http://dcfm.eastmoney.com//em_mutisvcexpandinterface/api/js/get?type=NSHDDETAILLA&token=70f12f2f4f091e459a279469fe49eca5&cmd=&st=NDATE,SCODE,RANK&sr=1&p={2}&ps=5000&js={1}&filter=(RDATE=%27^{0}^%27)".format(reportdate,'{%22pages%22:(tp),%22data%22:(x)}',i)

            r=requests.get(url,headers=hds())
            text=r.text
            text=text.replace('pages:','"pages":').replace("data:",'"data":')
            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))

    df['NDATE']=df['NDATE'].map(lambda x:x[:10])
    df['RDATE']=df['RDATE'].map(lambda x:x[:10])
    df=df.replace('-',np.nan)
    df=df.drop(['SHAREHDCODE','COMPANYCODE', 'SHARESTYPE', 'LTAG'],axis=1)
    df=df.applymap(lambda x:wt._tofl(x))
    df['SCODE']=df['SCODE'].map(lambda x:str(x).split('.')[0].zfill(6))
    return df

def get_search_inst_num_EM(code=None):
    """机构调研列表或个股机构调研列表
    """
    if code is None:
        url='http://data.eastmoney.com/DataCenter_V3/jgdy/gsjsdy.ashx?pagesize=5000&page=1'
    else:
        url='http://data.eastmoney.com/DataCenter_V3/jgdy/gsjsdy.ashx?pagesize=5000&page=1&code={0}'.format(code)
    
    r=requests.get(url,headers=hds())
    #print(url)
    text=r.text
    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    tp=data['pages']

    if tp>1:
        for i in range(2,tp+1):
            if code is None:
                url='http://data.eastmoney.com/DataCenter_V3/jgdy/gsjsdy.ashx?pagesize=5000&page={0}'.format(i)
            else:
                url='http://data.eastmoney.com/DataCenter_V3/jgdy/gsjsdy.ashx?pagesize=5000&page={1}&code={0}'.format(code,i)
            r=requests.get(url,headers=hds())
            text=r.text
            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    if df.empty is False:
        del df['CompanyCode']
    #df=df.applymap(lambda x:wt._tofl(x))
    #df['SCode']=df['SCode'].map(lambda x:str(x).zfill(6))
    return df        

def get_drogan_tiger_EM(code=None,start='2017-07-01',end=today):

    if code is None:
        """不能超过60天的交易数据"""
        url='http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=500,page=1,sortRule=-1,sortType=,startDate={0},endDate={1},gpfw=0,js=var%20data_tab_2.html?'.format(start,end)
    else:
        url='http://data.eastmoney.com/DataCenter_V3/stock2016/PreviousPerformance.ashx?pagesize=1000&page=1&gpfw=0&code={0}&startDate={1}&endDate={2}'.format(code,start,end)

    r=requests.get(url,headers=hds())
    #print(url)
    text=r.text
    try:
        text=text.split("data_tab_2=")[1]
    except:
        pass
    #print(text[:300])
    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    tp=data['pages']
    #"""
    if tp>1:
        for i in range(2,tp+1):
            if code is None:
                url='http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=500,page={2},sortRule=-1,sortType=,startDate={0},endDate={1},gpfw=0,js=var%20data_tab_2.html?'.format(start,end,i)
            else:
                url='http://data.eastmoney.com/DataCenter_V3/stock2016/PreviousPerformance.ashx?pagesize=1000&page={3}&gpfw=0&code={0}&startDate={1}&endDate={2}'.format(code,start,end)
                
            r=requests.get(url,headers=hds())
            text=r.text
            try:
                text=text.split("data_tab_2=")[1]
            except:
                pass
            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    #"""
    try:
        del df['CType']
        df['TDate']=df['TDate'].map(lambda x: x[:10])
        df=df.replace('',np.nan)
        df=df.dropna(how='all',axis=1)
    except:
        pass
    return df

def get_holder_shareperiod_EM(code,year,qu):
    """
    报告期前十大流动股东情况

    """
    date=quarter[qu]%year
    
    url='http://data.eastmoney.com/DataCenter_V3/gdfx/stockholder.ashx?code={0}&date={1}'.format(code,date)
                
    r=requests.get(url,headers=hds())
    text=r.text
    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    
    df=df.drop(['COMPANYCODE', 'LTAG', 'SHARESTYPE','SNAME','SHAREHDCODE'],axis=1)
    df['NDATE']=df['NDATE'].map(lambda x:x[:10])
    df['RDATE']=df['RDATE'].map(lambda x:x[:10])
    return df

def get_holder_sharedetail_EM(code,year,qu):

    date=quarter[qu]%year
    
    url='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=ZLSJ&sty=CCJGMX&p=1&ps=3000&js=var%20PkFmjYRh={2}&code={0}&fd={1}'.format(code,date,'{%22pages%22:(pc),%22data%22:[(x)]}')

    r=requests.get(url,headers=hds())
    text=r.text.split("PkFmjYRh=")[1]
    data=json.loads(text)
    content=data['data']
    content='\n'.join(content).replace('"','')
    
    df=pd.read_csv(StringIO(content),header=None)
    df=df.drop([0,1,2],axis=1)
    df.columns=['Inst_name','type','Num','Values','Curr.R','Total.R','date']

    return df
    
    
            
if __name__=="__main__":
    #df=get_finance_index_EM(2016,2)
    #df=get_cashf_today_EM()
    #df=get_cashf_sharehist_EM(sys.argv[1])
    #ddf=get_holder_change_EM('600291')
    #dff=get_share_holdernum_change_EM('600531')
    #dff=get_holder_analys_EM(reportdate='2017-06-30')
    #df=get_search_inst_num_EM(sys.argv[1])
    #df=get_drogan_tiger_EM()
    dd=get_holder_sharedetail_EM(sys.argv[1])
