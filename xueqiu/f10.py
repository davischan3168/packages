import json
import os
import sys
from xueqiu import cons
from xueqiu import api_ref
from xueqiu import utls
from xueqiu.cons import _code

def skholderchg(symbol):
    symbol=_code(symbol)
    url = api_ref.f10_skholderchg+symbol
    return utls.fetch(url)


def skholder(symbol):
    symbol=_code(symbol)
    url = api_ref.f10_skholder+symbol
    return utls.fetch(url)


def industry(symbol):
    symbol=_code(symbol)
    url = api_ref.f10_industry+symbol
    return utls.fetch(url)


def holders(symbol):
    symbol=_code(symbol)
    url = api_ref.f10_holders+symbol
    return utls.fetch(url)


def bonus(symbol,page=1,size=10):
    url = api_ref.f10_bonus+symbol
    url = url + '&page='+str(page)
    url = url + '&size='+str(size)
    return utls.fetch(url)


def org_holding_change(symbol):
    symbol=_code(symbol)
    url = api_ref.f10_org_holding_change+symbol
    return utls.fetch(url)


def industry_compare(symbol):
    symbol=_code(symbol)
    url = api_ref.f10_industry_compare+symbol
    return utls.fetch(url)


def business_analysis(symbol):
    symbol=_code(symbol)
    url = api_ref.f10_business_analysis+symbol
    return utls.fetch(url)


def shareschg(symbol, count=5):
    symbol=_code(symbol)
    url = api_ref.f10_shareschg+symbol
    url = url + '&count='+str(count)
    return utls.fetch(url)


def top_holders(symbol, circula=1):
    symbol=_code(symbol)
    url = api_ref.f10_top_holders+symbol
    url = url + '&circula='+str(circula)
    return utls.fetch(url)


def main_indicator(symbol):
    symbol=_code(symbol)
    url = api_ref.f10_indicator+symbol
    print(url)
    #return utls.fetch(url)
    return utls.fetch_without_token(url)
if __name__=="__main__":
    main_indicator(sys.argv[1])
