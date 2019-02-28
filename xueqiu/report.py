import json
import os
from xueqiu import cons
from xueqiu import api_ref
from xueqiu import utls
from xueqiu.cons import _code

def report(symbol):
    symbol=_code(symbol)
    url = api_ref.report_latest_url+symbol
    return utls.fetch(url)


def earningforecast(symbol):
    symbol=_code(symbol)
    url = api_ref.report_earningforecast_url+symbol
    return utls.fetch(url)
