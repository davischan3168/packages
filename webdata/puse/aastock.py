# -*- coding:utf-8 -*- 
"""
基本面数据接口 
Created on 2015/01/18
@author: Davis Chan
@group : Davis-webdata
@contact: racheal123@163.com
"""
import pandas as pd
import sys,os,time
import lxml.html
from lxml import etree
import requests,json
from bs4 import BeautifulSoup
import re
#from webdata.puse.hds import user_agent as hds
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
TRD_COLS=['symbol','name','engname','tradetype','lasttrade','prevclose','open','high','low','volume','currentvolume','amount','ticktime','buy','sell','high_52week','low_52week','eps','dividend','stocks_sum','pricechange','changepercent']
FR_COLS=['Closing_Date','Current_Ratio_Analysis','Capital_Adequacy_(%)','Cost-to-Income_(%)','Liquid_Fund/Deposits_(%)','Trading_Analysis','Loans/Deposits_(%)','Loans/Equity_(X)','Loans/Total_Assets_(%)','Deposits/Equity_(X)','Deposits/Total_Assets_(%)','Return_on_Investment_Analysis','Return_on_Loans_(%)','Return_on_Deposits_(%)','Return_on_Equity_(%)','Return_on_Total_Assets_(%)','Investment_Income_Analysis','Dividend_Payout_(%)','Related_Statistics','Fiscal_Year_High','Fiscal_Year_Low','Fiscal_Year_PER_Range_High_(X)','Fiscal_Year_PER_Range_Low_(X)','Fiscal_Year_Yield_Range_High_(%)','Fiscal_Year_Yield_Range_Low_(%)']
Div_COls=['Date','Year','Items','Particular','Type','Ex-Date','Book Close Date','Payable Date']
DATA_GETTING_TIPS = '[Getting data:]'
DATA_GETTING_FLAG = '#'
MI={'HSI':'hang-sen-40',#香港恒生指数 
    'DJI':'us-30',#道琼斯工业平均指数 
    'SPX':'us-spx-500',#美国标准普尔500指数 
    'IXIC':'nasdaq-composite',#纳斯达克综合指数
    'GDDAXI':'germany-30',#德国DAX30指数 
    'FTSE':'uk-100',#英国富时100指数
    'US2000':'smallcap-2000',#'美国小型股2000 (CFD)'
    'VIX':'volatility-s-p-500',#'CBOE Volatility Index'
    'GSPTSE':'s-p-tsx-composite',#'加拿大多伦多S&P/TSX 综合指数'
    'BVSP':'bovespa',#'巴西IBOVESPA股指'
    'MXX':'ipc',#'墨西哥IPC指数'
    'FCHI':'france-40',#'法国CAC40指数 (CFD)'
    'STOXX50E':'eu-stoxx50',#'欧洲斯托克(Eurostoxx)50指数 (CFD)'
    'AEX':'netherlands-25',#'荷兰AEX指数 (CFD)'
    'IBEX':'spain-35',#'西班牙IBEX35指数 (CFD)'
    'FTMIB':'it-mib-40',#'意大利富时MIB指数 (CFD)'
    'SSMI':'switzerland-20',#'瑞士SWI20指数 (CFD)'
    'PSI20':'psi-20',#'葡萄牙PSI20指数 (CFD)'
    'BFX':'bel-20',#'比利时BEL20指数 (CFD)'
    'OMXS30':'omx-stockholm-30',#'瑞典OMX斯德哥尔摩30指数'
    'MCX':'mcx',#'俄罗斯MICEX指数'
    'IRTS':'rtsi',#'俄罗斯交易系统市值加权指数'
    'XU100':'ise-100',#'土耳其伊斯坦堡100指数'
    'TA25':'ta25',#'以色列特拉维夫TA25指数'
    'TASI':'tasi',#'沙特阿拉伯TASI指数'
    'N225':'japan-ni225',#'日经225指数'
    'AXJO':'aus-200',#'澳大利亚S&P/ASX200指数'
    'FTSE':'ftse-china-a50',#'富时中国A50指数'
    'DJSH':'dj-shanghai',#'Dow Jones Shanghai'
    'TWII':'taiwan-weighted',#'台湾加权指数'
    'KS11':'kospi',#'韩国KOSPI指数'
    'JKSE':'idx-composite',#'印尼雅加达综合指数'
    'NSEI':'s-p-cnx-nifty',#'印度S&P CNX NIFTY指数'
    'BSESN':'sensex',#'印度孟买30指数'
    'CS':'cse-all-share'#'斯里兰卡科伦坡指数'
}
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
def delect_same_rows(fp):
    print ('update file......')
    if os.path.exists(fp):
        df=pd.read_csv(fp)#,index_col=0)#,encoding='gbk')
        try:
            df=df.drop_duplicates(subset=['Closing Date'])
            df=df.sort_values(by=['Closing Date'])
        except:
            df=df.drop_duplicates(subset=['Date'])
            df=df.sort_values(by=['Date'])
        df=df.set_index('Closing Date')
        df.to_csv(fp)
    return df

