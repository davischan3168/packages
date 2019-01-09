#!/usr/bin/env python3
# -*-coding:utf-8-*-

"""
获取在美国NasdaQ上市股票的历史交易数据。
"""
from selenium import webdriver
import time,sys
import pandas as pd
from bs4 import BeautifulSoup
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.select import Select
"""
import webdriver.mydriver as dr
driver=dr.Firefox_hdless()
import re
from io import StringIO
"""
if sys.platform=="linux":
    driver=webdriver.Chrome('/usr/bin/chromedriver')
else:
    driver=webdriver.Chrome()
data=pd.DataFrame()
driver.set_window_size(480, 800)
"""
#driver = webdriver.PhantomJS()
#driver=webdriver.Chrome()

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


#code=input("Enter the USA listed Company code:")
#url='http://www.nasdaq.com/symbol/{0}/historical'.format(code)
def get_nasd_data(code,mdate='10y'):
    """
    date: 5d-5Days,1m-1Month,3m-3Month,6m-6Month
          1y-1Year,18m-18Month,2y-2 Years,3y-3 Years
          4y,5y,6y,7y,8y,9,10y.
    """
    url='http://www.nasdaq.com/symbol/{}/historical'.format(code)
    driver.get(url)
    waitForLoad(driver)
    #"""
    sel = driver.find_element_by_xpath("//select[@id='ddlTimeFrame']")
    Select(sel).select_by_value(mdate)
    #"""
    #driver.find_element_by_xpath("//select[@id='ddlTimeFrame']/option[value='5y']").click()
    soup=BeautifulSoup(driver.page_source,'lxml')
    table=soup.find_all('table')
    data=table[5]
    df=pd.read_html(str(data))[0]
    df.columns=['Date','Open','High','Low','Close/Last','Volume']
    return df


if __name__=="__main__":
    df=get_nasd_data('sina')
