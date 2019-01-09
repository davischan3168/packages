# -*- coding:utf-8 -*- 
import pandas as pd
import numpy as np
import sys,os,json,time
#from tushare.stock import cons as ct
import lxml.html
from bs4 import BeautifulSoup
from lxml import etree
import re,sys,os,requests
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
#sys.setdefaultencoding('gbk')
DATE_CHK_MSG = '年度输入错误：请输入1989年以后的年份数字，格式：YYYY'
DATE_CHK_Q_MSG = '季度输入错误：请输入1、2、3或4数字'
REPORT_COLS=['date','N_O','Buy','Sell','B_S','Day_balance','T_balance','Name','p_change','code','index','index_pchg']
Main14_COLS=['date','eps','np','np_yoy','np_d','business_income','bi_yoy','nabs','roe','roe_a','a_libility_r','reservedPerShare','undistrib_ps','cf_ps']
#,'sale_margin','inventory_turnover_rate']
Main16_COLS=['date','eps','np','np_yoy','np_d','business_income','bi_yoy','nabs','roe','roe_a','a_libility_r','reservedPerShare','undistrib_ps','cf_ps','sale_margin','inventory_turnover_rate']
LABEL=['eps','np','np_yoy','np_d','business_income','bi_yoy','nabs','roe','roe_a','a_libility_r','reservedPerShare','undistrib_ps','cf_ps','sale_margin','inventory_turnover_rate']
REPORT_cash=['code','name','close','p_change','turnover','inamount','outamount','netamount','t_amount','big_inamount']
Main14_COLShk=['date','eps','eps_d','div','nvps','cfps','bsps','reservedPerShare','profits_0000','roe','mb_np_r','a_libility_r']
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



def get_current_hu_ths():
    _write_head()
    _write_console()
    try:
        url='http://data.10jqka.com.cn/hgt/hgtb/'
        r=requests.get(url,headers=hds())
        r=r.text
        r=r.split('var dataDay = [[[',1)[1]
        #r=r.split('["2016-04-12",1731.5500]]];',1)[0]
        r=r.split(']]];',1)[0]
        r=r.split(']],[[',1)[0]
        r=r.replace('],','\n')
        r=r.replace('[','')
        r=r.replace('"','')
        df=pd.read_csv(StringIO(r),header=None)
        df.columns=['time','trade_amount','day_balance']
        return df
    except Exception as e:
        print(e)    
def get_current_hongk_ths():
    _write_head()
    _write_console()
    try:
        url='http://data.10jqka.com.cn/hgt/ggtb/'
        r=requests.get(url,headers=hds())
        r=r.text
        r=r.split('var dataDay = [[[',1)[1]
        #r=r.split('["2016-04-12",1731.5500]]];',1)[0]
        r=r.split(']]];',1)[0]
        r=r.split(']],[[',1)[0]
        r=r.replace('],','\n')
        r=r.replace('[','')
        r=r.replace('"','')
        df=pd.read_csv(StringIO(r),header=None)
        df.columns=['time','trade_amount','day_balance']
        return df
    except Exception as e:
        print(e)    
def _handle(r):
    r=r.replace('[','')
    r=r.replace(']','')
    r=r.replace('}','')
    r=r.replace('simple','')
    r=r.replace('title','')
    r=r.replace('year','')
    r=r.replace(':','')
    r=r.replace('"','')
    r=r.replace('false','')
    return r
def _filter_data_fi(r):
    r=r.text
    r=r.split('"report":',1)[1]
    r=r.split(']]}',1)[0]
    r=r.replace('],','\n')
    f=r.split(':[[',2)[0]
    q=r.split(':[[',2)[1]
    y=r.split(':[[',2)[2]
    f=_handle(f)
    q=_handle(q)
    y=_handle(y)
    return f,q,y