def _handle(r):
    r=r.text
    html = lxml.html.parse(StringIO(r))
    res = html.xpath("//table[@id='cnhk-list']/*/tr")
    if PY3:
        sarr = [etree.tostring(node).decode('utf-8') for node in res]
    else:
        sarr = [etree.tostring(node) for node in res]
    sarr = ''.join(sarr)
    sarr = '<table>%s</table>'%sarr
    df = pd.read_html(sarr)[0]
    #print df
    df=df.drop(6,axis=1)
    #df=df.drop('Trend',axis=1)
    return df

def _handle_div(r):
    r=r.text
    html = lxml.html.parse(StringIO(r))
    res = html.xpath("//table[@class='tab05']/*/tr")
    if PY3:
        sarr = [etree.tostring(node).decode('gbk') for node in res]
    else:
        sarr = [etree.tostring(node) for node in res]
    sarr = ''.join(sarr)
    sarr = '<table>%s</table>'%sarr
    df = pd.read_html(sarr)[0]
    df=df.drop(0)
    df=df.drop(2,axis=1)
    return df

def _pre_code(code):
    code=str(code).zfill(5)
    return code

def HK_firatio_data_year(code):
    """
    aastock网站的数据。
    --------------------------------------
    code:香港联交所上市股票代码,like 00005
    """
    code=_pre_code(code)
    dataArr=pd.DataFrame()
    send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh,zh-CN;q=0.5',
                  'Connection':'keep-alive',
                  'DNT':'1',
                  'Host':'www.aastocks.com',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    for i in [4]:
        url="http://www.aastocks.com/en/stocks/analysis/company-fundamental/financial-ratios?symbol=%s&period=%s"%(code,i)
        r=requests.get(url=url,timeout=10,headers=send_headers)
        df=_handle(r)
        df=df.T
        dataArr=dataArr.append(df)
        uname=dataArr.ix[0,:]
        dataArr.columns=uname
        dataArr=dataArr.drop(0)
        dataArr=dataArr.set_index('Closing Date')
        dataArr=dataArr.drop('Trading Analysis',axis=1)
    return dataArr

def HK_firatio_data_hyear(code):
    """
    aastock网站的数据。
    --------------------------------------
    code:香港联交所上市股票代码,like 00005
    """    
    code=_pre_code(code)
    dataArr=pd.DataFrame()
    send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh,zh-CN;q=0.5',
                  'Connection':'keep-alive',
                  'DNT':'1',
                  'Host':'www.aastocks.com',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    for i in [2]:
        url="http://www.aastocks.com/en/stocks/analysis/company-fundamental/financial-ratios?symbol=%s&period=%s"%(code,i)
        r=requests.get(url=url,timeout=10,headers=send_headers)
        df=_handle(r)
        df=df.T
        dataArr=dataArr.append(df)
        uname=dataArr.ix[0,:]
        dataArr.columns=uname
        dataArr=dataArr.drop(0)
        dataArr=dataArr.set_index('Closing Date')
        dataArr=dataArr.drop('Trading Analysis',axis=1)
    return dataArr

def HK_firatio_data_AAST(code):
    """
    aastock网站的数据。
    --------------------------------------
    code:香港联交所上市股票代码,like 00005
    """    
    df=HK_firatio_data_year(code)
    dd=HK_firatio_data_hyear(code)
    df=df.append(dd)
    df=df.sort_index()
    df=df.dropna(how='all',axis=0)
    df=df.dropna(how='all',axis=1)
    return df

def HK_ploss_data_year(code):
    """
    aastock网站的数据。
    --------------------------------------
    code:香港联交所上市股票代码,like 00005
    """    
    code=_pre_code(code)
    dataArr=pd.DataFrame()
    send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh,zh-CN;q=0.5',
                  'Connection':'keep-alive',
                  'DNT':'1',
                  'Host':'www.aastocks.com',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    for i in [4]:
        url="http://www.aastocks.com/en/stocks/analysis/company-fundamental/profit-loss?symbol=%s&period=%s"%(code,i)
        r=requests.get(url=url,timeout=10,headers=send_headers)
        df=_handle(r)
        df=df.T
        dataArr=dataArr.append(df)
        uname=dataArr.ix[0,:]
        dataArr.columns=uname
        dataArr=dataArr.drop(0)
        dataArr=dataArr.set_index('Closing Date')
        #dataArr=dataArr.drop('Trading Analysis',axis=1)
    return dataArr
