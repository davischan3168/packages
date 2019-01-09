#!/usr/bin/env python3
# -*-coding:utf-8-*-
import numpy as np
import pandas as pd
import quandl
token="ALM9oCUNixBCkHwyxJHF"

def quandld(code,authtoken=token, start='1990-01-01',end=None):
    """
    参数说明：
    code:代码， 构成主要有数据库加代码，如
          YAHOO/SS_600036,YAHOO/SZ_000002,YAHOO/HK_0005
    start:开始时间
    end：  截止时间
    """
    if end is None:
        import time
        end=time.strftime("%Y-%m-%d")
    try:
        df=quandl.get(code,authtoken=token, trim_start=start,trim_end=end)
        return df
    except Exception as e:
        print(e)

def quandlyd(code,authtoken=token, start='1990-01-01',end=None):
    """
    本函数主要是获取上海、深圳和香港联交所的股票数据
    参数说明：
    code:代码， 为上海、深圳和联交所的股票代码，前两个交所的代码为6位，联交所的
    为4位，如YAHOO/SS_600036,YAHOO/SZ_000002,YAHOO/HK_0005
    start:开始时间
    end：  截止时间
    """
    if end is None:
        import time
        end=time.strftime("%Y-%m-%d")
    if len(code)==6:
        if code[0] in ['6','9']:
            code='YAHOO/SS_'+code
            df=quandl.get(code,authtoken=token, trim_start=start,trim_end=end)
            return df
        elif code[0] in ['0','3','2']:
            code='YAHOO/SZ_'+code
            df=quandl.get(code,authtoken=token, trim_start=start,trim_end=end)
            return df
        else:
            print(u"代码输入错误，不是上海和深圳交所的股票代码")
    elif len(code)==4:
        code='YAHOO/HK_'+code
        df=quandl.get(code,authtoken=token, trim_start=start,trim_end=end)
        return df
    else:
        print(u'code 为6位或4位的数字符号')
        
    

if __name__=="__main__":
    df=quandlyd('600036')
