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

def get_BDI_EM():
    """
    BDI: 波罗的海干散货指数（BDI）
    --------------------------
    """
        
    url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00107664%27)&st=DATADATE&sr=-1&p=1&ps=2000&js=var%20GiHSNWoZ={pages:(tp),data:(x)}'

    r=requests.get(url,headers=hds())
    text=r.text
    text=text.replace('pages','"pages"').replace('data:[','"data":[')
    text=text.split("GiHSNWoZ=")[1]

    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    tp=data['pages']

    if tp>1:
        for i in range(2,tp+1):
            url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00107664%27)&st=DATADATE&sr=-1&p={0}&ps=2000&js=var%20GiHSNWoZ={1}'.format(i,'{pages:(tp),data:(x)}')
            r=requests.get(url,headers=hds())
            text=r.text
            text=text.replace('pages','"pages"').replace('data:[','"data":[')
            text=text.split("GiHSNWoZ=")[1]

            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    
    df.columns=['date','code','price','change','chg']
    df=df[['date','price','change','chg']]
    df=df.set_index('date')
    df=df.sort_index()
    df=df.applymap(lambda x:wt._tofl(x))    
    return df

def get_BCI_EM():
    """
    BCI: 海岬型运费指数（BCI）
    --------------------------
    """
        
    url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00107666%27)&st=DATADATE&sr=-1&p=1&ps=2000&js=var%20YJTIAtMT={pages:(tp),data:(x)}&rt=50063515'

    r=requests.get(url,headers=hds())
    text=r.text
    text=text.replace('pages','"pages"').replace('data:[','"data":[')
    text=text.split("=")[1]

    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    tp=data['pages']

    if tp>1:
        for i in range(2,tp+1):
            url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00107666%27)&st=DATADATE&sr=-1&p={0}&ps=2000&js=var%20YJTIAtMT={1}&rt=50063515'.format(i,'{pages:(tp),data:(x)}')
            r=requests.get(url,headers=hds())
            text=r.text
            text=text.replace('pages','"pages"').replace('data:[','"data":[')
            text=text.split("=")[1]

            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    
    df.columns=['date','code','price','change','chg']
    df=df[['date','price','change','chg']]
    df=df.set_index('date')
    df=df.sort_index()
    df=df.applymap(lambda x:wt._tofl(x))    
    return df

def get_TDI_EM():
    """
    TDI: 沿海集装箱运价指数（TDI）
    --------------------------
    """
        
    url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00478149%27)&st=DATADATE&sr=-1&p=1&ps=200&js=var%20MTKxyKGl={pages:(tp),data:(x)}&rt=50063502'

    r=requests.get(url,headers=hds())
    text=r.text
    text=text.replace('pages','"pages"').replace('data:[','"data":[')
    text=text.split("=")[1]

    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    tp=data['pages']

    if tp>1:
        for i in range(2,tp+1):
            url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00478149%27)&st=DATADATE&sr=-1&p={0}&ps=20&js=var%20MTKxyKGl={1}&rt=50063502'.format(i,'{pages:(tp),data:(x)}')
            r=requests.get(url,headers=hds())
            text=r.text
            text=text.replace('pages','"pages"').replace('data:[','"data":[')
            text=text.split("=")[1]

            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    
    df.columns=['date','code','price','change','chg']
    df=df[['date','price','change','chg']]
    df=df.set_index('date')
    df=df.sort_index()
    df=df.applymap(lambda x:wt._tofl(x))    
    return df

def get_BBPI_EM():
    """
    大宗商品价格指数（BPI）
    --------------------------
    """
    url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00662535%27)&st=DATADATE&sr=-1&p=1&ps=2000&js=var%20tQtWlTPU={pages:(tp),data:(x)}&rt=50061768'

    r=requests.get(url,headers=hds())
    text=r.text
    text=text.replace('pages','"pages"').replace('data:[','"data":[')
    text=text.split("QtWlTPU=")[1]

    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    tp=data['pages']

    if tp>1:
        for i in range(2,tp+1):
            url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00662535%27)&st=DATADATE&sr=-1&p={0}&ps=2000&js=var%20tQtWlTPU={1}&rt=50061768'.format(i,'{pages:(tp),data:(x)}')

            r=requests.get(url,headers=hds())
            text=r.text
            text=text.replace('pages','"pages"').replace('data:[','"data":[')
            text=text.split("QtWlTPU=")[1]

            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    
    df.columns=['date','code','price','change','chg']
    df=df[['date','price','change','chg']]
    df=df.set_index('date')
    df=df.sort_index()
    df=df.applymap(lambda x:wt._tofl(x))    
    return df

