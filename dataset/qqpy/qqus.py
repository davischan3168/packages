#!/usr/bin/env python3
# -*-coding:utf-8-*-

import requests,os,sys
import pandas as pd
import numpy as np
import json,datetime
#from util import dateu as du
from webdata.puse.qqpy.uscode import codeset

usstock_url='http://stock.gtimg.cn/data/index.php?appn=usRank&t={0}/code&p=1&o=0&l=8000&v=list_data&_du_r_t=0.08047113276767703'

TT_K_TYPE = {'D': 'day', 'W': 'week', 'M': 'month'}
K_LABELS = ['D', 'W', 'M']
TTfq_URL='http://web.ifzq.gtimg.cn/appstock/app/%skline/get?_var=kline_%s&param=%s,%s,%s,%s,640,%s&r=0.%s'
TTmq_URL='http://web.ifzq.gtimg.cn/appstock/app/kline/kline?_var=kline_%s&param=%s,%s,%s,%s,640,%s&r=0.%s'
NETWORK_URL_ERROR_MSG = '获取失败，请检查网络和URL'

uscodebk={'IMP':'IMP','TDR':'TDR','HDR':'HDR',
        'CDR':'CDR','TEC':'TEC','FIN':'FIN',
        'MAR':'MAR','MED':'MED','AAE':'AAE','MAF':'MAF'}


name=['id','code','name','close','chg%','chg','buy','sell','volume','PE','open','pre.close','high','low']



def get_usgrouby_data(bk):
    """
    
    """
    url=usstock_url.format(bk)
    #print(url)
    r=requests.get(url)
    print(r.text)
    text=r.text.split('data=')[1]
    data=json.loads(text)
    df=pd.DataFrame(data['data']['result'],columns=name)
    return df

def get_usall_data():
    """
    """
    df=pd.DataFrame()
    for bk in uscodebk.keys():
        df=df.append(get_usgrouby_data(bk))

    df=df.set_index('code')
    return df

indexsymbol={'DJI':'DJI','NSDQ':'IXIC','SP':'INX'}

def get_k_usdata(code,start='',end='',
                     index=False,autype=None,
                     ktype='d'):
    
    if index:
        df=get_k_us_index(code,start,end,ktype=ktype)
    else:
        df=get_k_us_data(code,start,end,autype,ktype)

    return df
        
def get_k_us_data(code,start='',end='',
                     autype=None,
                     ktype='d'):

    """
    获取k线数据
        retry_count=3,
        pause=0.001
    ---------
    Parameters:
      code:string
                  股票代码 e.g. 600848
      start:string
                  开始日期 format：YYYY-MM-DD 为空时取上市首日
      end:string
                  结束日期 format：YYYY-MM-DD 为空时取最近一个交易日
      autype:string
                  复权类型，qfq-前复权 None-不复权，默认为qfq
      ktype：string
                  数据类型，D=日k线 W=周 M=月, 默认为D
      retry_count : int, 默认 3
                 如遇网络等问题重复执行的次数 
      pause : int, 默认 0
                重复请求数据过程中暂停的秒数，防止请求间隔时间太短出现的问题
    return
    -------
      DataFrame
          date 交易日期 (index)
          open 开盘价
          high  最高价
          close 收盘价
          low 最低价
          volume 成交量
          code 股票代码
    """
        
    symbol= 'us%s'%codeset[code]
    if (start is not None) & (start != ''):
        end = today() if end is None or end == '' else end    
    if ktype.upper() in K_LABELS:
        fq=autype if autype is not None else ''
        dataflag = '%s%s'%(fq, TT_K_TYPE[ktype.upper()])
        fq1=TT_K_TYPE[ktype.upper()]+fq
        
        if autype is None:
            if (start is None or start == '') & (end is None or end == ''):
                #print("Kline:",kline)
                urls=[TTmq_URL%(fq1,symbol,TT_K_TYPE[ktype.upper()],
                                start,end,fq,_random(17))]

            else:
                years=tt_dates(start,end)
                urls=[]
                for year in years:
                    startdate=str(year) + '-01-01'
                    enddate=str(year+1) + '-12-31'
                    url=TTmq_URL%(fq1,symbol,TT_K_TYPE[ktype.upper()],
                                startdate,enddate,fq,_random(17))
                    urls.append(url)

            df=pd.DataFrame()
            for url in urls:
                #print(url)
                r=requests.get(url)
                
                text=r.text.split(fq1+'=')[1]
                #print(text[:20])
                data=json.loads(text)
                df=df.append(pd.DataFrame(data['data'][symbol][dataflag]))

        else:
            kline='usfq'
            if (start is None or start == '') & (end is None or end == ''):
                #print("Kline:",kline)
                urls=[TTfq_URL%(kline,fq1,symbol,TT_K_TYPE[ktype.upper()],
                              start,end,fq,_random(17))]

            else:
                years=tt_dates(start,end)
                urls=[]
                for year in years:
                    startdate=str(year) + '-01-01'
                    enddate=str(year+1) + '-12-31'
                    url=TTfq_URL%(kline,fq1,symbol,TT_K_TYPE[ktype.upper()],
                                startdate,enddate,fq,_random(17))
                    urls.append(url)

            df=pd.DataFrame()
            for ulr in urls:
                #print(ulr)
                r=requests.get(ulr)
                text=r.text.split(fq1+'=')[1]
                #print(text[:20])
                data=json.loads(text)
                df=df.append(pd.DataFrame(data['data'][symbol][dataflag]))
                    
                    
    df.columns=['date','open','close','high','low','volume']
    df['code']=symbol
    return df

