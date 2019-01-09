# -*- coding:utf-8 -*- 
import pandas as pd
import numpy as np
import sys,requests,os
import lxml.html
from lxml import etree
import json
import re,time
from webdata.util.hds import user_agent as hds
try:
    from io import StringIO
except:
    from pandas.compat import StringIO
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
#reload(sys)
#sys.setdefaultencoding('utf-8')
DATE_CHK_MSG = '年度输入错误：请输入1989年以后的年份数字，格式：YYYY'
DATE_CHK_Q_MSG = '季度输入错误：请输入1、2、3或4数字'
REPORT_COLS=['code','name','preclose','open','close','high','low','Volumn','Change','p_ch','time']
REPORT_COLS1=['N1','mark','name','pchg','main_buy','main_pnt','sb_buy','sb_pnt','b_buy','b_pnt','m_buy','m_pnt','sm_buy','sm_pnt','name','code']
SH_COLS=['N1','code','name','close','pchg','zl_netinamount','zl_netratio','sb_netinamount','sb_netratio','b_netinamont','b_netratio','m_netinamount','m_netratio','sm_netinamount','sm_netratio','date']
REPORT_usa1=['code','name','preclose','open','close','high','low','volumn','chg','chg_p','amplitude','N1','N2','N3','N4','N5','N6','N7','time','total_shares','markcap']
REPORT_usa2=['preclose','open','close','high','low','volumn','chg','N1','N2','N4','N6','total_shares','markcap']
REPORT_index1=['code','name','preclose','open','close','high','low','chg','chg_p','amplitude','time']
REPORT_index2=['preclose','open','close','high','low','chg','chg_p','amplitude']
TRD_COLS=['symbol','name','trade_hk','pch_hk','code','trade_a','pch_a','Bijia_h/a','Exchange','premium_h/a']
REPORT_hgt=['date','N_O','Buy','Sell','B_S','Day_balance','T_balance','Name','p_change','code','index','index_pchg']
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



def comp2indu(code):
    """
    获取该只股票与行业平均的比较，以明白所选股票在行业中地位
    Parameter:
         code: string like 600422
    Return:
    -------------------
         DataFrame:
             Item:
             T_V:总资产
             N_A：净资产
             N_P：净利润
             PE：市盈率
             PB：市净率
             Gross：毛利率
             N_PR：净利率
             ROE：净资产收益率
         
    """
    if code[0]=='6' or code=='9':
        code='sh'+code
    else:
        code='sz'+code
    url='http://quote.eastmoney.com/%s.html'%code
    r=requests.get(url=url)
    u=r.content.decode('GBK')
    html=lxml.html.parse(StringIO(u))
    res = html.xpath("//div[@class=\"cwzb\"]/table/tbody/tr")
    if PY3:
        sarr = [etree.tostring(node).decode('gb18030') for node in res]
    else:
        sarr = [etree.tostring(node) for node in res]
    sarr = ''.join(sarr)
    sarr = '<table>%s</table>'%sarr
    df = pd.read_html(sarr)[0]
    df=df.drop(3)
    names=['Item','Market.Cap','Net.Asset','Net.Profit','PE','PB','G.Profit.rate','Net.Profit.rate','ROE']
    df.columns=names
    df.iloc[2,2:]=df.iloc[2,2:].map(lambda x:x.split('|')[0])
    df.iloc[1,0]='行业平均'
    return df

def dividen(date='2016-12-31'):
    """
    http://data.eastmoney.com/yjfp/
    -----------------------------
    Parameter:
         date: 分红送配报告期，一般是每年的中期或年终，即6月30日或12月31日
    Return:
          上海、深圳两地交易所所有上市股票的分配方案及实施情况
          DataFrame:
                   Name:               股票名称
                   SZZBL:              每10股送转总比例
                   SGBL:               每10股送股比例
                   ZGBL：              每10股转股比例
                   XJFH：              每10股现金分红总额（元）
                   GXL:                股息率（%）
                   YAGGR:              预案公告日
                   YAGGRHSRZF:         预案公告日后10日涨幅%
                   GQDJRQSRZF:         股权登记日前10日涨幅%
                   GQDJR:              股权登记日
                   CQCXR:              除权除息日
                   CQCXRHSSRZF":       除权除息日后30日涨幅%
                   YCQTS:"35.0",
                   TotalEquity:        总股本（元）
                   EarningsPerShare:   每股收益（元）
                   NetAssetsPerShare:  每股净资产（元）
                   MGGJJ:              每股公积金（元）
                   MGWFPLY:            每股未分配利润（元）
                   JLYTBZZ:            净利润同比增长（%）
                   ReportingPeriod:    报告期
                   ResultsbyDate:      业绩披露日期
                   ProjectProgress:    实施进度和情况
                   AllocationPlan:     分配方案
    """
    url='http://data.eastmoney.com/DataCenter_V3/yjfp/getlist.ashx?js=var%20pgZjuNmi&pagesize=50000&page=1&sr=-1&sortType=SZZBL&mtk=%C8%AB%B2%BF%B9%C9%C6%B1&filter=(ReportingPeriod=^{0}^)&rt=49819281'.format(date)
    html=requests.get(url)
    text=html.text
    text=text.split("pgZjuNmi=")[1]
    data=json.loads(text)
    div=data['data']
    df=pd.DataFrame(div)
    for label in ['YAGGR','GQDJR','CQCXR','ReportingPeriod','ResultsbyDate']:
        df[label]=df[label].map(lambda x:str(x)[:10])
    df=df.set_index('Code')
    return df
    
