# -*- coding:utf-8 -*- 
"""
"""
import pandas as pd
import sys,requests
import lxml.html
from lxml import etree
import datetime
import re,os
from io import StringIO
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
import time
try:
    import urllib
except:
    import urllib2 as urllib
import numpy as np
from bs4 import BeautifulSoup
from openpyxl import Workbook
from webdata.util.hds import user_agent as hds
from webdata.util.rw import ReadFile
from urllib.request import urlretrieve


    

def _set_code(code):
    if code[0] in ['0','2','3']:
        code='sz'+code
    elif code[0] in ['6','9']:
        code='sh'+code
    else:
        print(u'code 是深圳和上海交易所的股票代码.')
    return code

def tick_data_today(code):
    """
    Parameter：
              code: 上海和深圳的股票代码，为6位数字符
    return:
          DataFrame:
               time:  交易的时间
               price: 成交的价格,float
               change:
               volumn: 成交量，单位手，即100的整数倍
               amount: 成交金额，单位元
               type:   B 买入,S 卖出,M 中性盘
    """
    code=_set_code(code)
    detail=[]
    d=pd.DataFrame()
    for i in range(1000):
        url='http://stock.gtimg.cn/data/index.php?appn=detail&action=data&c={0}&p={1}'.format(code,i)
        try:
            #print("Getting page %s" %i)
            r=requests.get(url,headers=hds())
            r=r.text.split(',"')[1]
            r=r.split('"]')[0]
            #break
            dat=r.split('|')
            for data in dat:
                data=data.split('/')
                detail.append(data)
        except Exception as e:
            #print(e)
            #pass
            break
    dataset=pd.DataFrame(detail)
    dataset=dataset.drop(0,axis=1)
    name=['time','price','change','volume','amount','type']
    dataset.columns=name
    for label in ['price','change','volume','amount']:
        dataset[label]=dataset[label].astype(float)
    return dataset


def get_dadan(code,opt=4):
    """
    默认是以400手
    Parameters:
             code:  上海和深圳的股票代码
             opt:   1-9:的数字代表成交量，分别为100手，
                    200手,300,400,500,800,1000,1500,2000手
                    10-13:代表成交额大于等于 100万元、200、500、1000万元
   Return:
         time:      股票成交的时间
         price:     股票成交的价格（元）
         volumn     股票成交的股数（手，即100股的整数倍）
         amount:    股票成交金额（万元）
         type:      买（B）或卖（S)
    """
    
    code=_set_code(code)
    url='http://stock.finance.qq.com/sstock/list/view/dadan.php?t=js&c={0}&max=800000&p=1&opt={1}&o=0'.format(code,opt)
    r=requests.get(url,headers=hds())
    r=r.text.split(",'")[1]
    r=r.split("']")[0]
    r=r.split('^')
    dataset=[]
    for data in r:
        #print(data)
        data=data.split('~')
        dataset.append(data)
    df=pd.DataFrame(dataset)
    df=df.drop(0,axis=1)
    df.columns=['time','price','volume','amount','type']
    for label in ['price','volume','amount']:
        df[label]=df[label].astype(float)
    return df

def finance_share_news(code):
    """
    获取股票个股新闻的标题和内容
    --------------------------------
    Parameter:
             code:  股票代码，String like，600026
    Return:
             title:      标题
             url：       网址
             datetime：  新闻发布时间
             id：        识别号
             code：      与相关股份的相应
   
    """
    code=_set_code(code)
    url='http://news2.gtimg.cn/lishinews.php?name=finance_news&symbol={0}&page=1'.format(code)
    #print(url)
    r=requests.get(url,headers=hds())
    content=r.text
    pageN=re.findall('"total_page":\d+',content)
    pageNo=int(re.findall('\d+',pageN[0])[0])+1
    tem=[]
    for i in range(pageNo):
        url='http://news2.gtimg.cn/lishinews.php?name=finance_news&symbol={0}&page={1}'.format(code,i)
        r=requests.get(url,headers=hds())
        content=r.content.decode('unicode-escape')#decode('gb18030')
        r=content.split(':{"data":[')[1][:-1]
        r=r.split('}],')[0]
        newslist=r.split('},{')
        for news in newslist:
            news=news.split(',')
            tem1=[]
            for n in news:
                try:
                    #name=n.split('":"',1)[0]
                    value=n.split('":"',1)[1]
                    value=value.replace('"','')
                    #if '\\' in value:
                    value=value.replace('\\','')
                    #print(u'%s'%value)
                    tem1.append(value)
                except:
                    pass
            tem.append(tem1)
    df=pd.DataFrame(tem)
    df.columns=['title','url','datetime','id','code']
    return df

