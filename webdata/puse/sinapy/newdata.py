#!/usr/bin/env python3
# -*-coding:utf-8-*-

import sys,requests
import os
from urllib.parse import quote
import lxml.html
from io import StringIO
import time
import json
import pandas as pd
import numpy as np
import pickle
from webdata.util.hds import user_agent as hds
import webdata.puse.eastmpy.cont as wt

def get_pepb_Sina():
    dff=pd.DataFrame()
    url='http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[[%22hq%22,%22hs_a%22,%22%22,0,1,500]]&callback=FDC_DC.theTableData'
    r=requests.get(url,headers=hds())
    text=r.text.split('theTableData(')[1]
    text=text.replace(')\n','')

    d=json.loads(text)
    df=pd.DataFrame(d[0]['items'])
    df.columns=d[0]['fields']
    dff=dff.append(df)

    pageNo=2
    while True:
        url='http://money.finance.sina.com.cn/d/api/openapi_proxy.php/?__s=[[%22hq%22,%22hs_a%22,%22%22,0,{0},500]]&callback=FDC_DC.theTableData'.format(pageNo)
        #print(url)
        r=requests.get(url,headers=hds())
        text=r.text.split('theTableData(')[1]
        text=text.replace(')\n','')

        d=json.loads(text)
        if len(d[0]['items'])<1:
            print('Exit ....')
            break        
        df=pd.DataFrame(d[0]['items'])
        df.columns=d[0]['fields']
        dff=dff.append(df)
        pageNo = pageNo + 1

    dff['date']=d[0]['day']
    dff=dff.drop(["symbol","favor","guba"],axis=1)
    dff=dff.set_index('code')
    return dff
if __name__=="__main__":
    df=get_pepb_Sina()
