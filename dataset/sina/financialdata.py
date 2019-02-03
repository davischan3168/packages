# -*- coding:utf-8 -*- 
import pandas as pd
import numpy as np
import sys,os,json
import lxml.html
from lxml import etree
import requests
from bs4 import BeautifulSoup
import re
from pandas.compat import StringIO
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
DATE_CHK_MSG = '年度输入错误：请输入1989年以后的年份数字，格式：YYYY'
DATE_CHK_Q_MSG = '季度输入错误：请输入1、2、3或4数字'

DATA_GETTING_TIPS = '[Getting data:]'
DATA_GETTING_FLAG = '#'
def _check_input(year, quarter):
    if isinstance(year, str) or year < 1989 :
        raise TypeError(DATE_CHK_MSG)
    elif quarter is None or isinstance(quarter, str) or quarter not in [1, 2, 3, 4]:
        raise TypeError(DATE_CHK_Q_MSG)
    else:
        return True
def _write_head():
    sys.stdout.write(DATA_GETTING_TIPS)
    sys.stdout.flush()

def _write_console():
    sys.stdout.write(DATA_GETTING_FLAG)
    sys.stdout.flush()
PY3 = (sys.version_info[0] >= 3)

def Financial_Summary(code):
    """
    数据来自sina
    ------------------
    Parameter:
      code:上海和深圳交易所的股票代码
    ---------------------------
    Return:
     DataFrame
        P_date:   公布数据的截止日期
        NASPS：   每股净资产，单位元
        EPS:      每股收益，单位元
        CFPS:     每股现金含量，单位元
        RVSPS:    每股资本公积金，单位元
        FAS:      固定资产合计，单位元
        CAS:      流动资产合计，单位元
        TAS:      资产总计，单位元
        LD:       长期负债合计，单位元
        MIncome:  主营业务收入，单位元
        FFee:     财务费用，单位元
        NetP:     净利润，单位元
    """
    url='http://money.finance.sina.com.cn/corp/go.php/vFD_FinanceSummary/stockid/{}.phtml'.format(code)
    html=requests.get(url)
    soup=BeautifulSoup(html.content.decode('gbk'),'lxml')
    table=soup.find(id="FundHoldSharesTable")
    df=pd.read_html(str(table))[0]
    df=df.drop(0)
    name=['P_date','NASPS','EPS','CFPS','RVSPS','FAS','CAS','TAS','LD','MIncome','FFee','NetP']
    datalist=df.iloc[:,1].tolist()
    dataset=[]
    tem=[]
    n=1
    for x in datalist:
        tem.append(x)
        if re.match(('\d{4}-\d{2}-\d{2}'),str(x)):
            if len(tem)>1:
                dataset.append(tem)
            tem=[]
            tem.append(x)

    df=pd.DataFrame(dataset)
    df=df.drop(12,axis=1)
    df.columns=name
    fn=lambda x:str(x).replace(u'元','').replace(',','').replace('--','')
    df=df.applymap(fn)
    df=df.applymap(lambda x: _to_float(x))
    return df

def BalanceSheet(code):
    """
    数据来自sina,单位均为万元
    ------------------
    Parameter:
      code:上海和深圳交易所的股票代码
    """
    url='http://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/{0}/ctrl/part/displaytype/4.phtml'.format(code)
    html=requests.get(url)
    content=html.content.decode('gbk')
    ht=lxml.html.parse(StringIO(content))
    urlist=ht.xpath('//div[@id="con02-1"]/table/tr[2]/td/a/@href')

    dd=pd.DataFrame()

    for ul in urlist:
        html=requests.get(ul)
        content=html.content.decode('gbk')
        soup=BeautifulSoup(content,'lxml')
        table=soup.find(id='BalanceSheetNewTable0')
        try:
            df=pd.read_html(str(table))[0]
            N=df.shape[1]
            if N==2:
                df.columns=['items',df.iloc[0,1]]
            elif N==3:
                df.columns=['items',df.iloc[0,1],df.iloc[0,2]]
            elif N==4:
                df.columns=['items',df.iloc[0,1],df.iloc[0,2],df.iloc[0,3]]
            elif N==5:            
                df.columns=['items',df.iloc[0,1],df.iloc[0,2],df.iloc[0,3],df.iloc[0,4]]
            df=df.set_index('items')
            dd=pd.concat([dd,df],axis=1)
        except:
            pass
    dd=dd.drop('报表日期')
    dd=dd.applymap(lambda x:str(x).replace('--',''))
    dd=dd.applymap(lambda x: _to_float(x))
    return dd.T