def hist_tick_pershare(code,date):
    """
    按日期获取每天的每笔交易数据。
    Parameter：
    --------------------------
    code:上海、深圳的股票代码
    date:交易日期，like "20170113"
    ---------------------------
    Return:
          DataFrame:
              datetime:成交时间
              price:   成交价格
              change:  价格变动
              volume:  成交量(手)
              amount:  成交额(元)
              type:    性质
              date:    该笔交易的日期
          
    """
    code=_set_code(code)
    url='http://stock.gtimg.cn/data/index.php?appn=detail&action=download&c={0}&d={1}'.format(code,date)
    filepath="%s_%s.csv"%(code,date)
    urlretrieve(url,filepath)
    content=ReadFile(filepath,encoding='gbk')
    cc=StringIO(content)
    df=pd.read_table(cc)
    df['date']=date
    os.remove(filepath)
    try:
        #df.columns=['datetime','price','change','volume','amount','type']
        df.rename(columns={u'成交时间': 'datetime',u'成交价格': 'price', u'价格变动': 'change',u'成交量(手)': 'volume',u'成交额(元)': 'amount',u'性质':'type'}, inplace=True)
        for label in ['price','change','volume','amount']:
            df[label]=df[label].astype(float)
    except:
        pass
    df=df.replace('买盘','B').replace('卖盘','S').replace('中性盘','M')
    return df

def hist_tick(code,start,end):
    """
    获取某只股票一段时间内的tick数据。
    -------------------------------
    Parameter:
       code:  股票代码
       start: 开始日期
       end:   截止日期
    -------------------------------
    Return:
          DataFrame:
              datetime:成交时间
              price:   成交价格
              change:  价格变动
              volume:  成交量(手)
              amount:  成交额(元)
              type:    性质
              date:    该笔交易的日期
    """
    date_range=pd.date_range(start=start,end=end,freq='B')
    tick_data=pd.DataFrame()
    for date in date_range:
        date=date.strftime("%Y%m%d")
        df=hist_tick_pershare(code,date)
        if not df.empty:
            tick_data=tick_data.append(df)

    return tick_data

def vmprice(code):
    """
    获得股票最近交易日的成交量加权平均价格
    """
    day=datetime.datetime.today()
    if day.hour<16:
        df=tick_data_today(code)
    else:
        if day.weekday()==5:
            day=day-datetime.timedelta(days=1)
        elif day.weekday()==6:
            day=day-datetime.timedelta(days=2)
        df=hist_tick_pershare(code,day.strftime('%Y%m%d'))

    price=(df['price']*df['volume']).sum()/(df['volume'].sum())
    print(price)
    return price
    
#http://stock.finance.qq.com/cgi-bin/sstock/hyxw?ZHENGQUANDM=600066&pt=04ZC70&p=1
def _read_table(text,dataset):
    tbs=text.xpath('//table[@class="r_con"]/tr[position()>2]')
    for tb in tbs:
        name=tb.xpath('td[1]/a/text()')
        href=tb.xpath('td[1]/a/@href')
        time=tb.xpath('td[2]/text()')
        try:
            n=name[0]
            h=href[0]
            t=time[0]
            dataset.append([n,h,t])
            
        except:
            pass
    return

