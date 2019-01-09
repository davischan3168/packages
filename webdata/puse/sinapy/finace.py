#!/usr/bin/env python3
# -*-coding:utf-8-*-
import pandas as pd
import numpy as np
import sys,os
import lxml.html
from lxml import etree
import requests
from io import StringIO
from bs4 import BeautifulSoup


def BS_sina(code):
    """
    20170616，测试有问题
    获得个股的资产负责表
    -------
    Return
    """
    DF=pd.DataFrame()
    url='http://money.finance.sina.com.cn/corp/go.php/vFD_BalanceSheet/stockid/{0}/ctrl/part/displaytype/4.phtml'.format(code)
    r=requests.get(url)
    r=r.content.decode('gbk')
    html=lxml.html.parse(StringIO(r))
    urls=html.xpath("//div[@id='con02-1']/table[1]//a/@href")
    
    for url in urls:
        r=requests.get(url)
        r=r.content.decode('gbk')
        html=BeautifulSoup(r,'lxml')
        text=html.find(id='BalanceSheetNewTable0')
        df=pd.read_html(str(text),header=0)[0]
        df.columns=df.iloc[0,:]
        df=df.drop(0,axis=0)
        df=df.set_index('报表日期')
        df=df.T
        #print(df)
        DF=DF.append(df)    

    return DF

def IS_sina(code):
    """
    20170616，测试有问题
    获得个股的利润表
    -------
    Return
    """    
    DF=pd.DataFrame()
    url='http://money.finance.sina.com.cn/corp/go.php/vFD_ProfitStatement/stockid/{0}/ctrl/part/displaytype/4.phtml'.format(code)
    r=requests.get(url)
    r=r.content.decode('gbk')
    html=lxml.html.parse(StringIO(r))
    urls=html.xpath("//div[@id='con02-1']/table[1]//a/@href")
    
    for url in urls:
        r=requests.get(url)
        r=r.content.decode('gbk')
        html=BeautifulSoup(r,'lxml')
        text=html.find(id='ProfitStatementNewTable0')
        df=pd.read_html(str(text),header=0)[0]
        df.columns=df.iloc[0,:]
        df=df.drop(0,axis=0)
        df=df.set_index('报表日期')
        df=df.T
        #print(df)
        DF=DF.append(df)    

    return DF

def CS_sina(code):
    """
    20170616，测试有问题
    获得个股的现金流量表
    -------
    Return
    """
    DF=pd.DataFrame()
    url='http://money.finance.sina.com.cn/corp/go.php/vFD_CashFlow/stockid/{0}/ctrl/part/displaytype/4.phtml'.format(code)
    r=requests.get(url)
    r=r.content.decode('gbk')
    html=lxml.html.parse(StringIO(r))
    urls=html.xpath("//div[@id='con02-1']/table[1]//a/@href")
    
    for url in urls:
        r=requests.get(url)
        r=r.content.decode('gbk')
        html=BeautifulSoup(r,'lxml')
        text=html.find(id='ProfitStatementNewTable0')
        df=pd.read_html(str(text),header=0)[0]
        df.columns=df.iloc[0,:]
        df=df.drop(0,axis=0)
        df=df.set_index('报表日期')
        df=df.T
        #print(df)
        DF=DF.append(df)    

    return DF    


def FI_sina(code):
    """
    获得个股的财务指标
    ---------
    Return
    """
    DF=pd.DataFrame()
    url='http://money.finance.sina.com.cn/corp/go.php/vFD_FinancialGuideLine/stockid/{0}/displaytype/4.phtml'.format(code)
    r=requests.get(url)
    r=r.content.decode('gbk')
    html=lxml.html.parse(StringIO(r))
    urls=html.xpath("//div[@id='con02-1']/table[1]//a/@href")
    
    for url in urls:
        r=requests.get(url)
        r=r.content.decode('gbk')
        html=BeautifulSoup(r,'lxml')
        text=html.find(id='BalanceSheetNewTable0')
        df=pd.read_html(str(text),header=0)[0]
        df.columns=df.iloc[0,:]
        df=df.drop(0,axis=0)
        df=df.set_index('报告日期')
        df=df.T
        #print(df)
        DF=DF.append(df)
    return DF
    
if __name__=="__main__":
    code='600000'
    #df=financial_index_sina(code)
    #df=balance_sheet_sina(code)
    #df=income_statement_sina(code)
    df=cashflow_statement_sina(code)
