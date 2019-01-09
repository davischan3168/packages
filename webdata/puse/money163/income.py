#!/usr/bin/env python3
# -*-coding:utf-8-*-

import pandas as pd
import numpy as np
import sys,requests,os
import lxml.html
from lxml import etree
import json
import re,time
import datetime as dt
from webdata.util.hds import user_agent as hds
from io import StringIO
from bs4 import BeautifulSoup
import webdata.puse.money163.cons as wc


def get_income_m163(code,mytype='hy'):
    url=wc.income %(code,mytype)
    r=requests.get(url,stream=True)
    text=r.text.replace('\r\n','\n')
    #f=open('income_%s_%s.csv'%(code,mytype),'w')
    #f.write(text)
    #f.close()
    df=pd.read_csv(StringIO(text),header=None)
    return df
                

    
if __name__=="__main__":
    #df=get_mk_data('600160')
    df=income_data(sys.argv[1])