def HK_ploss_data_hyear(code):
    """
    aastock网站的数据。
    --------------------------------------
    code:香港联交所上市股票代码,like 00005
    """    
    code=_pre_code(code)
    dataArr=pd.DataFrame()
    send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh,zh-CN;q=0.5',
                  'Connection':'keep-alive',
                  'DNT':'1',
                  'Host':'www.aastocks.com',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    for i in [2]:
        url="http://www.aastocks.com/en/stocks/analysis/company-fundamental/profit-loss?symbol=%s&period=%s"%(code,i)
        r=requests.get(url=url,timeout=10,headers=send_headers)
        df=_handle(r)
        df=df.T
        dataArr=dataArr.append(df)
        uname=dataArr.ix[0,:]
        dataArr.columns=uname
        dataArr=dataArr.drop(0)
        dataArr=dataArr.set_index('Closing Date')
        #dataArr=dataArr.drop('Trading Analysis',axis=1)
        return dataArr

def HK_ploss_data_AAST(code):
    """
    aastock网站的数据。
    --------------------------------------
    code:香港联交所上市股票代码,like 00005
    """    
    df=HK_ploss_data_year(code)
    dd= HK_ploss_data_hyear(code)
    df=df.append(dd)
    df=df.sort_index()
    df=df.dropna(how='all',axis=0)
    df=df.dropna(how='all',axis=1)
    return df

def HK_bsheet_data_year(code):
    """
    aastock网站的数据。
    --------------------------------------
    code:香港联交所上市股票代码,like 00005
    """    
    code=_pre_code(code)
    dataArr=pd.DataFrame()
    send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh,zh-CN;q=0.5',
                  'Connection':'keep-alive',
                  'DNT':'1',
                  'Host':'www.aastocks.com',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    for i in [4]:
        url="http://www.aastocks.com/en/stocks/analysis/company-fundamental/balance-sheet?symbol=%s&period=%s"%(code,i)
        r=requests.get(url=url,timeout=10,headers=send_headers)
        df=_handle(r)
        df=df.T
        dataArr=dataArr.append(df)
        uname=dataArr.ix[0,:]
        dataArr.columns=uname
        dataArr=dataArr.drop(0)
        dataArr=dataArr.set_index('Closing Date')
    return dataArr

def HK_bsheet_data_hyear(code):
    """
    aastock网站的数据。
    --------------------------------------
    code:香港联交所上市股票代码,like 00005
    """    
    code=_pre_code(code)
    dataArr=pd.DataFrame()
    send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh,zh-CN;q=0.5',
                  'Connection':'keep-alive',
                  'DNT':'1',
                  'Host':'www.aastocks.com',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    for i in [2]:
        url="http://www.aastocks.com/en/stocks/analysis/company-fundamental/balance-sheet?symbol=%s&period=%s"%(code,i)
        r=requests.get(url=url,timeout=10,headers=send_headers)
        df=_handle(r)
        df=df.T
        dataArr=dataArr.append(df)
        uname=dataArr.ix[0,:]
        dataArr.columns=uname
        dataArr=dataArr.drop(0)
        dataArr=dataArr.set_index('Closing Date')
    return dataArr
def HK_bsheet_data_AAST(code):
    """
    aastock网站的数据。
    --------------------------------------
    code:香港联交所上市股票代码,like 00005
    """    
    df = HK_bsheet_data_year(code)
    dd = HK_bsheet_data_hyear(code)
    df=df.append(dd)
    df=df.sort_index()
    df=df.dropna(how='all',axis=0)
    return df

def HK_earsummary_data_year(code):
    """
    aastock网站的数据。
    --------------------------------------
    code:香港联交所上市股票代码,like 00005
    """    
    code=_pre_code(code)
    dataArr=pd.DataFrame()
    send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh,zh-CN;q=0.5',
                  'Connection':'keep-alive',
                  'DNT':'1',
                  'Host':'www.aastocks.com',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    for i in [4]:
        url="http://www.aastocks.com/en/stocks/analysis/company-fundamental/earnings-summary?symbol=%s&period=%s"%(code,i)
        r=requests.get(url=url,timeout=10,headers=send_headers)
        df=_handle(r)
        df=df.T
        dataArr=dataArr.append(df)
        uname=dataArr.ix[0,:]
        dataArr.columns=uname
        dataArr=dataArr.drop(0,axis=0)
        dataArr=dataArr.set_index('Closing Date')
    return dataArr

def HK_earsummary_data_hyear(code):
    """
    aastock网站的数据。
    --------------------------------------
    code:香港联交所上市股票代码,like 00005
    """    
    code=_pre_code(code)
    dataArr=pd.DataFrame()
    send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh,zh-CN;q=0.5',
                  'Connection':'keep-alive',
                  'DNT':'1',
                  'Host':'www.aastocks.com',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    for i in [2]:
        url="http://www.aastocks.com/en/stocks/analysis/company-fundamental/earnings-summary?symbol=%s&period=%s"%(code,i)
        r=requests.get(url=url,timeout=10,headers=send_headers)
        df=_handle(r)
        df=df.T
        dataArr=dataArr.append(df)
        uname=dataArr.ix[0,:]
        dataArr.columns=uname
        dataArr=dataArr.drop(0)
        dataArr=dataArr.set_index('Closing Date')
    return dataArr