def div_share(code):
    """
    http://data.eastmoney.com/yjfp/detail/000039.html
    --------------------------------------
    Parameter:
             code:股票代码
    Return:
         DataFrame:
                   Name:               股票名称
                   SZZBL:              每10股送转总比例
                   SGBL:               每10股送股比例
                   ZGBL：              每10股转股比例
                   XJFH：              每10股现金分红总额（元）
                   GXL:                股息率（%）
                   YAGGR:              预案公告日
                   YAGGRHSRZF:         预案公告日后10日涨幅%
                   GQDJRQSRZF:         股权登记日前10日涨幅%
                   GQDJR:              股权登记日
                   CQCXR:              除权除息日
                   CQCXRHSSRZF":       除权除息日后30日涨幅%
                   YCQTS:"35.0",
                   TotalEquity:        总股本（元）
                   EarningsPerShare:   每股收益（元）
                   NetAssetsPerShare:  每股净资产（元）
                   MGGJJ:              每股公积金（元）
                   MGWFPLY:            每股未分配利润（元）
                   JLYTBZZ:            净利润同比增长（%）
                   ReportingPeriod:    报告期
                   ResultsbyDate:      业绩披露日期
                   ProjectProgress:    实施进度和情况
                   AllocationPlan:     分配方案

    """
    url='http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=DCSOBS&token=70f12f2f4f091e459a279469fe49eca5&p=1&ps=5000&sr=-1&st=ReportingPeriod&filter=&cmd={0}&js=var%20HolPnOBQ={1}&rt=49824882'.format(code,"{pages:%28tp%29,data:%28x%29}")
    html=requests.get(url)
    text=html.text
    text=text.split("HolPnOBQ=")[1]
    text=text.replace('pages','"pages"')
    text=text.replace('data','"data"')
    data=json.loads(text)
    div=data['data']
    df=pd.DataFrame(div)
    #print(df.columns)
    for label in ['YAGGR','GQDJR','CQCXR','ReportingPeriod','ResultsbyDate']:
        df[label]=df[label].map(lambda x:str(x)[:10])    
    df=df.set_index('ReportingPeriod')
    return df

def div_share_mkra(code):
    """
    记录分红方案对市场的反映，即推出分红后该股的表现，即是涨跌情况
    http://data.eastmoney.com/yjfp/detail/000039.html
    --------------------------------------
    Parameter:
             code:股票代码
    Return:
         DataFrame:
                   Name:               股票名称
                   SZZBL:              每10股送转总比例
                   SGBL:               每10股送股比例
                   ZGBL：              每10股转股比例
                   XJFH：              每10股现金分红总额（元）
                   GXL:                股息率（%）
                   YAGGR:              预案公告日
                   YAGGRHSRZF:         预案公告日后10日涨幅%
                   GQDJRQSRZF:         股权登记日前10日涨幅%
                   GQDJR:              股权登记日
                   CQCXR:              除权除息日
                   CQCXRHSSRZF":       除权除息日后30日涨幅%
                   YCQTS:"35.0",
                   TotalEquity:        总股本（元）
                   EarningsPerShare:   每股收益（元）
                   NetAssetsPerShare:  每股净资产（元）
                   MGGJJ:              每股公积金（元）
                   MGWFPLY:            每股未分配利润（元）
                   JLYTBZZ:            净利润同比增长（%）
                   ReportingPeriod:    报告期
                   ResultsbyDate:      业绩披露日期
                   ProjectProgress:    实施进度和情况
                   AllocationPlan:     分配方案
    """
    url='http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?type=DCSOBS&token=70f12f2f4f091e459a279469fe49eca5&p=1&ps=50&sr=-1&st=ReportingPeriod&filter=&cmd={0}&js=var%20kSoEhqiC={1}&rt=49824956'.format(code,"{pages:%28tp%29,data:%28x%29}")
    html=requests.get(url)
    text=html.text
    text=text.split("kSoEhqiC=")[1]
    text=text.replace('pages','"pages"')
    text=text.replace('data','"data"')
    data=json.loads(text)
    div=data['data']
    df=pd.DataFrame(div)
    for label in ['YAGGR','GQDJR','CQCXR','ReportingPeriod','ResultsbyDate']:
        df[label]=df[label].map(lambda x:str(x)[:10])    
    df=df.set_index('ReportingPeriod')
    return df


def _str2fl(x):
    if u'万' in x:
        x=x.replace(u'万','')
        x=float(x)
    elif u'亿' in x:
        x=x.replace(u'亿','')
        x=float(x)*10000
    elif '%' in x:
        x=x.replace('%','')
        x=float(x)
    elif u'千' in x:
        x=x.replace(u'千','')
        x=float(x)/10
    elif x.strip()=='-':
        x=x.replace('-','')
    return x

def _totime(x):
    d=re.compile(r'\d+')
    u=d.findall(x)[0][:10]
    u=int(u)
    timeA=time.localtime(u)
    t=time.strftime("%Y-%m-%d",timeA)
    return t

if __name__=="__main__":
    #dd=share_div_mkra('000039')
    #df=dividen()
    #date='2017-03-31'
    #dd=_qfllcg(date)
    #dd=jgcg('2017-03-31')
    #dd=jgcgmx('600132','2017-03-31')
    #df=cashflow_emnow()
    df=controller_increase()
