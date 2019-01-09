#!/usr/bin/env python3
# -*-coding:utf-8-*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.support.wait import WebDriverWait
import unittest, time, re
import sys,os
import requests
from bs4 import BeautifulSoup
import lxml.html
from io import StringIO
import time
driver = webdriver.PhantomJS()

urll='http://www.sbkk88.com/mingzhu/ertong/shenshixixiaoshuo/'
base='http://www.sbkk88.com/'

r=requests.get(urll)
text=r.content.decode('gbk')

html=lxml.html.parse(StringIO(text))

lis=html.xpath('//ul[@class="leftList"]/li')
urls={}
n=0
for li in lis:
    name=li.xpath('a/text()')[0]
    href=li.xpath('a/@href')[0]
    urls[n]=[name,base+href]
    #print(n)
    n=n+1

def get_pagetext(url):
    """
    r=requests.get(url)
    text=r.content.decode('gbk')
    soup=BeautifulSoup(text,'lxml')
    text=soup.find_all('p')
    """
    print(url)
    driver.get(url)
    driver.implicitly_wait(3)
    texts=driver.find_elements_by_xpath('//div[@id="f_article"]/p')
    con=[]
    for s in texts:
        con.append(s.text)

    return '\n\n'.join(con)

for i in range(7,35,1):
    name=urls[i][0]
    uk=urls[i][1]
    text=get_pagetext(uk)
    print("Getting %s"%name)
    f=open(str(i).zfill(2)+name+'.txt','w',encoding='utf8')
    f.write(text)
    f.flush()
    time.sleep(0.3)

