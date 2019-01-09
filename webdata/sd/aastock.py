#!/usr/bin/env python3
# -*-coding:utf-8-*-

#from selenium import webdriver
import time,re,sys
import pandas as pd
import numpy as np
from io import StringIO
import datetime
import webdriver.mydriver as dr
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.expected_conditions import visibility_of
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#import unittest, time, re
"""
"""
if sys.platform=='win32':
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] =('Mozilla/5.0(WindowsNT6.1;WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/59.0.3071.115Safari/537.36x-requested-with:XMLHttpRequest')
    dcap["phantomjs.page.settings.loadImages"] = True
    driver=webdriver.PhantomJS(desired_capabilities=dcap)
else:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='/usr/bin/chromedriver')
"""
driver=dr.Firefox_hdless()
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

def HK_tick_aastock(code):
    """
    香港股票为5位数的代码
    """
    df=pd.DataFrame()
    #url='http://www.aastocks.com/sc/stocks/analysis/transaction.aspx?symbol={0}'.format(code)
    url='http://www.aastocks.com/en/stocks/analysis/transaction.aspx?symbol={0}'.format(code)
    print(url)
    driver.get(url)
    waitForLoad(driver)
    driver.find_element_by_xpath('//div[@id="divChartOption"]//input[@value="2"]').click()
    dfd=driver.find_elements_by_xpath('//table[starts-with(@id,"tradeLog")]')
    tik=1
    for i in dfd:
        print(i.text)
        try:
            df=df.append(pd.read_csv(StringIO(i.text),sep=' ',header=0))
            print(df)
        except:
            pass
    while True:
        try:
            driver.find_element_by_xpath("//div[@id='tsNext']").click()
            waitForLoad(driver)
            dfd=driver.find_elements_by_xpath('//table[starts-with(@id,"tradeLog")]')
            for i in dfd:
                print(i.text)
                try:
                    df=df.append(pd.read_csv(StringIO(i.text),sep=' ',header=0))
                    print(df)
                except:
                    pass
            tick=tick+1
            if tick >20:
                break
        except:
            break
    return df

def HK_tick_AAST(code,upl=100):
    """
    香港股票为5位数的代码
    """
    df=pd.DataFrame()
    #url='http://www.aastocks.com/sc/stocks/analysis/transaction.aspx?symbol={0}'.format(code)
    url='http://www.aastocks.com/en/stocks/analysis/transaction.aspx?symbol={0}'.format(code)
    print(url)
    driver.get(url)
    waitForLoad(driver)
    driver.find_element_by_xpath("//input[@value=2]").click()
    for n in range(upl):
        try:
            print('Getting page',n)
            dfd=driver.find_elements_by_xpath('//table[starts-with(@id,"tradeLog")]')
            for i in dfd:
                try:
                    df=df.append(pd.read_csv(StringIO(i.text),sep=' '))
                    #print(df)
                except Exception as e:
                    print(e)
                    pass
            driver.find_element_by_xpath("//div[@id='tsNext']").click()
        except Exception as e:
            print(e)
            break
    try:
        print(df.head())
        df=df.drop_duplicates()
        df=df.drop('Turnover',axis=1)
        df.columns=['Volume','Price','Turnover','Type']
        #df=df.set_index('时间')
        #df=df.set_index('Time')
    except:
        pass
    
    return df

def HK_tick_AAST(code,upl=100):
    """
    香港股票为5位数的代码
    """
    df=pd.DataFrame()
    #url='http://www.aastocks.com/sc/stocks/analysis/transaction.aspx?symbol={0}'.format(code)
    url='http://www.aastocks.com/en/stocks/analysis/transaction.aspx?symbol={0}'.format(code)
    #print(url)
    
    start=datetime.datetime.now()
    driver.get(url)
    driver.implicitly_wait(3)
    #waitForLoad(driver)
    driver.find_element_by_xpath('//div[@id="divChartOption"]//input[@value="2"]').click()
    #driver.find_element_by_xpath("//input[@value=2]").click()
    
    for i in range(upl):
        dfd=driver.find_elements_by_xpath('//table[starts-with(@id,"tradeLog")]')
        for t in dfd:
            try:
                df=df.append(pd.read_csv(StringIO(t.text),sep=' '))
            except:
                break
        """
        Tag=driver.find_element_by_id('tsNext')
        if visibility_of(Tag):
            Tag.click()
        else:
            break
        """
        try:
            driver.find_element_by_id('tsNext').click()
        except:
            print('Getting %s'%i)
            break#"""

    #df.Type=df.Turnover +' ' +df.Type
    df=df.drop('Turnover',axis=1)
    df.columns=['Volume','Price','Turnover','Type']
    df.index.name='Time'
    df=df.drop_duplicates(keep='first')
    print('Use time %s seconds'%(datetime.datetime.now()-start).seconds)
    return df

        
            
"""
    
    for n in range(upl):
        try:
            print('Getting page',n)
            dfd=driver.find_elements_by_xpath('//table[starts-with(@id,"tradeLog")]')
            for i in dfd:
                try:
                    df=df.append(pd.read_csv(StringIO(i.text),sep=' '))
                    #print(df)
                except Exception as e:
                    print(e)
                    pass
            driver.find_element_by_xpath("//div[@id='tsNext']").click()
        except Exception as e:
            print(e)
            break
    try:
        print(df.head())
        df=df.drop_duplicates()
        df=df.drop('Turnover',axis=1)
        df.columns=['Volume','Price','Turnover','Type']
        #df=df.set_index('时间')
        #df=df.set_index('Time')
    except:
        pass
    
    return df
"""

if __name__=="__main__":
    #df=get_tick_aastock(sys.argv[1])
    df=HK_tick_AAST(sys.argv[1],50)
