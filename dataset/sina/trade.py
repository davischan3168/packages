#!/usr/bin/env python3
# -*-coding:utf-8-*-

import requests,json
import pandas as pd
import numpy as np
import lxml.html
from lxml import etree
import time,sys
import datetime as dt
from bs4 import BeautifulSoup
today=time.strftime('%Y_%m_%d')
from io import StringIO
import webdata.puse.sinapy.cons as ws
from selenium import webdriver
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = ('Mozilla/5.0(WindowsNT6.1;WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/59.0.3071.115Safari/537.36x-requested-with:XMLHttpRequest')
dcap["phantomjs.page.settings.loadImages"] = True    
driver=webdriver.PhantomJS(desired_capabilities=dcap)

def US_datasina(code,end=today,mtype='day'):
    """
    获得美国近年上市公司的股票交易数据
    """
    urls={'day':'http://stock.finance.sina.com.cn/usstock/api/jsonp_v2.php/var_{0}=/US_MinKService.getDailyK?symbol={1}&_={2}&___qn=3','mm':'http://stock.finance.sina.com.cn/usstock/api/jsonp_v2.php/var{0}_{2}_{1}=/US_MinKService.getMinK?symbol={0}&type={2}&___qn=3'}
    if mtype=="day":
        codetimeflag=code+end
        #url='http://stock.finance.sina.com.cn/usstock/api/jsonp_v2.php/var_{0}=/US_MinKService.getDailyK?symbol={1}&_={2}&___qn=3'.format(codetimeflag,code,end)
        url=urls[mtype].format(codetimeflag,code,end)
    elif mtype in ['m5','m15','m30','m60']:
        mt=mtype.replace('m','')
        dtstamp=int(dt.datetime.timestamp(dt.datetime.today())*1000)
        url=urls['mm'].format(code,dtstamp,mt)
    else:
        sys.exit()
        
    r=requests.get(url)
    text=r.text
    text=text.split("=")[1]
    text=text.replace('([{','').replace('}]);','')
    text=text.replace('},{','\n')
    text=text.replace('"o":','').replace('"d":','')
    text=text.replace('"o":','').replace('"d":','')
    text=text.replace('"h":','').replace('"l":','')
    text=text.replace('"c":','').replace('"v":','')
    df=pd.read_csv(StringIO(text),header=None)
    df.columns=['date','open','high','low','close','volume']
    #print(df.head())
    df['date']=pd.to_datetime(df['date'])
    df=df.set_index('date')
    df=df.applymap(lambda x:float(x))
    return df

def HK_datasina_byquarter(code,year,quarter):
    """
    code: 香港的股票代码，like 00005,
    year:年度，str,like 2018
    quarter:季度,str,like 4
    -----------------------
    Return:
         DataFrame
    """
    url='http://stock.finance.sina.com.cn/hkstock/history/{}.html'.format(code)

    driver.get(url)
    driver.implicitly_wait(5)
    sel = Select(driver.find_element_by_xpath("//select[@id='selectYear']"))
    #Select(sel).select_by_value(year)
    sel.select_by_value(year)
    #ssel = driver.find_element_by_xpath("//select[@id='selectSeason']")
    sell = Select(driver.find_element_by_id('selectSeason'))
    #Select(ssel).select_by_value(quarter)
    sell.select_by_value(quarter)
    driver.find_element_by_xpath("//div[@class='part02']/div/form/input[@type='submit']").click()

    soup=BeautifulSoup(driver.page_source,'lxml')
    table=soup.find_all('table')
    data=table[0]
    df=pd.read_html(str(data),header=0)[0]
    df.columns=['Date','Close','Diff','Chg','Volume','Amount','Open','High','Low','Amplitude']    
    return df

def make_ym(i):
    year=str(i)[:4]
    dd=[]
    if str(i)[5:7] in ['01','02','03']:
        quarter='1'
        dd.append((year,quarter))
    elif str(i)[5:7] in ['04','05','06']:
        quarter='2'
        dd.append((year,quarter))            
    elif str(i)[5:7] in ['07','08','09']:
        quarter='3'
        dd.append((year,quarter)) 
    elif str(i)[5:7] in ['10','11','12']:
        quarter='4'
        dd.append((year,quarter))
    return dd
        

def HK_datasina(code,start=None,end=None):
    """
    code: 香港的股票代码，like 00005,
    start:开始年度和季度，str,like 2010-01
    end:结束年度和季度，str,like 2010-01
    -----------------------
    Return:
         DataFrame
    """    
    url='http://stock.finance.sina.com.cn/hkstock/api/jsonp.php//HistoryTradeService.getHistoryRange?symbol=%s'%code
    
    r=requests.get(url)
    text=r.text.replace('((','').replace('));','').replace('max','"max"').replace('min','"min"')
    data=json.loads(text)
    maxx=dt.datetime.strptime(data['max'],'%Y-%m')
    minn=dt.datetime.strptime(data['min'],'%Y-%m')
    #print(maxx,minn)

    #"""
    if start is None:
        start=str(minn)[:10]
    elif start < str(minn):
        start=str(minn)[:10]

    if end is None:
        end=str(maxx)[:10]
    elif end > str(maxx):
        end=str(maxx)[:10]#"""

    if not isinstance(start,dt.datetime):
        try:
            start=dt.datetime.strptime(start,'%Y-%m')
        except:
            start=dt.datetime.strptime(start,'%Y-%m-%d')

    if not isinstance(end,dt.datetime):
        try:
            end=dt.datetime.strptime(end,'%Y-%m')
        except:
            end=dt.datetime.strptime(end,'%Y-%m-%d')

    end=end+dt.timedelta(days=93)
        
    ttradelist=pd.date_range(start,end,freq='q')
    dd=[]    
    for i in ttradelist:
        dd.extend(make_ym(i))
    df=pd.DataFrame()
    #print(dd)
    for ym in dd:
        #print(ym)
        try:
            dff=HK_datasina_byquarter(code,ym[0],ym[1])
            #print(dff.head(2))
            df=df.append(dff)
        except Exception as e:
            print(e)
            #pass
            
    
    df=df.set_index('Date')
    df=df.applymap(lambda x:ws._tofl(x))
    df=df.applymap(lambda x:np.where(x=='--',np.nan,x))
    df=df.dropna(how='all')
    df.index=df.index.map(lambda x: dt.datetime.strptime(str(x),'%Y%m%d'))
    df=df.sort_index()
    return df

