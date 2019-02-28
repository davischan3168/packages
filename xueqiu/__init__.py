import os

name = "xueqiu"

__author__ = 'Yang Yu'


from xueqiu.finance import (cash_flow, indicator, balance, income, business)

from xueqiu.report import (report, earningforecast)

from xueqiu.capital import(
    margin, blocktrans, capital_assort, capital_flow, capital_history)

from xueqiu.realtime import(quotec, pankou)

from xueqiu.f10 import(skholderchg, skholder, main_indicator,
                           industry, holders, bonus, org_holding_change, 
                           industry_compare, business_analysis, shareschg, top_holders)

from xueqiu.token import (get_token,set_token)
