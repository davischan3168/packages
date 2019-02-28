import json
import os
from xueqiu import cons
from xueqiu import api_ref
from xueqiu import utls
from xueqiu.cons import _code



def cash_flow(symbol, is_annals=0, count=10):
    symbol=_code(symbol)
    url = api_ref.finance_cash_flow_url+symbol
    
    if is_annals == 1:
        url = url + '&type=Q4'
    
    url = url + '&count='+str(count)

    return utls.fetch(url)


def indicator(symbol, is_annals=0, count=10):
    symbol=_code(symbol)
    url = api_ref.finance_indicator_url+symbol
    
    if is_annals == 1:
        url = url + '&type=Q4'
    
    url = url + '&count='+str(count)

    return utls.fetch(url)


def balance(symbol, is_annals=0, count=10):
    symbol=_code(symbol)
    url = api_ref.finance_balance_url+symbol

    if is_annals == 1:
        url = url + '&type=Q4'

    url = url + '&count='+str(count)

    return utls.fetch(url)


def income(symbol, is_annals=0, count=10):
    symbol=_code(symbol)
    url = api_ref.finance_income_url+symbol

    if is_annals == 1:
        url = url + '&type=Q4'

    url = url + '&count='+str(count)

    return utls.fetch(url)


def business(symbol, is_annals=0, count=10):
    symbol=_code(symbol)
    url = api_ref.finance_business_url+symbol

    if is_annals == 1:
        url = url + '&type=Q4'

    url = url + '&count='+str(count)

    return utls.fetch(url)
 
if __name__=="__main__":
    df=balance('SH600685')
