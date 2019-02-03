#!/usr/bin/env python3
# -*-coding:utf-8-*-
import sys
DATA_GETTING_TIPS = '[Getting data:]'
DATA_GETTING_FLAG = '#'
def _check_input(year, quarter):
    if isinstance(year, str) or year < 1989 :
        raise TypeError(DATE_CHK_MSG)
    elif quarter is None or isinstance(quarter, str) or quarter not in [1, 2, 3, 4]:
        raise TypeError(DATE_CHK_Q_MSG)
    else:
        return True
    
def _write_head():
    sys.stdout.write(DATA_GETTING_TIPS)
    sys.stdout.flush()

def _write_console():
    sys.stdout.write(DATA_GETTING_FLAG)
    sys.stdout.flush()
    
PY3 = (sys.version_info[0] >= 3)


"""http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?page=1&breed=ZN0&start=2007-08-01&end=2017-09-27&jys=shfe&pz=ZN&hy=ZN0&type=inner
http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?page=1&breed=CF0&start=2007-08-01&end=2017-09-27&jys=czce&pz=CF&hy=CF0&type=inner
http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?page=1&breed=A0&start=2007-08-01&end=2017-09-27&jys=dce&pz=A&hy=A0&type=inner
http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?page=1&breed=IC0&start=2007-08-01&end=2017-09-27&jys=cffex&pz=IC&hy=IC0&type=inner"""
"""jys:shfe上期所;cffex:中金所;dce大商所:;czce:郑商所."""

czce=['CF','CY','FG','JR','LR','MA','OI','RI','RM','RS','SF','SM','SR','TA','WH','ZC']
dce=['A','B','C','CS','FB','I','J','JD','JM','L','M','P','PP','V','Y']
shfe=['AG','AL','AU','BU','CU','FU','HC','NI','PB','RB','RU','SN','WR','ZN']
cffex=["IC",'IF','IH','T','TF']

FC_url='http://vip.stock.finance.sina.com.cn/q/view/vFutures_History.php?page={3}&breed={0}0&start={1}&end={2}&jys={4}&pz={0}&hy={0}0&type=inner'

def _tofl(x):
    try:
        if ',' in x:
            x=x.replace(',','')
            return float(x)
        else:
            return float(x)
    except:
        return x