def get_MetalC_EM():
    """
    有色金属指数
    --------------------------
    """
    url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00662542%27)&st=DATADATE&sr=-1&p=1&ps=2000&js=var%20oqHHHzay={pages:(tp),data:(x)}&rt=50061784'

    r=requests.get(url,headers=hds())
    text=r.text
    text=text.replace('pages','"pages"').replace('data:[','"data":[')
    text=text.split("qHHHzay=")[1]

    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    tp=data['pages']

    if tp>1:
        for i in range(2,tp+1):
            url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00662542%27)&st=DATADATE&sr=-1&p={0}&ps=2000&js=var%20oqHHHzay={1}&rt=50061784'.format(i,'{pages:(tp),data:(x)}')

            r=requests.get(url,headers=hds())
            text=r.text
            text=text.replace('pages','"pages"').replace('data:[','"data":[')
            text=text.split("qHHHzay=")[1]

            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    
    df.columns=['date','code','price','change','chg']
    df=df[['date','price','change','chg']]
    df=df.set_index('date')
    df=df.sort_index()
    df=df.applymap(lambda x:wt._tofl(x))    
    return df

def get_TieKuangshi_EM():
    """
    铁矿石指数
    --------------------------
    """
    url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00064805%27)&st=DATADATE&sr=-1&p=1&ps=2000&js=var%20cpozUGER={pages:(tp),data:(x)}&rt=50061815'

    r=requests.get(url,headers=hds())
    text=r.text
    text=text.replace('pages','"pages"').replace('data:[','"data":[')
    text=text.split("=")[1]

    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    tp=data['pages']

    if tp>1:
        for i in range(2,tp+1):
            url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00064805%27)&st=DATADATE&sr=-1&p=1&ps=2000&js=var%20cpozUGER={1}&rt=50061799'.format(i,'{pages:(tp),data:(x)}')

            r=requests.get(url,headers=hds())
            text=r.text
            text=text.replace('pages','"pages"').replace('data:[','"data":[')
            text=text.split("=")[1]

            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    
    df.columns=['date','code','price','change','chg']
    df=df[['date','price','change','chg']]
    df=df.set_index('date')
    df=df.sort_index()
    df=df.applymap(lambda x:wt._tofl(x))    
    return df

def get_BPI_EM():
    """
    BPI: 巴拿马型运费指数（BPI）
    --------------------------
    """
        
    url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00107665%27)&st=DATADATE&sr=-1&p=1&ps=2000&js=var%20upiLBkHh={pages:(tp),data:(x)}&rt=50063525'

    r=requests.get(url,headers=hds())
    text=r.text
    text=text.replace('pages','"pages"').replace('data:[','"data":[')
    text=text.split("=")[1]

    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    tp=data['pages']

    if tp>1:
        for i in range(2,tp+1):
            url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00107665%27)&st=DATADATE&sr=-1&p={0}&ps=200&js=var%20upiLBkHh={1}&rt=50063525'.format(i,'{pages:(tp),data:(x)}')
            
            r=requests.get(url,headers=hds())
            text=r.text
            text=text.replace('pages','"pages"').replace('data:[','"data":[')
            text=text.split("=")[1]

            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    
    df.columns=['date','code','price','change','chg']
    df=df[['date','price','change','chg']]
    df=df.set_index('date')
    df=df.sort_index()
    df=df.applymap(lambda x:wt._tofl(x))    
    return df

def get_CONC_EM():
    """
    美原油指数CONC
    --------------------------
    """    
    
    url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI01508580%27)&st=DATADATE&sr=-1&p=1&ps=2000&js=var%20ZPwRtPbD={pages:(tp),data:(x)}&rt=50063532'
    
    r=requests.get(url,headers=hds())
    text=r.text
    text=text.replace('pages','"pages"').replace('data:[','"data":[')
    text=text.split("=")[1]

    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    tp=data['pages']

    if tp>1:
        for i in range(2,tp+1):
            url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI01508580%27)&st=DATADATE&sr=-1&p={0}&ps=2000&js=var%20ZPwRtPbD={1}&rt=50063532'.format(i,'{pages:(tp),data:(x)}')
            
            r=requests.get(url,headers=hds())
            text=r.text
            text=text.replace('pages','"pages"').replace('data:[','"data":[')
            text=text.split("=")[1]

            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    
    df.columns=['date','code','price','change','chg']
    df=df[['date','price','change','chg']]
    df=df.set_index('date')
    df=df.sort_index()
    df=df.applymap(lambda x:wt._tofl(x))    
    return df