name=["name",'cname','category','symbol','price','diff','chg','preclose','open','high','low','amplitude','volume','mktcap','pe','market','category_id',]

def US_allsina(n=139):
    url="http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['doRC9iO10SZezYVc']/US_CategoryService.getList?page={0}&num=60&sort=&asc=1&market=&id="
    
    df=pd.DataFrame()
    for i in range(1,int(n)+1):
        urld=url.format(i)
        #print(urld)
        r=requests.get(urld)
        delfname=["cname:",'name:','price:','symbol:','diff:','chg:','preclose:','open:','high:','low:','amplitude:','volume:','mktcap:','pe:','market:','category_id:','category:']
        try:
            text=r.text.split("data:[{")[1]
            text=text.replace("}]}));",'')
            text=text.replace('},{','\n')
            for nm in delfname:
                text=text.replace(nm,'')
                #print(text)
            dff=pd.read_csv(StringIO(text),header=None)
            dff.columns=name
            df=df.append(dff)
        except Exception as e:
            pass
            
    df=df.applymap(lambda x:ws._tofl(x))
    df=df.applymap(lambda x:np.where(x=='--',np.nan,x))
    df=df.replace('null',np.nan)
    df=df.set_index('symbol')
    return df

def get_dadan_sina(code,opt=1,dt=None):
    """
    code:
    opt:成交量大于等于（≥）:
            1： 400手,2: 500手,3: 600手,4: 700手,5: 800手,6: 900手,7: 1000手,
            8: 2000手,9: 5000手,10: 10000手
        成交额大于等于（≥）: 
            11:50万,12: 100万,13: 200万,14: 500万 ,15:1000万
        上一交易日平均每笔成交量（≥）: 
            16:5倍 ,17:10倍 ,18:20倍,19: 50倍,20: 100倍
    dt: 交易的时间
    ------------------
    Return:
        code:
        name：
        time'：
        price：
        volume：
        prev_price：
        kind: U --Buy,D--Sell,E--中性盘
    
    """
    
    if code[0] in ['6','9']:
        code='sh'+code
    else:
        code='sz'+code

    if dt is None:
        dt=time.strftime('%Y-%m-%d',time.localtime())

    dd={1:{'v':40000,'a':0,'t':0},2:{'v':50000,'a':0,'t':0},3:{'v':60000,'a':0,'t':0},4:{'v':70000,'a':0,'t':0},5:{'v':80000,'a':0,'t':0},6:{'v':90000,'a':0,'t':0},7:{'v':100000,'a':0,'t':0},8:{'v':200000,'a':0,'t':0},9:{'v':500000,'a':0,'t':0},10:{'v':1000000,'a':0,'t':0},11:{'v':0,'a':500000,'t':0},12:{'v':0,'a':1000000,'t':0},13:{'v':0,'a':2000000,'t':0},14:{'v':0,'a':5000000,'t':0},15:{'v':0,'a':10000000,'t':0},16:{'v':0,'a':0,'t':1},17:{'v':0,'a':0,'t':2},18:{'v':0,'a':0,'t':3},19:{'v':0,'a':0,'t':4},20:{'v':0,'a':0,'t':5}}
    
    #dataset=[]
    df=pd.DataFrame()
    for p in range(1,10):
        url='http://vip.stock.finance.sina.com.cn/quotes_service/api/json_v2.php/CN_Bill.GetBillList?symbol={0}&num=60&page={5}&sort=ticktime&asc=0&volume={1}&amount={2}&type={3}&day={4}'.format(code,dd[opt]['v'],dd[opt]['a'],dd[opt]['t'],dt,p)
        r=requests.get(url)
        if len(r.text)>10:
            text=r.text
            dtext=text.replace('[{','')
            dtext=dtext.replace('}]','')
            dtext=dtext.replace('prev_price:','')
            dtext=dtext.replace('symbol:','')
            dtext=dtext.replace('name:','')
            dtext=dtext.replace('ticktime:','')
            dtext=dtext.replace('volume:','')
            dtext=dtext.replace('kind:','')
            dtext=dtext.replace('},{','\n')
            dtext=dtext.replace('price:','')
            df=df.append(pd.read_csv(StringIO(dtext),header=None))

    try:       
        df.columns=['code','name','time','price','volume','prev_price','kind']
        for lb in ['price','volume','prev_price']:
            df[lb]=df[lb].astype(float)

        df['code']=df['code'].map(lambda x:x[2:])
        df=df.sort_values(by='time')
        df=df.reset_index(drop=True)
    except Exception as e:
        print(e)
        #pass
    df=df.replace('U','B').replace('D','S')
    return df
            
        
        
if __name__=="__main__":
    #df=get_us_allsina()
    #df=get_dadansina(sys.argv[1])
    #df=get_us_datasina(sys.argv[1],mtype=sys.argv[2])
    #df=get_hk_datasina_byquarter(sys.argv[1],sys.argv[2],sys.argv[3])
    
    df=get_hk_datasina('00005',start='2010-01',end='2016-04')
    