def get_finance_index_ths(code):
    """
    获取上海或深圳交易所的上市的股票财务指标
    _______________
    code: like 600422
    ----------------------------------------
    return:
           date:             报告的截至时间
           eps:              每股收益，元
           np:               净利润，万元
           np_yoy:           净利润增长率，%
           np_d:             扣除非经常性损益后的净利润，万元
           business_income:  营业收入，万元
           bi_yoy:           营业收入增长率，%
           nabs:             每股净资产，元
           roe:              净资产收益率，%
           roe_a:            净资产收益率（摊薄），%
           a_libility_r:      资产负债率，%
           reservedPerShare:  每股盈余公积金，元
           undistrib_ps:     每股分配利润，元
           cf_ps:            每股经营性现金流，元
           sale_margin:      销售毛利率，%
           inventory_turnover_rate:存货周转率，%
    """
    _write_head()
    _write_console()
    try:
        url="http://stockpage.10jqka.com.cn/basic/%s/main.txt"%code
        r=requests.get(url,timeout=10,headers=hds())
        f,q,y=_filter_data_fi(r)
        df=pd.read_csv(StringIO(f),header=None)
        df=df.T
        if df.shape[1]==14:
            df.columns=Main14_COLS
            df['sale_margin']=np.nan
            df['inventory_turnover_rate']=np.nan
        elif df.shape[1]==16:
            df.columns=Main16_COLS
        df['code']=code
        df=df.set_index('code')
        for label in LABEL:
            df[label]=df[label].astype(float)
        return df
    except Exception as e:
        print(e)

def get_finance_index_simple(code):
    _write_head()
    _write_console()
    try:
        url="http://stockpage.10jqka.com.cn/basic/%s/main.txt"%code
        r=requests.get(url,timeout=10,headers=hds())
        f,q,y=_filter_data_fi(r)
        df=pd.read_csv(StringIO(q),header=None)
        df=df.T
        if df.shape[1]==14:
            df.columns=Main14_COLS
            df['sale_margin']=np.nan
            df['inventory_turnover_rate']=np.nan
        elif df.shape[1]==16:
            df.columns=Main16_COLS
        df['code']=code
        df=df.set_index('code')
        return df
    except Exception as e:
        print(e)

def get_finance_index_year(code):
    _write_head()
    _write_console()
    try:
        url="http://stockpage.10jqka.com.cn/basic/%s/main.txt"%code
        r=requests.get(url,timeout=10,headers=hds())
        f,q,y=_filter_data_fi(r)
        df=pd.read_csv(StringIO(y),header=None)
        df=df.T
        if df.shape[1]==14:
            df.columns=Main14_COLS
            df['sale_margin']=np.nan
            df['inventory_turnover_rate']=np.nan
        elif df.shape[1]==16:
            df.columns=Main16_COLS
        df['code']=code
        df=df.set_index('code')
        return df
    except Exception as e:
        print(e)
def get_cashflow_thspershare(code):
    """
    code:  string 上海和深圳交易所的股票代码，like 600422
    ----------------
    return:
           close:        收盘价，单位元
           change：      涨跌幅 %
           net_income：  当日资金净流入，万元
           net_income_5：5日资金净流入（万元）
           l_net，l_per：大单资金流入（万元）及占比（%）
           m_net,m_per： 中单资金流入（万元）及占比（%）
           s_net,s_per： 小单资金流入（万元）及占比（%）
    """
    url='http://stockpage.10jqka.com.cn/{}/funds/'.format(code)
    r=requests.get(url,headers=hds())
    content=r.text
    soup=BeautifulSoup(content,'lxml')
    data=soup.find('table',attrs={'class':"m_table_3"})
    data=str(data)
    df=pd.read_html(data)[0]
    df=df.drop(0)
    df=df.drop(1)
    df.columns=['date','close','change','net_income','net_income_5','l_net','l_per','m_net','m_per','s_net','s_per']#REPORT_COLS
    df['date']=pd.to_datetime(df['date'])
    for label in ['close','change','net_income','net_income_5','l_net','l_per','m_net','m_per','s_net','s_per']:
        #map(lambda x: _str2fl(x))
        try:
            df[label]=df[label].map(lambda x: x.replace('%',''))
            df[label]=df[label].astype(float)
        except:
            df[label]=df[label].astype(float)
    df=df.set_index('date')
    return df