def qqhyxw(code):
    """
    获取股票所在行业新闻的标题
    """
    url='http://stockhtm.finance.qq.com/sstock/ggcx/{0}.shtml'.format(code)

    html=requests.get(url,headers=hds())
    soup=BeautifulSoup(html.content,'lxml')
    dataset=[]
    
    url=soup.find_all('a',text='行业新闻')[0].get('href')
    html=requests.get(url)
    content=html.content.decode('gbk')
    text=lxml.html.parse(StringIO(content))
    _read_table(text,dataset)
    
    for _ in range(11):
        soup=BeautifulSoup(content,'lxml')
        try:
            nexturl=soup.find('a',text='下一页').get('href')
            html=requests.get(nexturl,headers=hds())
            content=html.content.decode('gbk')
            text=lxml.html.parse(StringIO(content))
            _read_table(text,dataset)
        except Exception as e:
            print(e)

    df=pd.DataFrame(dataset)
    df.columns=['name','href','datetime']
    return df

        
def get_text(url):
    """
    获取网址对应的标题、和内容。
    --------------
    url：输入的网址
    -----------------
    return：
          title:文章的标题
               ：相应的网址内容。
    """
    html=requests.get(url,headers=hds())
    con=lxml.html.parse(StringIO(html.text))
    
    #ti=con.xpath("/h1/text()")
    tt=con.xpath('//div[@id="Cnt-Main-Article-QQ"]/p')
    textset=[]
    for  t in tt:
        try:
            text=t.xpath('text()')[0]
            text=text.strip()
            textset.append(text)
        except Exception as e:
            #print(e)
            pass
    return '\n\n'.join(textset)

def qqfinance_index(code):
    """获取某只股票的财务指标
    Parameter：
           code：上海、深圳交易所的股票代码
    -------------------------------------
    Return：
          DataFrame：
                    单位均为元(万元或元）。
    """
    url='http://stock.finance.qq.com/corp1/mfratio.php?zqdm={0}'.format(code)
    html=requests.get(url,headers=hds())
    h=lxml.html.parse(StringIO(html.text))
    urls=h.xpath('//div[@class="right"]/table[2]/tr/td/a/@href')
    AT=pd.DataFrame()
    for url in urls:
        html=requests.get(url,headers=hds())
        soup=BeautifulSoup(html.text,'lxml')
        table=soup.find_all('table',attrs={'class','list'})
        df=pd.read_html(str(table))[0]
        df=df.dropna(how='all',axis=1)
        df=df.T
        df.columns=df.ix[0,:]
        df=df.drop(0,axis=0)
        AT=AT.append(df)
    AT=AT.set_index('报告期')
    AT=AT.dropna(how='all',axis=1)
    AT=AT.applymap(lambda x:_str2fl(x))
    AT=AT.sort_index()
    return AT


def qqfinance_summary(code):
    """获取某只股票的财务指标
    Parameter：
           code：上海、深圳交易所的股票代码
    -------------------------------------
    Return：
          DataFrame：
                    单位均为元(万元或元）。
    """    
    url='http://stock.finance.qq.com/corp1/annual_sum.php?zqdm={0}&type=0'.format(code)
    html=requests.get(url,headers=hds())
    h=lxml.html.parse(StringIO(html.text))
    urls=h.xpath('//div[@class="right"]/table[3]/tr/td/a/@href')
    urls.append(url)
    AT=pd.DataFrame()
    for url in urls:
        html=requests.get(url,headers=hds())
        soup=BeautifulSoup(html.text,'lxml')
        table=soup.find_all('table',attrs={'class','list'})
        df=pd.read_html(str(table))[0]
        df=df.drop([0,10,18,11,19],axis=0)
        df=df.dropna(how='all',axis=1)
        df=df.dropna(how='all',axis=0)
        df=df.T
        df.columns=df.ix[0,:]
        df=df.drop(0,axis=0)
        #print(df)
        AT=AT.append(df)
    AT=AT.set_index('报告期')
    AT=AT.dropna(how='all',axis=1)
    AT=AT.applymap(lambda x:_str2fl(x))
    AT=AT.sort_index()
    return AT