def get_SPI_EM():
    """
    资源商品指数Source Product Index
    --------------------------
    """    
    
    url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00662537%27)&st=DATADATE&sr=-1&p=1&ps=20&js=var%2000eVClsGVv={pages:(tp),data:(x)}&rt=50063539'
    
    r=requests.get(url,headers=hds())
    text=r.text
    text=text.replace('pages','"pages"').replace('data:[','"data":[')
    text=text.split("=")[1]

    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    tp=data['pages']

    if tp>1:
        for i in range(2,tp+1):
            url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00662537%27)&st=DATADATE&sr=-1&p={0}&ps=2000&js=var%20eVClsGVv={1}&rt=50063539'.format(i,'{pages:(tp),data:(x)}')
            
            r=requests.get(url,headers=hds())
            text=r.text
            text=text.replace('pages','"pages"').replace('data:[','"data":[')
            text=text.split("=")[1]

            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    
    df.columns=['date','code','price','change','chg']
    df=df[['date','price','change','chg']]
    df=df.set_index('date')
    df=df.sort_index()
    df=df.applymap(lambda x:wt._tofl(x))    
    return df

def get_ZHQPI_EM():
    """
    中纤价格指数：中化纤
    --------------------------
    """    
    
    url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00048726%27)&st=DATADATE&sr=-1&p=1&ps=2000&js=var%20egkqSkew={pages:(tp),data:(x)}&rt=50063546'
    
    r=requests.get(url,headers=hds())
    text=r.text
    text=text.replace('pages','"pages"').replace('data:[','"data":[')
    text=text.split("=")[1]

    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    tp=data['pages']

    if tp>1:
        for i in range(2,tp+1):
            url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00048726%27)&st=DATADATE&sr=-1&p={0}&ps=2000&js=var%20egkqSkew={1}&rt=50063546'.format(i,'{pages:(tp),data:(x)}')
            
            r=requests.get(url,headers=hds())
            text=r.text
            text=text.replace('pages','"pages"').replace('data:[','"data":[')
            text=text.split("=")[1]

            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    
    df.columns=['date','code','price','change','chg']
    df=df[['date','price','change','chg']]
    df=df.set_index('date')
    df=df.sort_index()
    df=df.applymap(lambda x:wt._tofl(x))    
    return df

def get_ZGMHPI_EM():
    """
    中国棉花价格指数：1129B
    --------------------------
    """    
    
    url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00254935%27)&st=DATADATE&sr=-1&p=1&ps=2000&js=var%20dOMsqgAk={pages:(tp),data:(x)}&rt=50063551'
    
    r=requests.get(url,headers=hds())
    text=r.text
    text=text.replace('pages','"pages"').replace('data:[','"data":[')
    text=text.split("=")[1]

    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    tp=data['pages']

    if tp>1:
        for i in range(2,tp+1):
            url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00254935%27)&st=DATADATE&sr=-1&p={0}&ps=2000&js=var%20dOMsqgAk={1}&rt=50063551'.format(i,'{pages:(tp),data:(x)}')
            
            r=requests.get(url,headers=hds())
            text=r.text
            text=text.replace('pages','"pages"').replace('data:[','"data":[')
            text=text.split("=")[1]

            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    
    df.columns=['date','code','price','change','chg']
    df=df[['date','price','change','chg']]
    df=df.set_index('date')
    df=df.sort_index()
    df=df.applymap(lambda x:wt._tofl(x))    
    return df

def get_STI_EM():
    """
    钢铁指数
    --------------------------
    """    
    
    url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00662545%27)&st=DATADATE&sr=-1&p=1&ps=2000&js=var%20CENlUZQH={pages:(tp),data:(x)}&rt=50063561'
    
    r=requests.get(url,headers=hds())
    text=r.text
    text=text.replace('pages','"pages"').replace('data:[','"data":[')
    text=text.split("=")[1]

    data=json.loads(text)
    df=pd.DataFrame(data['data'])
    tp=data['pages']

    if tp>1:
        for i in range(2,tp+1):
            url='http://dcfm.eastmoney.com//EM_MutiSvcExpandInterface/api/js/get?type=QHHQBLDH&token=70f12f2f4f091e459a279469fe49eca5&filter=(ID=%27EMI00662545%27)&st=DATADATE&sr=-1&p={0}&ps=2000&js=var%20CENlUZQH={1}&rt=50063561'.format(i,'{pages:(tp),data:(x)}')
            
            r=requests.get(url,headers=hds())
            text=r.text
            text=text.replace('pages','"pages"').replace('data:[','"data":[')
            text=text.split("=")[1]

            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']))
    
    df.columns=['date','code','price','change','chg']
    df=df[['date','price','change','chg']]
    df=df.set_index('date')
    df=df.sort_index()
    df=df.applymap(lambda x:wt._tofl(x))
    return df




if __name__=="__main__":
    #dd=get_BDI_EM()
    dd=get_TieKuangshi_EM()