def get_cashflow_thsnow():
    """
    Parameters:
    ---------------------------------
    return:
          DataFrame:
             code:      股票代码
             name：     股票名称
             close：    最新价格（元）
             p_change： 涨跌幅%
             turnover： 换手率
             inamount： 流入金额（万元）
             outamount：流出金额（万元）
             netamount：现金净流入额（万元）
             t_amount： 成交金额（万元）
             big_inamount：大胆流入额（万元）
    """
    _write_head()
    dataArr=pd.DataFrame()
    for i in range(1,55,1):
        try:
            _write_console()
            url="http://data.10jqka.com.cn/funds/ggzjl/field/zdf/order/desc/page/{0}/ajax/1/".format(i)
            send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                      'Accept-Encoding':'gzip, deflate',
                      'Accept-Language':'zh,zh-CN;q=0.5',
                      'Connection':'keep-alive',
                      'DNT':'1',
                      'Host':'data.10jqka.com.cn',
                      'Referer':'http://www.10jqka.com.cn/',
                      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
            }
            #print(url)
            #print ("Get page %s completed"%i)
            r=requests.get(url,headers=send_headers,timeout=10)
            r=r.text
            text=r
            html = lxml.html.parse(StringIO(text))
            res = html.xpath("//table/tbody/tr")
            if PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            #print sarr
            sarr = '<table>%s</table>'%sarr
            df = pd.read_html(sarr)[0]
            #df=df.drop(0)
            df = df.drop(0, axis=1)
            df.columns = REPORT_cash
            dataArr = dataArr.append(df, ignore_index=True)
        except Exception as e:
            print(e)
    dataArr['code'] = dataArr['code'].map(lambda x:str(x).zfill(6))
    dataArr=dataArr.set_index('code')
    for label in ['p_change','turnover','inamount','outamount','netamount','t_amount','big_inamount']:
        dataArr[label]=dataArr[label].map(lambda x: _str2fl(x))
    return dataArr

def get_cashflow_ths3days():
    """
    Parameters:
    ---------------------------------
    return:
          DataFrame:    
             code:              股票代码
             name:              股票名称
             price:             最新价
             percent_period:    阶段涨跌幅%
             turn_over:         连续换手率%
             net_income:        资金流入净额(万元)
    """
    _write_head()
    dataArr=pd.DataFrame()
    for i in range(1,55,1):
        try:
            _write_console()
            url="http://data.10jqka.com.cn/funds/ggzjl/board/3/field/zdf/order/desc/page/{0}/ajax/1/".format(i)
            send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                      'Accept-Encoding':'gzip, deflate',
                      'Accept-Language':'zh,zh-CN;q=0.5',
                      'Connection':'keep-alive',
                      'DNT':'1',
                      'Host':'data.10jqka.com.cn',
                      'Referer':'http://www.10jqka.com.cn/',
                      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
            }
            r=requests.get(url,headers=send_headers,timeout=10)
            r=r.text
            text=r
            html = lxml.html.parse(StringIO(text))
            res = html.xpath("//table/tbody/tr")
            if PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>'%sarr
            df = pd.read_html(sarr)[0]
            df = df.drop(0, axis=1)
            df.columns = ['code','name','price','percent_period','turn_over','net_income']
            dataArr = dataArr.append(df, ignore_index=True)
        except Exception as e:
            print(e)
    dataArr['code'] = dataArr['code'].map(lambda x:str(x).zfill(6))
    dataArr=dataArr.set_index('code')
    for label in ['percent_period','turn_over','net_income']:
        dataArr[label]=dataArr[label].map(lambda x: _str2fl(x))
    return dataArr

def get_cashflow_ths5days():
    """
    Parameters:
    ---------------------------------
    return:
          DataFrame:    
             code:              股票代码
             name:              股票名称
             price:             最新价
             percent_period:    阶段涨跌幅%
             turn_over:         连续换手率%
             net_income:        资金流入净额(万元)
    """
    _write_head()
    dataArr=pd.DataFrame()
    for i in range(1,55,1):
        try:
            _write_console()
            url="http://data.10jqka.com.cn/funds/ggzjl/board/5/field/zdf/order/desc/page/{0}/ajax/1/".format(i)
            send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                      'Accept-Encoding':'gzip, deflate',
                      'Accept-Language':'zh,zh-CN;q=0.5',
                      'Connection':'keep-alive',
                      'DNT':'1',
                      'Host':'data.10jqka.com.cn',
                      'Referer':'http://www.10jqka.com.cn/',
                      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
            }
            r=requests.get(url,headers=send_headers,timeout=10)
            r=r.text
            text=r
            html = lxml.html.parse(StringIO(text))
            res = html.xpath("//table/tbody/tr")
            if PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>'%sarr
            df = pd.read_html(sarr)[0]
            df = df.drop(0, axis=1)
            df.columns = ['code','name','price','percent_period','turn_over','net_income']
            dataArr = dataArr.append(df, ignore_index=True)
        except Exception as e:
            print(e)
    dataArr['code'] = dataArr['code'].map(lambda x:str(x).zfill(6))
    dataArr=dataArr.set_index('code')
    for label in ['percent_period','turn_over','net_income']:
        dataArr[label]=dataArr[label].map(lambda x: _str2fl(x))
    return dataArr