us_index='http://web.ifzq.gtimg.cn/appstock/app/usfqkline/get?_var=kline_%s&param=%s,%s,%s,%s,640,qfq&r=%s'

def get_k_us_index(code,start='',end='',ktype='D'):
    
    #symbol=indexsymbol[code]
    symbol='us.%s'%indexsymbol[code]
    df=pd.DataFrame()
    if (start is not None) & (start != ''):
        end = today() if end is None or end == '' else end    
    if ktype.upper() in K_LABELS:
        dataflag = 'qfq%s'%TT_K_TYPE[ktype.upper()]
        #print(dataflag)
        
        fq=TT_K_TYPE[ktype.upper()]+'qfq'
        if (start is None or start == '') & (end is None or end == ''):
            urls=[us_index%(fq,symbol,TT_K_TYPE[ktype.upper()],start,end,_random(17))]

        else:
            years=tt_dates(start,end)
            urls=[]
            for year in years:
                startdate=str(year) + '-01-01'
                enddate=str(year+1) + '-12-31'
                url=us_index%(fq,symbol,TT_K_TYPE[ktype.upper()],startdate,enddate,_random(17))
                urls.append(url)

        for url in urls:
            r=requests.get(url)
            #print(url)
            text=r.text.split(fq+'=')[1]
            #print(text[:100])
            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data'][symbol][dataflag]))

    df.columns=['date','open','close','high','low','volume']
    df['code']=symbol
    return df

hk_index='http://web.ifzq.gtimg.cn/appstock/app/kline/kline?_var=kline_%s&param=%s,%s,%s,%s,640,&r=%s'
def get_k_hkindex(code,start='',end='',ktype='D'):
    """
    code: HSI--恒生指数,HSCEI--国企指数,HSCCI--红筹指数
    ktype：D--日线，W--周线 M--月线

    """
    
    #symbol=indexsymbol[code]
    symbol='hk%s'%code
    df=pd.DataFrame()
    if (start is not None) & (start != ''):
        end = today() if end is None or end == '' else end    
    if ktype.upper() in K_LABELS:
        dataflag = '%s'%TT_K_TYPE[ktype.upper()]
        
        fq=TT_K_TYPE[ktype.upper()]+'qfq'
        if (start is None or start == '') & (end is None or end == ''):
            urls=[hk_index%(fq,symbol,TT_K_TYPE[ktype.upper()],start,end,_random(17))]

        else:
            years=tt_dates(start,end)
            urls=[]
            for year in years:
                startdate=str(year) + '-01-01'
                enddate=str(year+1) + '-12-31'
                url=hk_index%(fq,symbol,TT_K_TYPE[ktype.upper()],startdate,enddate,_random(17))
                urls.append(url)

        for url in urls:
            r=requests.get(url)
            #print(url)
            text=r.text.split(fq+'=')[1]
            #print(text[:100])
            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data'][symbol][dataflag]))

    df.columns=['date','open','close','high','low','volume']
    df['code']=symbol
    return df


def _random(n=13):
    from random import randint
    start = 10**(n-1)
    end = (10**n)-1
    return str(randint(start, end))

def today():
    day = datetime.datetime.today().date()
    return str(day)
def tt_dates(start='', end=''):
    startyear = int(start[0:4])
    endyear = int(end[0:4])
    dates = [d for d in range(startyear, endyear+1, 2)]
    return dates

if __name__=="__main__":
    #df=get_usall_data()
    #dd=get_kus_data(sys.argv[1])
    #dd=get_k_usdata(sys.argv[1],index=True)
    dd=get_k_hkindex(sys.argv[1])