def HK_earsummary_data_AAST(code):
    """
    aastock网站的数据。
    --------------------------------------
    code:香港联交所上市股票代码,like 00005
    """    
    df = HK_earsummary_data_year(code)
    dd = HK_earsummary_data_hyear(code)
    df=df.append(dd)
    df=df.sort_index()
    df=df.dropna(how='all',axis=0)
    df=df.dropna(how='all',axis=1)
    return df

def HK_divhis_data(code):
    """
    get data of div for H Share from sina website
    -----------------
    code: string zfill(5)
    
    """
    url="http://stock.finance.sina.com.cn/hkstock/dividends/%s.html"%code
    send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh,zh-CN;q=0.5',
                  'Connection':'keep-alive',
                  'DNT':'1',
                  'Host':'www.aastocks.com',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    r=requests.get(url=url,timeout=10)
    df=_handle_div(r)
    try:
        df.columns=Div_COls
    except:
        pass
    return df

def get_HSI_index():
    """
    get the history data for HSI
    Parameter:
        None
        ---------------------------
        Return:
              DataFrame
                       Data
                       Open,High,Low,Close,Volume
    """
    _write_head()
    _write_console()
    dataArr=pd.DataFrame()
    send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh,zh-CN;q=0.5',
                  'Connection':'keep-alive',
                  'DNT':'1',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    try:
        url='http://cn.investing.com/indices/hang-sen-40-historical-data'
        #print(url)
        r=requests.get(url,headers=send_headers)
        r=r.text
        text=r
        text = text.replace('--', '')
        text = text.replace('年','-')
        text = text.replace('月','-')
        text = text.replace('日','')
        html = lxml.html.parse(StringIO(text))
        res = html.xpath("//table[@id=\"curr_table\"]/tbody/tr")
        if PY3:
            sarr = [etree.tostring(node).decode('utf-8') for node in res]
        else:
            sarr = [etree.tostring(node) for node in res]
        sarr = ''.join(sarr)
        #print sarr
        sarr = '<table>%s</table>'%sarr
        df = pd.read_html(sarr,header=None)[0]
        #df=df.drop(0)
        df.columns = ['Date','Close','Open','High','Low','Volumn','Change']
        df.Date=pd.to_datetime(df['Date'])
        df=df.sort_values(by='Date')
        #df=df.set_index('Date')
        dataArr = dataArr.append(df, ignore_index=True)
        return dataArr
    except Exception as e:
        print(e)
def get_mainindex_data(code):
    """
    获得全球主要股指指数的数据
    Parameters:
    --------------------
      code:String
    Return
    """

    df =  _get_mainindex_investing(code,pd.DataFrame())
    if df is not None:
        #df['code'] = df['code'].map(lambda x:str(x).zfill(6))
        return df
    
def _get_mainindex_investing(code,dataArr):
    _write_console()
    send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh,zh-CN;q=0.5',
                  'Connection':'keep-alive',
                  'DNT':'1',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    try:
        url='http://cn.investing.com/indices/%s-historical-data'%MI[code]
        #print(url)
        r=requests.get(url,headers=send_headers)
        r=r.text
        text=r
        text = text.replace('--', '')
        text = text.replace('年','-')
        text = text.replace('月','-')
        text = text.replace('日','')
        html = lxml.html.parse(StringIO(text))
        res = html.xpath("//table[@id=\"curr_table\"]/tbody/tr")
        if PY3:
            sarr = [etree.tostring(node).decode('utf-8') for node in res]
        else:
            sarr = [etree.tostring(node) for node in res]
        sarr = ''.join(sarr)
        #print sarr
        sarr = '<table>%s</table>'%sarr
        df = pd.read_html(sarr)[0]
        #df=df.drop(0)
        df.columns = ['Date','Close','Open','High','Low','Volumn','Change']
        df.Date=pd.to_datetime(df['Date'])
        df=df.sort_values(by='Date')
        #df=df.set_index('Date')
        dataArr = dataArr.append(df, ignore_index=True)
        return dataArr
    except Exception as e:
        print(e)
def _handle_div(r):
    r=r.text
    html = lxml.html.parse(StringIO(r))
    res = html.xpath("//table[@class=\"cnhk-cf tblM s4 s5\"]/tr")
    if PY3:
        sarr = [etree.tostring(node).decode('gbk') for node in res]
    else:
        sarr = [etree.tostring(node) for node in res]
    sarr = ''.join(sarr)
    sarr = '<table>%s</table>'%sarr
    #print (sarr)
    df = pd.read_html(sarr)[0]
    #df=df.drop(0)
    #df=df.drop(2,axis=1)
    return df