def qqfinance_BS(code):
    """获取某只股票的财务指标
    Parameter：
           code：上海、深圳交易所的股票代码
    -------------------------------------
    Return：
          DataFrame：
                    单位均为元(万元或元）。
    """    
    url='http://stock.finance.qq.com/corp1/cbsheet.php?zqdm={0}'.format(code)
    html=requests.get(url,headers=hds())
    h=lxml.html.parse(StringIO(html.text))
    urls=h.xpath('//div[@class="right"]/table[2]/tr/td/a/@href')
    AT=pd.DataFrame()
    for url in urls:
        html=requests.get(url,headers=hds())
        soup=BeautifulSoup(html.text,'lxml')
        table=soup.find_all('table',attrs={'class','list'})
        df=pd.read_html(str(table))[0]
        df=df.dropna(how='all',axis=1)
        df=df.T
        df.columns=df.ix[0,:]
        df=df.drop(0,axis=0)
        AT=AT.append(df)
    AT=AT.set_index('报表日期')
    AT=AT.dropna(how='all',axis=1)
    AT=AT.applymap(lambda x:_str2fl(x))
    AT=AT.sort_index()
    return AT

def qqfinance_CF(code):
    """获取某只股票的财务指标
    Parameter：
           code：上海、深圳交易所的股票代码
    -------------------------------------
    Return：
          DataFrame：
                    单位均为元(万元或元）。
    """    
    url='http://stock.finance.qq.com/corp1/cfst.php?zqdm={0}'.format(code)
    html=requests.get(url,headers=hds())
    h=lxml.html.parse(StringIO(html.text))
    urls=h.xpath('//div[@class="right"]/table[2]/tr/td/a/@href')
    AT=pd.DataFrame()
    for url in urls:
        html=requests.get(url,headers=hds())
        soup=BeautifulSoup(html.text,'lxml')
        table=soup.find_all('table',attrs={'class','list'})
        df=pd.read_html(str(table))[0]
        df=df.dropna(how='all',axis=1)
        df=df.T
        df.columns=df.ix[0,:]
        df=df.drop(0,axis=0)
        AT=AT.append(df)
    AT=AT.set_index('报表日期')
    AT=AT.dropna(how='all',axis=1)
    AT=AT.applymap(lambda x:_str2fl(x))
    AT=AT.sort_index()
    return AT

def qqfinance_InSt(code):
    """获取某只股票的财务指标
    Parameter：
           code：上海、深圳交易所的股票代码
    -------------------------------------
    Return：
          DataFrame：
                    单位均为元(万元或元）。
    """
    url='http://stock.finance.qq.com/corp1/inst.php?zqdm={0}'.format(code)
    html=requests.get(url,headers=hds())
    h=lxml.html.parse(StringIO(html.text))
    urls=h.xpath('//div[@class="right"]/table[2]/tr/td/a/@href')
    AT=pd.DataFrame()
    for url in urls:
        html=requests.get(url,headers=hds())
        soup=BeautifulSoup(html.text,'lxml')
        table=soup.find_all('table',attrs={'class','list'})
        df=pd.read_html(str(table))[0]
        df=df.dropna(how='all',axis=1)
        df=df.T
        df.columns=df.ix[0,:]
        df=df.drop(0,axis=0)
        AT=AT.append(df)
    AT=AT.set_index('报表日期')
    AT=AT.dropna(how='all',axis=1)
    AT=AT.applymap(lambda x:_str2fl(x))
    AT=AT.sort_index()
    return AT

def _str2fl(x):
    if '万元' in x:
        x=x.replace('万元','')
        x=x.replace(',','')
        x=float(x)
        #x=float(x)*10000
        return x
    elif '元' in x:
        x=x.replace('元','')
        x=x.replace(',','')
        x=float(x)
        return x
    elif '--' in x:
        x=x.replace('--','')
        return x
    else:
        return np.nan
     
    
    
        
if __name__=="__main__":
    #df=tick_data_today('300019')
    #df=qq_share_news('300019')    
    #df=hist_tick_pershare(,date)
    #df=hist_tick('300006',start='20170101',end='20170313')
    #r=vmprice('000039')
    #df=qqggxw('000039')
    #df=finance_share_news('000039')
    #df=qqfinance_index('000039')
    df=qqfinance_InSt('000039')
