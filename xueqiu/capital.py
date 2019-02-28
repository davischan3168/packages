import json
import os
from xueqiu import cons
from xueqiu import api_ref
from xueqiu import utls
from xueqiu.cons import _code

def margin(symbol, page=1, size=180):
    symbol=_code(symbol)
    url = api_ref.capital_margin_url+symbol
    #print(url)
    url = url + '&page='+str(page)
    url = url + '&size='+str(size)
    return utls.fetch(url)


def blocktrans(symbol, page=1, size=30):
    symbol=_code(symbol)
    url = api_ref.capital_blocktrans_url+symbol
    url = url + '&page='+str(page)
    url = url + '&size='+str(size)
    return utls.fetch(url)


def capital_assort(symbol):
    symbol=_code(symbol)
    url = api_ref.capital_assort_url+symbol
    return utls.fetch(url)


def capital_flow(symbol):
    symbol=_code(symbol)
    url = api_ref.capital_flow_url+symbol
    return utls.fetch(url)


def capital_history(symbol, count=20):
    symbol=_code(symbol)
    url = api_ref.capital_history_url+symbol
    url = url + '&count='+str(count)
    return utls.fetch(url)