def HK_divs_AAST(code):
    """
    Get data from aastock.com
    ------------------------
    Parameters:
       code:string len is 00005
            code listed in Hongkong Exchange
    ------------------
    Return:
      ----------------
      DataFrame
            P_Date:The data for published the proposal,
            Year:  In which year and month
            D_Items: which time?
            Particular: details for the proposal
            Type:   cash or share?
            Ex-Date','Book Close Date','Payable Date'time
    """
    code=str(code).zfill(5)
    url="http://www.aastocks.com/tc/stocks/analysis/company-fundamental/dividend-history?symbol=%s"%code
    send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh,zh-CN;q=0.5',
                  'Connection':'keep-alive',
                  'Host':'www.aastocks.com',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    path='./stockdata/hkstockdata/'+code+'_div.csv'
    #r=requests.get(url=url,timeout=10,headers=send_headers)
    r=requests.get(url=url,timeout=10,headers=send_headers)

    soup=BeautifulSoup(r.text,'lxml')
    table=soup.findAll('table',attrs={'class','cnhk-cf tblM s4 s5 mar15T'})
    df=pd.read_html(str(table[1]))[0]
    df.columns=df.iloc[0,0:]
    df=df.drop(0,axis=0)
    df=df.set_index(df.columns[0])
    """
    df=_handle_div(r)
    df.columns=Div_COls
    df['code']=code
    #df=df.set_index('Date')
    if not os.path.exists(path):
        df.to_csv(path,index=False)#,encoding='gb18030')#,header=None)
    else:
        #df=df.drop(0)
        df.to_csv(path,header=None,mode='a',index=False)
    #delect_same_rows(path)
    """
    return df

def summit_for_ipo(PageNo=10):
    """
    从证监会的网站上提取提交ipo预披露和预披露更新的公司信息。
    Parameters：
        get PageNo-1 before
    -------------------------------
    Return:
         DataFrame
            name     公司名称
            date     披露或更新时间
            listed  上市地
            type    披露类型
    """
    _write_head()
    df=pd.DataFrame()
    for i in range(1,PageNo):
        try:
            df1 =  _summit_for_ipo(i,pd.DataFrame())
            if df is not None:
                df=df.append(df1)
            else:
                break
        except Exception as e:
            print (e)
    df=df.reset_index()
    df=df.drop('index',axis=1)
    return df


def _summit_for_ipo(PageNo,dataArr):
    _write_console()
    try:
        url='http://ipo.csrc.gov.cn/infoDisplay.action?pageNo=%s&temp=&temp1=&blockType=byTime'%PageNo
        #print(url)
        r=requests.get(url)
        r=r.text
        text=r
        html = lxml.html.parse(StringIO(text))
        res = html.xpath("//table/tr[@class=\"timeborder\"]")
        if PY3:
            sarr = [etree.tostring(node).decode('utf8') for node in res]
        else:
            sarr = [etree.tostring(node) for node in res]
        sarr = ''.join(sarr)
        sarr = '<table>%s</table>'%sarr
        #print (sarr)
        df = pd.read_html(sarr)[0]
        df.columns = ['name','date','listing','type_d','pdf']
        dataArr = dataArr.append(df, ignore_index=True)
        return dataArr
    except Exception as e:
        print(e)
def HK_buyback_data_AAST(code):
    """
    查询港股的回购情况，前的数据主要是按交易日统计，
    后半部数据是按月度来统计的。
    Parameter:
       code:string XXXXX.like. 08128
    ------------------------------
    Return:
       DataFrame
          Data
          Quantity(share)
          Highest Price
          Lowest  Price
    """
    url="http://www.aastocks.com/en/stocks/analysis/company-fundamental/securities-buyback?symbol=%s"%code
    send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh,zh-CN;q=0.5',
                  'Connection':'keep-alive',
                  'DNT':'1',
                  'Host':'www.aastocks.com',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    r=requests.get(url=url,timeout=10,headers=send_headers)
    df=_handle_div(r)
    names=df.ix[0]
    df=df.drop(0,axis=0)
    df.columns=names
    df=df.reset_index(drop=True)
    return df

def _summit_for_ipoII(PageNo,down,dataArr):
    _write_console()
    try:
        url='http://ipo.csrc.gov.cn/infoDisplay.action?pageNo=%s&temp=&temp1=&blockType=byTime'%PageNo
        r=requests.get(url)
        r=r.text
        html = lxml.html.parse(StringIO(r))
        res = html.xpath("//table/tr[@class=\"timeborder\"]")
        data=[]
        for td in res:
            co=td.xpath('td[1]/text()')[0].replace('\t','').replace('\r','').replace('\n','')
            date=td.xpath('td[2]/text()')[0].replace('\t','').replace('\r','').replace('\n','')
            addr=td.xpath('td[3]/text()')[0].replace('\t','').replace('\r','').replace('\n','')
            mtype=td.xpath('td[4]/text()')[0].replace('\t','').replace('\r','').replace('\n','')
            purl='%s%s'%('http://ipo.csrc.gov.cn/',td.xpath('td[5]/a/@href')[0])
            co=co.strip()
            data.append([co, date, addr, mtype, purl])
            if down:
                download_file(purl,co+date)
        names=['name','date','addr','type_d','url']
        df = pd.DataFrame(data,columns=names)
        """
        for label in names:
            df[label]=df[label].astype(str)
        """
        return df
    except Exception as e:
        print(e)

