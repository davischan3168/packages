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
#resource:http://xinsanban.eastmoney.com/DataCenter/Distribution/Bonus

def basic_data_new3lsit_EM(year,mtype='年报'):
    """
    获取在新三板挂牌公司的基本数据情况：
    ----------------------------------
    year：年份
    mtype：年报或中报
    """
    df=pd.DataFrame()
    url='http://xinsanban.eastmoney.com/api/DataCenter/YJBG/GetYJSL?baogaoqi={0}&reporttype={1}&page=1&pagesize=1000&sortType=NOTICEDATE&sortRule=-1'.format(year,quote(mtype))#mtype :年报、中标
    r=requests.get(url,headers=hds())
    data=json.loads(r.text)
    TpageNo=json.loads(r.text)['TotalPage']
    df=df.append(pd.DataFrame(json.loads(r.text)['result']))

    if TpageNo>1:
        for pageNo in range(2,int(TpageNo)+1):
            url='http://xinsanban.eastmoney.com/api/DataCenter/YJBG/GetYJSL?baogaoqi={0}&reporttype={1}&page={2}&pagesize=1000&sortType=NOTICEDATE&sortRule=-1'.format(year,quote(mtype),pageNo)
            r=requests.get(url,headers=hds())
            data=json.loads(r.text)
            df=df.append(pd.DataFrame(json.loads(r.text)['result']))
    df=df.set_index('MSECUCODE')
    return df
            
if __name__=="__main__":
    df=basic_data_new3lsit_EM(2016)
