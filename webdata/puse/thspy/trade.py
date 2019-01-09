#!/usr/bin/env python3
# -*-coding:utf-8-*-
"""
获得公司的基本信息和财务信息
"""
import requests,json
from io import StringIO
import re,sys,os
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import lxml.html
from lxml import etree
import time
import datetime as dt
import webdata.puse.thspy.cont as wt
from webdata.util.hds import user_agent as hds

def get_realtime_ths(tick):
    """
    获取某家上市公司的当前交易数据
    -------------------------------
    return ：
        DataFrame
    """
    url=wt.curr_last.format(tick)
    r=requests.get(url,headers=hds())

    text=r.text.split("last(")[1].replace('}})','}}')
    data=json.loads(text)    
    df=pd.DataFrame(data)

    name=['10', '13', '134152', '1378761', '14', '15', '17', '1771976',
       '19', '1968584', '199112', '2034120', '223', '224', '225', '226',
       '237', '238', '24', '25','259', '260', '264648',
       '30', '31', '3475914', '3541450',
       '395720', '402', '407', '461256', '49',
       '526792', '527198', '592920', '6', '69', '7', '70', '8', '9',
       'name','time']
    df=df.T
    df=df[name]
    df.rename(columns={'10':'close','13':'volume','19':'amount','134152':'PE','2034120':'PE_TTM','592920':'PB','6':'pre_close','69':'up_ceil','7':'open','70':'down_ceil','8':'high','9':'low','526792':'ZF','264648':'chg','199112':'chg%','3541450':'T.Value','402':'T.Share','407':'Cur.Share','1968584':'turnover','237':'Sm_in','238':'Sm_out','259':'M_in','260':'M_out','14':'buy_all','15':'Sell_all'},inplace=True)
    return df

def get_k_data_year_THS(code,year,if_fq='01'):
    # 00 不复权 01前复权 02后复权
    data_=[]


    url='http://d.10jqka.com.cn/v2/line/hs_%s/%s/%s.js'%(str(code),str(if_fq),str(year))
    #print(url)
    for item in requests.get(url,headers=hds()).text.split('\"')[3].split(';'):
        data_.append(item.split(','))

    df =pd.DataFrame(data_,index=list(np.asarray(data_).T[0]),columns=['date','open','high','low','close','volume','amount','factor'])
    df=df.applymap(lambda x:wt._tofl(x))
    df.index.name='date'
    del df['date']
    #df=df.sort_index()
    return df

def get_kdata_THS(code,start,end=time.localtime().tm_year,if_fq='01'):
    """start表示开始年度，end表示结束年度"""
    # 00 不复权 01前复权 02后复权
    df=pd.DataFrame()
    for y in range(start,end+1):
        try:
            df=df.append(get_k_data_year_THS(code,year=y,if_fq=if_fq))
        except Exception as e:
            print(e,"; Can't get data for %s"%y)
            pass

    df=df.sort_index()
    return df
    

if __name__=="__main__":
    #tick='600531'
    #dd=get_realtime_ths(sys.argv[1])
    df=get_kdata_THS('600531',2001,2017,'00')