def summit_for_ipoII(n=2,down=False):
    """
    从证监会的网站上提取提交ipo预披露和预披露更新的公司信息。
    Parameters：
       n:    get the page 1 to n-1
       downl:boolen,True or False,if True then download the document,
                    False,then do not download.
    -------------------------------
    Return:
         DataFrame
            name     公司名称
            date     披露或更新时间
            listed  上市地
            type    披露类型
             url    申报文件的url地址 for download document.
    """
    _write_head()
    df=pd.DataFrame()
    for i in range(1,n):
        try:
            df1 =  _summit_for_ipoII(i,down,pd.DataFrame())
            if df is not None:
                df=df.append(df1)
        except Exception as e:
            print (e)
    df=df.reset_index(drop=True)
    return df

def download_file(url,co): 
    """
    从网站上下载文件，需要知道相应的网址，输入另存为的文件名
    Parameter:
       url:string, down file url
       co: string,name for save the files
    """
    doc_type=os.path.splitext(url)[-1]
    local_filename = '../ipo_doc/'+ co+doc_type
    if not os.path.exists(local_filename):
        # NOTE the stream=True parameter  
        r = requests.get(url, stream=True)  
        with open(local_filename, 'wb') as f:  
            for chunk in r.iter_content(chunk_size=1024):  
                if chunk: # filter out keep-alive new chunks  
                    f.write(chunk)  
                    f.flush()  
        print ('Download %s finished'%co)
    return
def all_invest_mainindex():
    """
    get data of mainindex for close, high, low, change and percent from 
    investing website
    """    
    send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh,zh-CN;q=0.5',
                  'Connection':'keep-alive',
                  'DNT':'1',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}
    try:
        url='http://cn.investing.com/indices/major-indices'
        r=requests.get(url,headers=send_headers)
        text=StringIO(r.text)#.decode("utf8")
        html = lxml.html.parse(text)
        #html = lxml.html.parse(url)
        res = html.xpath("//table[@id=\"cr_12\"]/tbody/tr")
        if PY3:
            sarr = [etree.tostring(node).decode('utf-8') for node in res]
        else:
            sarr = [etree.tostring(node) for node in res]
        sarr = ''.join(sarr)
        #print (sarr)
        sarr = '<table>%s</table>'%sarr
        df = pd.read_html(sarr,header=None)[0]
        #print (df)
        df=df.drop(0,axis=1)
        df=df.drop(8,axis=1)
        df.columns = ['Index','Close','High','Low','Change','Percent','Date']
        return df
    except Exception as e:
        print(e)

def all_invest_mainindexII():
    """
    get data of mainindex for close, high, low, change and percent from 
    investing website
    """
    send_headers={'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                  'Accept-Encoding':'gzip, deflate',
                  'Accept-Language':'zh,zh-CN;q=0.5',
                  'Connection':'keep-alive',
                  'DNT':'1',
                  'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0'}    

    try:
        url='http://cn.investing.com/indices/major-indices'
        r=requests.get(url,headers=send_headers)
        text=r.text
        html = lxml.html.parse(StringIO(text))
        #html = lxml.html.parse(url)
        res = html.xpath("//table[@id=\"cr_12\"]/tbody/tr")
        data=[]
        for td in res:
            title=td.xpath('td[2]/a/@title')[0]
            url=td.xpath('td[2]/a/@href')[0]
            close=td.xpath('td[3]/text()')[0]
            high=td.xpath('td[4]/text()')[0]
            low=td.xpath('td[5]/text()')[0]
            change=td.xpath('td[6]/text()')[0]
            percent=td.xpath('td[7]/text()')[0]
            date=td.xpath('td[8]/text()')[0]
            code=os.path.split(url)[1]
            url='http://cn.investing.com/indices%s-historical-data'%url
            data.append([title,code,close,high,low,change,percent,date,url])
        df = pd.DataFrame(data,columns=['Index','Code','Close','High','Low','Change','Percent','Date','Url'])
        return df
    except Exception as e:
        print(e)

def _law_wenshu(mtyp='CPWS'):
    surl='http://policy.mofcom.gov.cn/blank/ccase!listByLibCode.action?libCode={1}&pager.pageNo={0}'.format(1,mtyp)
    r=requests.get(surl)
    r=r.text
    text=r
    html = lxml.html.parse(StringIO(text))
    get_tp=html.xpath("//div[@class=\"div_btn2\"]/text()")
    tp=re.findall(r'\d*',get_tp[0])[1]
    return tp
