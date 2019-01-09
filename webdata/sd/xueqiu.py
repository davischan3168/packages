# -*- coding: utf-8 -*-
from selenium import webdriver
import time,re,sys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

if sys.platform=='win32':
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ('Mozilla/5.0(WindowsNT6.1;WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/59.0.3071.115Safari/537.36x-requested-with:XMLHttpRequest')
    dcap["phantomjs.page.settings.loadImages"] = True    
    driver=webdriver.PhantomJS(desired_capabilities=dcap)
else:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='/usr/bin/chromedriver')


def waitForLoad(driver):
    elem = driver.find_element_by_tag_name("html")
    count = 0
    while True:
        count += 1
        if count > 20:
            #print("Timing out after 10 seconds and returning")
            return
        time.sleep(.5)
        try:
            elem == driver.find_element_by_tag_name("html")
        except StaleElementReferenceException:
            return

def _set_code(code):
    if len(code) == 6:
        if code[0] in ['2','0','3']:
            code='SZ'+code
            return code
        elif code[0] in ['6','9']:
            code='SH'+code
            return code
    else:
        return code

def _wf(path,content,mode='a'):
    f=open(path,mode)
    f.write(content)
    f.flush()
    return

class Xueqiu(object):
    def __init__(self,name="chenzuliang@163.com",pwd="chen&801019",\
                 base_url="https://xueqiu.com"):
        self.__name = name
        self.__pwd = pwd
        self.__url = base_url
        self.__driver = None
        self.__code = None

    def logon(self):
        driver.get(self.__url)
        waitForLoad(driver)
        driver.find_element_by_xpath('//div[@class="nav__login__btn"]/span').click()
        usename=driver.find_element_by_xpath('//input[@name="username"]')
        usename.clear()
        usename.send_keys(self.__name)
        password = driver.find_element_by_xpath('//input[@type="password"]')
        password.clear()
        password.send_keys(self.__pwd)
        driver.find_element_by_css_selector("div.modal__login__btn").click()
        waitForLoad(driver)
        self.__driver=driver
        print("Logon sucess....!")

    def getdriver(self):
        return self.__driver

    def code(self,code):
        code=_set_code(code)
        self.__code=code

    def lncode(self):    
        if self.__driver.find_element_by_id("nav-account-name").text != 'DavisChan':
            self.logon()
        url='https://xueqiu.com/S/{}'.format(self.__code)
        self.__driver.get(url)
        waitForLoad(self.__driver)
        self.__ = driver

    def price(self):
        if self.__driver.current_url.split("/")[-1] != self.__code:
            self.lncode()
        d=self.__driver.find_element_by_xpath('//table[@class="topTable"]').text.split()
        x=x=[i.split('：')[1] for i in d]

    def text(self,n=1,path=None):
        if self.__driver.current_url.split("/")[-1] != self.__code:
            lncode()
            
        d={1:'//div[@stockNews]/ul[1]/li[1]/a',
           2:'//div[@stockNews]/ul[1]/li[2]/a',
           3:'//div[@stockNews]/ul[1]/li[3]/a',
           4:'//div[@stockNews]/ul[1]/li[4]/a',
           5:'//div[@stockNews]/ul[1]/li[5]/a',
           6:'//div[@stockNews]/ul[1]/li[6]/a',
           7:'//div[@stockNews]/ul[1]/li[7]/a'}
    
        try:
            self.__driver.find_element_by_xpath(d[n]).click()
        except:
            pass

        _get_text(self.__driver,self.__code,path,n)

        pageno=1
        while True:
        
            try:
                self.__driver.find_element_by_xpath("//li[@class='next']/a").click()
                waitForLoad(self.__driver)
                print("Getting Page %s"%pageno)
                pageno +=1
                _get_text(self.__driver,self.__code,path,n)
            except:
                break        
        


    

def xueqiu(code,path=None,price=True,textv=False,n=1):
    """
    code:股票代码,
    n:对应雪球下方的讨论等文本的获取
    """
    driver.get("https://xueqiu.com")
    waitForLoad(driver)
    #driver.find_element_by_css_selector("div.nav__login__btn >span").click()
    driver.find_element_by_xpath('//div[@class="nav__login__btn"]/span').click()
    usename=driver.find_element_by_xpath('//input[@name="username"]')
    usename.clear()
    usename.send_keys("chenzuliang@163.com")
    password = driver.find_element_by_xpath('//input[@type="password"]')
    password.clear()
    password.send_keys("chen&801019")
    driver.find_element_by_css_selector("div.modal__login__btn").click()
    waitForLoad(driver)
    print('logon sucess')

    code=_set_code(code)
    url='https://xueqiu.com/S/{}'.format(code)
    #print(url)
    driver.get(url)
    waitForLoad(driver)
    print(driver.current_url)

    if price:
        #driver.current_url.split("/")[-1] != self.__code:
        d=driver.find_element_by_xpath('//table[@class="topTable"]').text.split()
        x=[i.split('：')[1] for i in d]
        print(d)

    d={1:'//div[@stockNews]/ul[1]/li[1]/a',
       2:'//div[@stockNews]/ul[1]/li[2]/a',
       3:'//div[@stockNews]/ul[1]/li[3]/a',
       4:'//div[@stockNews]/ul[1]/li[4]/a',
       5:'//div[@stockNews]/ul[1]/li[5]/a',
       6:'//div[@stockNews]/ul[1]/li[6]/a',
       7:'//div[@stockNews]/ul[1]/li[7]/a'}

    if textv:
        try:
            driver.find_element_by_xpath(d[n]).click()
        except:
            pass

        _get_text(driver,code,path,n)

        pageno=1
        while True:
        
            try:
                driver.find_element_by_xpath("//li[@class='next']/a").click()
                waitForLoad(driver)
                print("Getting Page %s"%pageno)
                pageno +=1
                _get_text(driver,code,path,n)
            except:
                break
    return

def _get_text(driver,code,path,n):
    ex=driver.find_elements_by_xpath('//div[@id="statusList"]/ul/li//span[@class="show-all"]/i')
    for e in ex:
        try:
            e.click()
        except Exception as e:
            pass

    ex=driver.find_elements_by_xpath('//div[@id="statusList"]/ul/li//span[@class="show-retweet"]/i')
    for e in ex:
        try:
            e.click()
        except Exception as e:
            #print(e)
            pass
    if path is None:
        path='./txt/'+code+'%s_.txt'%n
    fs=driver.find_elements_by_xpath('//div[@id="statusList"]/ul/li')
    for l in fs:
        text=l.text+'\n'+'----'*30+'\n'
        _wf(path,text)
    return
    

if __name__ == "__main__":
    #XueQiu
    xueqiu('600497')
    pass
