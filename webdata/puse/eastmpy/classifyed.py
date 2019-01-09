#!/usr/bin/env python3
# -*-coding:utf-8-*-
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json,pickle
from io import StringIO
import pandas as pd
import sys,os,requests,time
from datetime import datetime
import webdata.puse.eastmpy.cont as wt

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = ('Mozilla/5.0(WindowsNT6.1;WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/59.0.3071.115Safari/537.36x-requested-with:XMLHttpRequest')
dcap["phantomjs.page.settings.loadImages"] = True
driver = webdriver.PhantomJS(desired_capabilities=dcap)

def get_bkid():
    urls=['http://data.eastmoney.com/bkzj/hy.html','http://data.eastmoney.com/bkzj/dy.html','http://data.eastmoney.com/bkzj/gn.html']

    urlsets={}
    for url in urls:
        driver.get(url)
        driver.implicitly_wait(3)
        tems=driver.find_elements_by_xpath('//div[@class="content1"]//a')
        for u in tems:
            ul=u.get_attribute('href')
            name=u.text.replace(' ','')
            urlsets[name]=ul
            #print(ul,name)

    f=open('output/eastmsource/bkurls.pkl','wb')
    pickle.dump(urlsets,f)
    f.close()
    return urlsets

def get_code_classified_EM(name,mtype=1):

    names=wt.bkurlsets.keys()
    flag=True
    if name not in names:
        while flag:
            name =input("Input BK name:")
            if name in names:
                flag=False
                
        
    bkid=os.path.splitext(os.path.basename(urlsets[name]))[0]+'1'
    
    if int(mtype)==1:
        url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C.{0}&type=ct&st={2}&sr=-1&p=1&ps=1000&js={1}&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITA&rt=50334262'.format(bkid,'{%22pages%22:(pc),%22data%22:[(x)]}','(BalFlowMain)')
    elif int(mtype)==5:
        url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C.{0}&type=ct&st={2}&sr=-1&p=1&ps=1000&js={1}&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITA5&rt=50334262'.format(bkid,'{%22pages%22:(pc),%22data%22:[(x)]}','(BalFlowMainNet5)')
    elif int(mtype)==10:
        url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C.{0}&type=ct&st={2}&sr=-1&p=1&ps=1000&js={1}&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITA10&rt=50334262'.format(bkid,'{%22pages%22:(pc),%22data%22:[(x)]}','(BalFlowMainNet10)')
        
    r=requests.get(url)
    data=json.loads(r.text)
    df=pd.read_csv(StringIO('\n'.join(data['data'])),header=None)
    df=df.drop(0,axis=1)
    df.columns=['code','name','price','pct','Main_net','Main_pct','Sup_net','Sup_pct','Big_net','Big_pct','Mid_net','Mid_pct','Sm_net','Sm_pct','Date']
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    df=df.sort_values(by='pct',ascending=False)
    return df

def get_bkindex_EM(name,mtype='D'):
    mtp={'d':'k','wk':'wk','mk':'mk','5min':'m5k','15min':'m15k','30min':'m30k','60min':'m60k'}
    mtype=mtype.lower()
    timestamp=int(time.time()*1000)

    names=wt.bkurlsets.keys()
    flag=True
    if name not in names:
        while flag:
            name =input("Input BK name:")
            if name in names:
                flag=False
                
        
    bkid=os.path.splitext(os.path.basename(urlsets[name]))[0]+'1'
    url='http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=%s&TYPE=%s&js=(x)&rtntype=5&isCR=false&fsData%s'%(bkid,mtp[mtype],timestamp)
    r=requests.get(url)
    text=r.text
    #print(text[:300])
    data=json.loads(text)
    df=pd.read_csv(StringIO('\n'.join(data['data'])),header=None)
    df.columns=['date','open','close','high','low','volume','amount','amplitude']
    df=df.set_index('date')
    df.index=pd.to_datetime(df.index)
    for label in df.columns:
        try:
            df[label]=df[label].astype(float)
        except:
            df[label]=df[label].map(lambda x: wt._tofl(x))
    return df

if __name__=="__main__":
    #df=get_code_classified(sys.argv[1],sys.argv[2])
    df=get_bkindex_EM(sys.argv[1])