def _law_wenshuI(PageNo,mtyp='CPWS'):
    _write_console()
    url='http://policy.mofcom.gov.cn/blank/ccase!listByLibCode.action?libCode=CPWS&pager.pageNo={0}'.format(PageNo)
    r=requests.get(url)
    r=r.text
    text=r
    html = lxml.html.parse(StringIO(text))
    res =html.xpath("//table[@class=\"table_tr1\"]/tr/td/table/tr")
    data=[]
    for td in res:
        try:
            des=td.xpath("td[2]/a/font/text()")[0]
            iturl='%s%s'%('http://policy.mofcom.gov.cn',td.xpath('td[2]/a/@href')[0])
            date=td.xpath('td[3]/font/text()')[0].replace('\t','').replace('\r','').replace('\n','').replace('[','').replace(']','').replace(' ','')
            if mtyp =='CPWS':
                mtype='中国法院裁判文书库'
            else:
                mtype='最高人民法院公报案例库'
            data.append([des,iturl,mtype,date])
        except Exception as e:
            pass
            #print(e)
    df=pd.DataFrame(data,columns=['description','url','type','date'])
    return df
def get_law_wenshu(startpage=None,endpage=None,mtyp='CPWS'):
    """
    Parameter:
        startpage: int,and which is bigger than 0.
        endpage:   int,and which is bigger than 0 and startpage
        mtyp     : String, include:
                              'CPWS'中国法院裁判文书库,
                              'GBAL'最高人民法院公报案例库
    -------------------------------------
    Return:
          DataFrame:
              description: 案件的描述,string
              url:案件的描述的网络地址,url of the website for the content
              date:案件公文发布的时间,%Y-%m-%d

    """
    if startpage is None:
        startpage=1
    if endpage is None:
        tp=_law_wenshu()
        endpage=int(tp)+1

    _write_head()
    dd=pd.DataFrame()
    for i in range(startpage,endpage):
        try:
            df=_law_wenshuI(i,mtyp)
            if df is not None:
                dd=dd.append(df)
        except Exception as e:
            print(e)
    dd=dd.reset_index(drop=True)
    return dd

def _law(mtyp='A'):
    if mtyp in ['A','B','C','D']:
        surl='http://policy.mofcom.gov.cn/blank/claw!findMoreByXLCode.action?xlcode={1}&pager.pageNo={0}'.format(1,mtyp)
    elif mtyp in ['DFFG','GAT']:
        surl='http://policy.mofcom.gov.cn/service/claw!findMoreByXLCode.action?libCode={1}&pager.pageNo={0}'.format(1,mtyp)
    else:
        print("=== Unkown Type ====")
    r=requests.get(surl)
    r=r.text
    text=r
    html = lxml.html.parse(StringIO(text))
    get_tp=html.xpath("//div[@class=\"div_btn2\"]/text()")
    tp=re.findall(r'\d*',get_tp[0])[1]
    return tp

def _lawI(PageNo,mtyp='A'):
    _write_console()
    if mtyp in ['A','B','C','D']:
        url='http://policy.mofcom.gov.cn/blank/claw!findMoreByXLCode.action?xlcode={1}&pager.pageNo={0}'.format(PageNo,mtyp)
    elif mtyp in ['DFFG','GAT']:
        url='http://policy.mofcom.gov.cn/service/claw!findMoreByXLCode.action?libCode={1}&pager.pageNo={0}'.format(PageNo,mtyp)
    else:
        print("=== Unkown Type ====")
    r=requests.get(url)
    r=r.text
    text=r
    html = lxml.html.parse(StringIO(text))
    res =html.xpath("//table[@class=\"table_tr1\"]/tr/td/table/tr")
    data=[]
    for td in res:
        try:
            des=td.xpath("td[2]/a/text()")[0]
            iturl='%s%s'%('http://policy.mofcom.gov.cn',td.xpath('td[2]/a/@href')[0])
            date=td.xpath('td[3]/text()')[0].replace('\t','').replace('\r','').replace('\n','').replace('[','').replace(']','').replace(' ','')
            try:
                mtype=td.xpath("td[2]/font/text()")[0].replace(']','').replace('[','')
            except:
                if mtyp =='GAT':
                    mtype='港澳台法规'
                else:
                    mtype='地方法规'
            data.append([des,iturl,mtype,date])
        except Exception as e:
            pass
            #print(e)
    df=pd.DataFrame(data,columns=['description','url','type','date'])
    return df

