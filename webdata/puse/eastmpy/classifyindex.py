#!/usr/bin/env python3
# -*-coding:utf-8-*-

import sys,requests
import os
from urllib.parse import quote
import lxml.html
from io import StringIO
import time
import json
import pandas as pd
import numpy as np
import pickle
from webdata.util.hds import user_agent as hds
import webdata.puse.eastmpy.cont as wt

gn='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKGN&sty=FPGBKI&sortType=(ChangePercent)&sortRule=-1&page=1&pageSize=500&js={%22rank%22:[(x)],%22pages%22:(pc),%22total%22:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c'

dy='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKDY&sty=FPGBKI&sortType=(ChangePercent)&sortRule=-1&page=1&pageSize=5000&js={%22rank%22:[(x)],%22pages%22:(pc),%22total%22:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c'

hy='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKHY&sty=FPGBKI&sortType=(ChangePercent)&sortRule=-1&page=1&pageSize=500&js={%22rank%22:[(x)],%22pages%22:(pc),%22total%22:(tot)}&token=7bc05d0d4c3c22ef9fca8c2a912d779c'

urls=[gn,hy,dy]
columns=['Code','Name','ChgP','Market','turnover','info','upcode','upname','uprice','upchgp','dcode','dname','dprice','dchgp','Price','Chg']

def get_allclassified_EM(url=urls):
    df=pd.DataFrame()
    for u in url:
        r=requests.get(u,headers=hds())
        data=json.loads(r.text)
        data=data['rank']
        data='\n'.join(data)
        dff=pd.read_csv(StringIO(data),header=None)
        dff=dff.drop([0,8,13,17],axis=1)
        dff.columns=columns
        df=df.append(dff)
    fp='webdata/puse/eastmpy/classified.pkl'
    f=open(fp,'wb')
    dictt={}
    for i,r in df.iterrows():
        dictt[r['Name']]=r["Code"]
    pickle.dump(dictt,f)
    f.close()    
    return df
        

def get_classified_index_EM(concept,mtype='day',fq='fq'):

    """
    获取行业\概念\地域版块的指数：
    -------------------------------
    concept:行业\概念\地域 名词
    fq:不复权，None;qfq:前复权;hfq:后复权
    mtype:day,日线；week，周线；month,月线；m5：5分钟线；m15：15分钟线；m30：30分钟
    线；m60：60分钟线

    """
    fqv={'fq':'','qfq':'authorityType=fa','hfq':'authorityType=ba'}
    kline={'day':'K','month':'mk','week':'wk','m5':'m5k','m15':'m15k','m30':'m30k','m60':'m60k'}
    
    fp='webdata/puse/eastmpy/classified.pkl'
    f=open(fp,'rb')
    classify=pickle.load(f)
    f.close()

    if concept in classify.keys():
        if fq =='fq':
            url='http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s1&TYPE=%s&js=(x)&rtntype=5'%(classify[concept],kline[mtype])
        else:
            url='http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s1&TYPE=%s&js=(x)&rtntype=5&%s'%(classify[concept],kline[mtype],fqv[fq])
        r=requests.get(url,headers=hds())
        dtext=json.loads(r.text)
        dd='\n'.join(dtext['data'])
        df=pd.read_csv(StringIO(dd),header=None)        
        df.columns=['date','open','close','high','low','volume','amount','turnover']
        df=df.set_index('date')
        df.index=pd.to_datetime(df.index)
        df=df.replace('-',np.nan)
        for label in df.columns:
            try:
                df[label]=df[label].astype(float)
            except:
                df[label]=df[label].map(lambda x: wt._tofl(x))        
        return df
    else:
        print("%s not in classify......"%concept)
        print(classify.keys())
        sys.exit()

def get_shares_GroupbyClassify_EM(concept):
    
    fp='webdata/puse/eastmpy/classified.pkl'
    f=open(fp,'rb')
    classify=pickle.load(f)
    f.close()

    if concept in classify.keys():
        url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C.{0}1&sty=FCOIATA&sortType=(ChangePercent)&sortRule=-1&page=1&pageSize=1000&js={1}&token=7bc05d0d4c3c22ef9fca8c2a912d779c'.format(classify[concept],'{%22rank%22:[(x)],%22pages%22:(pc),%22total%22:(tot)}')
        r=requests.get(url,headers=hds())
        dtext=json.loads(r.text)
        dd='\n'.join(dtext['rank'])
        df=pd.read_csv(StringIO(dd),header=None)        
        df=df.drop([0,13,14,15,16,18,17,19,20],axis=1)
        df.columns=['code','name','close','chg','chgp%','zhengfu%','volume','amount','pre_close','open','high','low','chgp_in_5m%','liangbi','turnover%','PE','listed_date']
        df['code']=df['code'].map(lambda x:str(x).zfill(6))
        df=df.set_index('code')
        df=df.replace('-',np.nan)
        for label in df.columns:
            try:
                df[label]=df[label].astype(float)
            except:
                df[label]=df[label].map(lambda x: wt._tofl(x))        
        return df
    else:
        print("%s not in classify......"%concept)
        print(classify.keys())
        sys.exit()
        
if __name__=="__main__":
    #df=get_classified_index_EM(sys.argv[1])
    df=get_shares_GroupbyClassify_EM(sys.argv[1])
