import json
import os
from xueqiu import cons
from xueqiu import api_ref
from xueqiu import utls
from xueqiu.cons import _code

def quotec(symbols):
    symbols=_code(symbols)
    url = api_ref.realtime_quote+symbols
    return utls.fetch_without_token(url)


def pankou(symbol):
    symbol=_code(symbol)
    url = api_ref.realtime_pankou+symbol
    return utls.fetch_without_token(url)