def IncomeStatement(code):
    """
    数据来自sina,单位均为万元（每股收益为元）
    ------------------
    Parameter:
      code:上海和深圳交易所的股票代码
    """    
    url='http://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/{0}/ctrl/part/displaytype/4.phtml'.format(code)
    html=requests.get(url)
    content=html.content.decode('gbk')
    ht=lxml.html.parse(StringIO(content))
    urlist=ht.xpath('//div[@id="con02-1"]/table/tr[2]/td/a/@href')

    dd=pd.DataFrame()

    for ul in urlist:
        html=requests.get(ul)
        content=html.content.decode('gbk')
        soup=BeautifulSoup(content,'lxml')
        table=soup.find(id='ProfitStatementNewTable0')
        try:
            df=pd.read_html(str(table))[0]
            N=df.shape[1]
            if N==2:
                df.columns=['items',df.iloc[0,1]]
            elif N==3:
                df.columns=['items',df.iloc[0,1],df.iloc[0,2]]
            elif N==4:
                df.columns=['items',df.iloc[0,1],df.iloc[0,2],df.iloc[0,3]]
            elif N==5:            
                df.columns=['items',df.iloc[0,1],df.iloc[0,2],df.iloc[0,3],df.iloc[0,4]]
            df=df.set_index('items')
            dd=pd.concat([dd,df],axis=1)
        except:
            pass
    dd=dd.drop('报表日期')
    dd=dd.applymap(lambda x: str(x).replace('--',''))
    dd=dd.applymap(lambda x: _to_float(x))
    
    return dd.T


def CashFlowStatement(code):
    """
    数据来自sina,单位均为万元
    ------------------
    Parameter:
      code:上海和深圳交易所的股票代码
    """    
    url='http://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/{0}/ctrl/part/displaytype/4.phtml'.format(code)
    html=requests.get(url)
    content=html.content.decode('gbk')
    ht=lxml.html.parse(StringIO(content))
    urlist=ht.xpath('//div[@id="con02-1"]/table/tr[2]/td/a/@href')

    dd=pd.DataFrame()

    for ul in urlist:
        html=requests.get(ul)
        content=html.content.decode('gbk')
        soup=BeautifulSoup(content,'lxml')
        table=soup.find(id='ProfitStatementNewTable0')
        try:
            df=pd.read_html(str(table))[0]
            N=df.shape[1]
            if N==2:
                df.columns=['items',df.iloc[0,1]]
            elif N==3:
                df.columns=['items',df.iloc[0,1],df.iloc[0,2]]
            elif N==4:
                df.columns=['items',df.iloc[0,1],df.iloc[0,2],df.iloc[0,3]]
            elif N==5:            
                df.columns=['items',df.iloc[0,1],df.iloc[0,2],df.iloc[0,3],df.iloc[0,4]]
            df=df.set_index('items')
            dd=pd.concat([dd,df],axis=1)
        except:
            pass
    dd=dd.drop('报告期')
    dd=dd.applymap(lambda x:str(x).replace('--',''))
    dd=dd.applymap(lambda x: _to_float(x))
    return dd.T

def Finance_Index(code):
    url='http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{0}/displaytype/4.phtml'.format(code)
    html=requests.get(url)
    content=html.content.decode('gbk')
    ht=lxml.html.parse(StringIO(content))
    urlist=ht.xpath('//div[@id="con02-1"]/table[1]//a/@href')
    
    dd=pd.DataFrame()

    for ul in urlist:
        html=requests.get(ul)
        content=html.content.decode('gbk')
        soup=BeautifulSoup(content,'lxml')
        table=soup.find(id='BalanceSheetNewTable0')
        try:
            df=pd.read_html(str(table))[0]
            N=df.shape[1]
            if N==2:
                df.columns=['items',df.iloc[0,1]]
            elif N==3:
                df.columns=['items',df.iloc[0,1],df.iloc[0,2]]
            elif N==4:
                df.columns=['items',df.iloc[0,1],df.iloc[0,2],df.iloc[0,3]]
            elif N==5:
                df.columns=['items',df.iloc[0,1],df.iloc[0,2],df.iloc[0,3],df.iloc[0,4]]
            df=df.set_index('items')
            dd=pd.concat([dd,df],axis=1)
        except:
            pass
    dd=dd.drop('报告日期')
    dd=dd.applymap(lambda x:str(x).replace('--',''))
    dd=dd.applymap(lambda x: _to_float(x))
    return dd.T

def _to_float(x):
    try:
        return(float(x))
    except:
        pass

if __name__=="__main__":
    #df=Financial_Summary('000039')
    #d=BalanceSheet('000039')
    d=IncomeStatement('000039')
    #f=CashFlowStatement('000039')
