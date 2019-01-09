#!/usr/bin/env python3
# -*-coding:utf-8-*-

#from selenium import webdriver
import time,re,sys
import pandas as pd
import numpy as np
from io import StringIO
import lxml.html,requests
from bs4 import BeautifulSoup
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
#import unittest, time, re

if sys.platform=='win32':
    driver=driver=webdriver.PhantomJS()
else:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='/usr/bin/chromedriver')
"""
import webdriver.mydriver as dr
driver=dr.Firefox_hdless()
PY3 = (sys.version_info[0] >= 3)
    
def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return

def _get_info(driver):
    global dataset
    text=driver.page_source
    html=lxml.html.parse(StringIO(text))
    res=html.xpath("//table[@id='tablistph']//tr")
    

    for r in res:
        rptp=r.xpath("td[2]/text()")[0]
        title=r.xpath("td[3]/a/text()")[0]
        href=r.xpath("td[3]/a/@href")[0]
        date=r.xpath("td[4]/text()")[0]
        jg=r.xpath("td[5]/a/text()")[0]
        yjy=r.xpath("td[6]/a/text()")[0]
        dataset.append([rptp,title,href,date,jg,yjy])
    return

dataset=[]
def get_reportlistsd_qq(code):
    """
    获得研究报告的信息列表
    """

    if code[0] in ['0','2','3']:
        code='sz'+code
    elif code[0] in ['6','9']:
        code='sh'+code
    else:
        print("Input the right code, like 600000")    
        
    url='http://stockhtm.finance.qq.com/report/others/result.html#1,{0},0,0,0,0'.format(code)
    print(url)
    driver.get(url)
    waitForLoad(driver)

    
    _get_info(driver)

    while True:
        try:
            driver.find_element_by_link_text("下一页").click()
            _get_info(dirver)
        except:
            break

    df=pd.DataFrame(dataset)
    df.columns=['bglx','title','href','pubdata','institue','reserch']
    return df

def get_reseachtext_qq(code,n=5):
    """
    获得股票的研究报告
    """
    df=get_reportlistsd_qq(code)
    ddlist=list(df.iloc[:n,df.columns.get_loc('href')])
    textset=[]
    for url in ddlist:
        r=requests.get(url)
        soup=BeautifulSoup(r.content.decode('gbk'),'lxml')
        text=soup.find(id='main_content_div')
        try:
            textset.append(text.text)
        except Exception as e:
            print(e)
            pass

    #alltext='\n\n\n'.join(textset)
    return textset

    
    
if __name__=="__main__":
    #df=get_tick_aastock(sys.argv[1])
    #df=get_reportlistsd_qq(sys.argv[1])
    dd=get_reseachtext_qq(sys.argv[1],n=5)