def get_cashflow_ths10days():
    """
    Parameters:
    ---------------------------------
    return:
          DataFrame:    
             code:              股票代码
             name:              股票名称
             price:             最新价
             percent_period:    阶段涨跌幅%
             turn_over:         连续换手率%
             net_income:        资金流入净额(万元)
    """
    _write_head()
    dataArr=pd.DataFrame()
    for i in range(1,55,1):
        try:
            _write_console()
            url="http://data.10jqka.com.cn/funds/ggzjl/board/10/field/zdf/order/desc/page/{0}/ajax/1/".format(i)
            send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                      'Accept-Encoding':'gzip, deflate',
                      'Accept-Language':'zh,zh-CN;q=0.5',
                      'Connection':'keep-alive',
                      'DNT':'1',
                      'Host':'data.10jqka.com.cn',
                      'Referer':'http://www.10jqka.com.cn/',
                      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
            }
            r=requests.get(url,headers=send_headers,timeout=10)
            r=r.text
            text=r
            html = lxml.html.parse(StringIO(text))
            res = html.xpath("//table/tbody/tr")
            if PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>'%sarr
            df = pd.read_html(sarr)[0]
            df = df.drop(0, axis=1)
            df.columns = ['code','name','price','percent_period','turn_over','net_income']
            dataArr = dataArr.append(df, ignore_index=True)
        except Exception as e:
            print(e)
    dataArr['code'] = dataArr['code'].map(lambda x:str(x).zfill(6))
    dataArr=dataArr.set_index('code')
    for label in ['percent_period','turn_over','net_income']:
        dataArr[label]=dataArr[label].map(lambda x: _str2fl(x))
    return dataArr

def get_cashflow_ths20days():
    """
    Parameters:
    ---------------------------------
    return:
          DataFrame:    
             code:              股票代码
             name:              股票名称
             price:             最新价
             percent_period:    阶段涨跌幅%
             turn_over:         连续换手率%
             net_income:        资金流入净额(万元)
    """
    _write_head()
    dataArr=pd.DataFrame()
    for i in range(1,55,1):
        try:
            _write_console()
            url="http://data.10jqka.com.cn/funds/ggzjl/board/20/field/zdf/order/desc/page/{0}/ajax/1/".format(i)
            send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                      'Accept-Encoding':'gzip, deflate',
                      'Accept-Language':'zh,zh-CN;q=0.5',
                      'Connection':'keep-alive',
                      'DNT':'1',
                      'Host':'data.10jqka.com.cn',
                      'Referer':'http://www.10jqka.com.cn/',
                      'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
            }
            r=requests.get(url,headers=send_headers,timeout=10)
            r=r.text
            text=r
            html = lxml.html.parse(StringIO(text))
            res = html.xpath("//table/tbody/tr")
            if PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>'%sarr
            df = pd.read_html(sarr)[0]
            df = df.drop(0, axis=1)
            df.columns = ['code','name','price','percent_period','turn_over','net_income']
            dataArr = dataArr.append(df, ignore_index=True)
        except Exception as e:
            print(e)
    dataArr['code'] = dataArr['code'].map(lambda x:str(x).zfill(6))
    dataArr=dataArr.set_index('code')
    for label in ['percent_period','turn_over','net_income']:
        dataArr[label]=dataArr[label].map(lambda x: _str2fl(x))
    return dataArr

def _filter_hk_data(r):
    r=r.text
    r=r.split('"report":',1)[1]
    r=r.split(']],"year"',1)[0]
    r=r.replace('],','\n')
    r=r.replace('[','')
    r=r.replace(']','')
    r=r.replace('}','')
    r=r.replace('"','')
    r=r.replace('false','')
    return r

def _filter_hk_data1(r):
    r=r.text
    r=r.split(']],"year"',1)[1]
    r=r.replace('],','\n')
    r=r.replace('[','')
    r=r.replace(']','')
    r=r.replace('}','')
    r=r.replace('"','')
    r=r.replace(':','')
    r=r.replace('false','')
    return r