def get_law(startpage=None,endpage=None,mtyp='A'):
    """
    Parameter:
        startpage: int,and which is bigger than 0.
        endpage:   int,and which is bigger than 0 and startpage
        mtyp:      string, include: 'A'国家法律,
                                    'B'行政法规,
                                    'C'部门规章,
                                    'D'司法解释,
                                    'DFFG'地方法规,
                                    'GAT'港澳台
    -------------------------------------
    Return:
          DataFrame:
              description: 案件的描述,string
              url:         案件的描述的网络地址,url of the website for the content
              mtype:        string,法律的类型，如司法解释、国家法律,
              date:案件公文发布的时间,%Y-%m-%d

    """
    if startpage is None:
        startpage=1
    if endpage is None:
        tp=_law(mtyp)
        endpage=int(tp)+1
    else:
        endpage+=1
    _write_head()
    dd=pd.DataFrame()
    for i in range(startpage,endpage):
        try:
            df=_lawI(i,mtyp)
            if df is not None:
                dd=dd.append(df)
        except Exception as e:
            print(e)
    dd=dd.reset_index(drop=True)
    return dd

def HK_code_HKEX():
    """
    获取香港联交所的主板和创业板股票代码、名称、交易单位、是否可以卖空、是否纳入
    股票期权、是否纳入股票期货等信息。
    code:股票代码，由五位数字组成；
    name：名称
    unit：买卖单位，股
    trade:# 已纳入中央结算及交收系统
    sell：是否可以卖空，若是，则值为H
    option：是否纳入股票期权，若是，则值为O，
    future：是否纳入股票期货，若是，则值为F。
    
    """
    url='http://www.hkex.com.hk/chi/market/sec_tradinfo/stockcode/eisdeqty_c.htm'
    urr='http://www.hkex.com.hk/chi/market/sec_tradinfo/stockcode/eisdgems_c.htm'

    r=requests.get(url)
    content=r.content.decode('utf8')
    soup=BeautifulSoup(content,'lxml')
    s=soup.find('table',attrs={'class':'table_grey_border'})
    s=str(s)
    df=pd.read_html(s)[0][1:]
    
    r=requests.get(urr)
    content=r.content.decode('utf8')
    soup=BeautifulSoup(content,'lxml')
    s=soup.find('table',attrs={'class':'table_grey_border'})
    s=str(s)
    dd=pd.read_html(s)[0][1:]

    codes=pd.concat([df,dd],axis=0)
    codes.columns=['code','name','unit','trade','sell','option','future']
    codes=codes.reset_index(drop=True)
    return codes
def HK_cashfl_AAST(code):
    """
    code: HK share 5 string Like 00005\
          Mainland share code like 600010
    return:
           DataFrame
             前两列为散户的买入现金流，
             中两列是大户的买入现金流，
             后两列是所有股东买入先进入。
             后面数据的单位是百万港百（million HK$)
    """
    url='http://www.aastocks.com/en/stocks/analysis/moneyflow.aspx?symbol={}&type=h'.format(code)
    rr=requests.get(url)
    rr=rr.content.decode('utf8')
    html = lxml.html.parse(StringIO(rr))
    #res = html.xpath("//table[@class='mfTable s2 tblM']/*/tr[position()>1]")
    #res = html.xpath("//table[@class='mfTable s2 tblM']/*/tr")
    res=html.xpath('//table[@class="ns2 mar15T"]/*/tr')
    sarr = [etree.tostring(node).decode('utf8') for node in res]
    #sarr=str(sarr)
    sarr = ''.join(sarr)
    sarr = '<table>%s</table>'%sarr
    df = pd.read_html(str(sarr))[0]
    name=df.iloc[1,:]
    df=df.drop(0)
    df=df.drop(1)
    df.columns=name
    df=df.set_index('Date')
    return df

freq={'d':'1d','w':'1wk','m':'1mo'}
def get_trade_datayaho(code,start,end,ktype):

    ktype=ktype.lower()
    startdate=int(time.mktime(time.strptime(start,'%Y-%m-%d')))
    enddate=int(time.mktime(time.strptime(end,'%Y-%m-%d')))
    
    url="https://finance.yahoo.com/quote/{0}/history?period1={1}&period2={2}&interval={3}&filter=history&frequency={3}".format(code,startdate,enddate,freq[ktype])

    print(url)
    #ss=requests.Session()
    #r=ss.get(url,headers=hds())
    r=requests.get(url,headers=hds())
    html=lxml.html.parse(StringIO(r.text))


    res=html.xpath('//div[@id="Col1-1-HistoricalDataTable-Proxy"]/section/div[2]//tr')

    data=[etree.tostring(node) for node in res[:-1]]
    sarr='<table>%s</table>'%data
    #print(sarr)
    df=pd.read_html(sarr,header=0)[0]
    df=df.dropna(subset=['Volume'])
    return df

if __name__=="__main__":
    df=get_trade_datayaho('0005.hk','2001-01-01','2017-09-13','d')
    #df=HK_cashfl_AAST('00005')
