#!/usr/bin/env python3
# -*-coding:utf-8-*-

import datetime as dt
import sys
import numpy as np

PY3 = (sys.version_info[0] >= 3)

fin_hk={    'ins':'http://web.ifzq.gtimg.cn/appstock/hk/HkInfo/getFinReport?type=3&reporttime_type=-1&code={0}&startyear={1}&endyear={2}&_callback=',\
            'cfl':'http://web.ifzq.gtimg.cn/appstock/hk/HkInfo/getFinReport?type=2&reporttime_type=-1&code={0}&startyear={1}&endyear={2}&_callback=',\
            'bs' :'http://web.ifzq.gtimg.cn/appstock/hk/HkInfo/getFinReport?type=1&reporttime_type=-1&code={0}&startyear={1}&endyear={2}&_callback='}
#0位股票代码，1为开始年，2位结束年

named={"ylnl":['Cost.Profit.R','Net.oper.R','Profit_d','ROE','Three.Cost','Profit.R','Gross.Margin.R','Profit.bTax','Profit.R.bTax','O.Profit.Rate','ROA'],"mgzb":['EPS','W.EPS','W.EPS.D','Net.A.PS','CF_PS','Rev.PS','EPS.Dilute','EPS.Dilute.D','Net.A.PS.Adj','D.EPS'],"yynl":['Invt.Asset.R','Invt.turnover.R','Invt_turnover_day','Shareholder_turnover.R','Fixed_turnover.R','Curr_Asset_turnover.R','Curr_Asset_turnover_day','Receivable_turnover.R','Receivable_turnover_day','Asset_turnover.R','Asset_turnover_day'],"djcw":['ROE','ROE.D','EPS.DD','EPS.D','Rev.PS','ROA.bTax','Rev.NetProfit.R','Rev.Gr.Profit.R','Profit.bTax','Profit.bTax.R','ROA'],"czzb":['Debt.Equit.R','L.Debt.Work.Capital.R','Fix.Asset.R','Net.Asset.R','Curr.R','Liquidation.R','Quick.R','Cash.R','Capital.fixed.R','Capitalization_R','Assets.Debt.R','Asset'],'cznl':['Net.profit_yoy','T.profit_yoy','Rev.PS_yoy','CF_PS_yoy','Profit.bTax_yoy','Rev.Profit_yoy','Rev_yoy','Asset_yoy']}

inst_hk='http://web.ifzq.gtimg.cn/appstock/hk/HkInfo/getRightsMainHold?p={1}&c={0}&max=500&o=0&_callback='
#0为股票代码，1位页数
news_hk='http://web.ifzq.gtimg.cn/appstock/news/info/search?_appver=1.0&page={1}&symbol={0}&n=101&_var=finance_news&type=2&_=1499303957874'

notice_hk='http://web.ifzq.gtimg.cn/appstock/news/info/search?page={1}&symbol={0}&n=101&_var=finance_notice&type=0&_appver=1.0&_=1499303957903'

dividen_hk='http://web.ifzq.gtimg.cn/appstock/hk/HkInfo/getDividends?p={1}&c={0}&max=100&_callback='

forcast_a='http://stock.finance.qq.com/corp1/yjyg.php?zqdm={0}'
cwfx_a='http://stock.finance.qq.com/corp1/cwfx.html?ylnl-sz300113'
Right_issue_url='http://web.ifzq.gtimg.cn/appstock/hk/HkInfo/getRightsDirector?p=1&c={0}&max=3000000&_callback='

url_cashfl_industry={1:'http://stock.gtimg.cn/data/view/flow.php?t=2',2:'http://stock.gtimg.cn/data/view/flow.php?t=4',3:'http://stock.gtimg.cn/data/view/flow.php?t=5',4:'http://stock.gtimg.cn/data/view/flow.php?t=7&d=1',5:'http://stock.gtimg.cn/data/view/flow.php?t=8&d=1',6:'http://stock.gtimg.cn/data/view/flow.php?t=9&d=1'}

def _i2t(x):
    d1=str(x)
    d1=dt.datetime.strptime(d1,'%H%M%S')
    return d1.strftime("%H:%M:%S")

def _tofl(x):
    try:
        if ',' in x:
            x=x.replace(',','')
            return float(x)
        else:
            return float(x)
    except:
        return x

def _set_code(code):
    if len(code)==5:
        code='hk'+code
        return code
    elif len(code)==6:
        if code[0] in ['2','0','3']:
            code='sz'+code
            return code
        else:
            return 'sh'+code