def HK_finance_tem_ths(code,mtype='keyindex'):
    """
    从同花顺网站获得港股的财务数据：
    http://stockpage.10jqka.com.cn/HK0817/finance/
    -------------------------------
    code: 香港联交所上市的股票代码，四个字符 like XXXX
    mtype:为获得报告的类型，
          keyindex:为主要指标
          debt:资产负债表
          benefit:利润表
          cash：现金流量表
  Return:
       DataFrame
    """
    _write_head()
    _write_console()
    try:
        url="http://stockpage.10jqka.com.cn/financeflash/hk/HK%s/%s.txt"%(code,mtype)
        r=requests.get(url,timeout=10,headers=hds())
        u=r
        #print url
        r=_filter_hk_data(r)
        df=pd.read_csv(StringIO(r),header=None)
        df=df.T
        try:
            df.columns=Main14_COLShk
            df['code']=code
            df=df.set_index('code')
            df=df.sort_values(by='date')
        except:
            pass
        return df
    except Exception as e:
        print(e)

def HK_finance_year(code):
    _write_head()
    _write_console()
    try:
        url="http://stockpage.10jqka.com.cn/financeflash/hk/HK%s/keyindex.txt"%code
        r=requests.get(url,timeout=10,headers=hds())
        u=r
        #print url
        u=_filter_hk_data1(u)
        dfy=pd.read_csv(StringIO(u),header=None)
        dfy=dfy.T
        dfy.columns=Main14_COLShk
        dfy['code']=code
        dfy=dfy.set_index('code')
        return dfy
    except Exception as e:
        print(e)

def get_current_price(stockid):
    try:
        url = 'http://d.10jqka.com.cn/v2/realhead/hs_%s/last.js' % stockid
        send_headers = {
            'Host':'d.10jqka.com.cn',
            'Referer':'http://stock.10jqka.com.cn/',
            'Accept':'application/json, text/javascript, */*; q=0.01',
            'Connection':'keep-alive',
            'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36',
            'X-Forwarded-For':'124.160.148.178',
            'X-Requested-With':'XMLHttpRequest'
        }
        req = Request(url,headers=send_headers)
        f = urlopen(req)
        data = f.read().split('items":',1)[1]
        data = data.split('})',1)[0]
        J_data = json.loads(data)
        df=pd.DataFrame.from_dict(J_data.items(),orient='columns')
        df.set_index(0,inplace=True)
        df=df.T
        df['code']=stockid
        stockpe = J_data['2034120']
        stockname = J_data['name']
        sumvalue = J_data['3475914']
        totals= J_data['402']
        currentprice = J_data['10']
        #stockpb=J_data['1149395']
        return stockname,stockpe,sumvalue,currentprice,totals
    #except urllib2.HTTPError, e:
    except:
        #return e.code
        pass


def HK_finance_ths(code,mtype='keyindex'):
    """
    从同花顺网站获得港股的财务数据：
    http://stockpage.10jqka.com.cn/HK0817/finance/
    -------------------------------
    code: 香港联交所上市的股票代码，四个字符 like XXXX
    mtype:为获得报告的类型，
          keyindex:为主要指标
          debt:资产负债表
          benefit:利润表
          cash：现金流量表
  Return:
       DataFrame
    """
    _write_head()
    _write_console()
    try:
        url="http://stockpage.10jqka.com.cn/financeflash/hk/HK%s/%s.txt"%(code,mtype)
        r=requests.get(url,timeout=10,headers=hds())
        text=r.text
        data=json.loads(text)

        name=[]
        for i in range(len(data['title'])):
            if i>0:
                name.append(''.join(data['title'][i]))
                #name.append(data['title'][i][0])

        df=pd.DataFrame(data['report'])
        df.columns=df.loc[0,0:]
        df=df.drop(0,axis=0)

        df=df.T
        df.columns=name

        #df=df.T
        df=df.dropna(how='all',axis=1)

        return df
    except Exception as e:
        print(e)    



    
def _str2fl(x):
    try:
        if '万' in x:
            x=x.strip().replace('万','')
            x=float(x)
        elif '亿' in x:
            x=x.strip().replace('亿','')
            x=float(x)*10000
        elif '%' in x:
            x=x.strip().replace('%','')
            x=float(x)
        elif '千' in x:
            x=x.strip().replace('千','')
            x=float(x)/10
        return x
    except:
        return x

if __name__=="__main__":
    df=HK_finance_ths(sys.argv[1])
