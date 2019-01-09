#!/usr/bin/env python3
# -*-coding:utf-8-*-

from selenium import webdriver
import time,re,sys
import pandas as pd
import numpy as np
from io import StringIO
import lxml.html,requests
from bs4 import BeautifulSoup
import urllib.parse

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def Firefox_hdless():
    options = webdriver.FirefoxOptions()
    options.add_argument('-headless')
    profile = webdriver.FirefoxProfile()
    profile.set_preference('permissions.default.image', 2)
    profile.set_preference('dom.ipc.plugins.enabled.npswf32.dll', 'false')
    profile.set_preference('javascript.enabled', 'false')
    browser = webdriver.Firefox(options=options,firefox_profile = profile)
    return browser
"""
def Phantomjs():
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = ('Mozilla/5.0(WindowsNT6.1;WOW64) AppleWebKit/537.36(KHTML, likeGecko) Chrome/59.0.3071.115Safari/537.36x-requested-with:XMLHttpRequest')
    dcap["phantomjs.page.settings.loadImages"] = True    
    driver=webdriver.PhantomJS(desired_capabilities=dcap)
    return driver
"""
def Chrome_hdless():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options,executable_path='/usr/bin/chromedriver')    
    return driver

def get_cookies(url):
    parsed_url = urllib.parse.urlparse(url)
    if parsed_url.scheme:
        domain = parsed_url.netloc
    else:
        raise urllib.error.URLError("You must include a scheme with your URL.")
       
    driver.get(url)
    driver.implicitly_wait(5)
    sl=driver.get_cookies()
    cookies={}
    for dn in sl:
        cookies[dn['name']]=dn['value']
    #print(cookies)
    #driver.quit()
    return cookies

if __name__=="__main__":
    #cook=get_cookies(sys.argv[1])
    if sys.platform=='win32':
        driver=Firefox_hdless()
    else:
        driver=Chrome_hdless()
    #pass
