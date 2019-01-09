#!/usr/bin/env python3
# -*-coding:utf-8-*-
import time,random,requests,json,re
import pandas as pd
import datetime as dt
from io import StringIO
#import webdata as wd
import webdata.puse.eastmpy.cont as wt

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from lxml import etree

today=dt.datetime.today()
today=today.strftime('%Y%m%d')

radar_type={1:'09000945',2:'09451000',3:'10001015',4:'10151030',5:'10301045',6:'10451100',7:'11001115',8:'11151130',9:'13001315',10:'13151330',11:'13301345',12:'13301345',13:'14001415',14:'14151430',15:'14301445',16:'14451515'}



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

class EMSource(object):
    def __init__(self,browser=0,use_cookie=0):
        self.browser=browser
        self.use_cookiex=use_cookie
        #self.__code=code
        #self.bs_url='http://data.eastmoney.com/stockdata/{0}.html'.format(code)
        self.bk=pd.read_pickle('output/eastmsource/bk.pkl')
        if self.use_cookiex==0:
            dcap = dict(DesiredCapabilities.PHANTOMJS)
            dcap["phantomjs.page.settings.userAgent"] = ('Mozilla/5.0(WindowsNT6.1;WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/59.0.3071.115Safari/537.36x-requested-with:XMLHttpRequest')
            dcap["phantomjs.page.settings.loadImages"] = True
            
            if self.browser==0:
                self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
            if self.browser==1:
                self.driver=webdriver.Chrome()
            if self.browser==2:
                self.driver=webdriver.Firefox()
                
    def cashfl_concept_hist(self,bkname):
        
        """核心题材
        """
        idd=self.bk[self.bk['name']==bkname]['id'].tolist()[0]
        #print(idd)
        url='http://data.eastmoney.com/bkzj/{0}.html'.format(idd)
        self.driver.get(url)
        waitForLoad(self.driver)
        self.driver.find_element_by_xpath('//ul[@id="s1-tab"]/li[2]').click()
        text=self.driver.find_element_by_xpath('//table[@id="tb_lishi"]').text
        text=text.replace(' ',',')
        text=text.split('\n')
        dataset=[]
        for i in text[2:]:
            dataset.append(i)
        df=pd.read_csv(StringIO('\n'.join(dataset)),header=None)
        df=df.applymap(lambda x:wt._tofl(x))
        #df=df.applymap(lambda x:wt._tofl(x))
        return df
        
if __name__=="__main__":
    qa=EMSource()
    

