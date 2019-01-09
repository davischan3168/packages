#!/usr/bin/env python3
# -*-coding:utf-8-*-

import pandas as pd
import numpy as np
import sys,os,json,time
#from tushare.stock import cons as ct
import lxml.html
from bs4 import BeautifulSoup
from lxml import etree
import re,sys,os,requests
from webdata.util.hds import user_agent as hds
from io import StringIO
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request
import webdata.puse.thspy.cont as wt

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
seasons={1:'%s-03-31',2:'%s-06-30',3:'%s-09-30',4:'%s-12-31'}

def _str2fl(x):
    try:
        if u'万' in x:
            x=x.replace('万','')
            x=float(x)
        if u'亿' in x:
            x=x.replace('亿','')
            x=float(x)*10000
        if u'%' in x:
            x=x.replace('%','')
            x=float(x)
        if u'千' in x:
            x=x.replace('千','')
            x=float(x)/10
        return float(x)
    except:
        return x

def get_financeindex_shares_THS(code,mtype='report'):
    """
    获取上海或深圳交易所的上市的股票财务指标
    _______________
    code: like 600422
    mtype: report-季度报告
           simple 单季财务指标
           year   年度财务指标
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
        text=r.text
        data=json.loads(text)

        df=pd.DataFrame(data[mtype])
        df=df.T
        
        if df.shape[1]==14:
            df.columns=Main14_COLS
            df['sale_margin']=np.nan
            df['inventory_turnover_rate']=np.nan
        elif df.shape[1]==16:
            df.columns=Main16_COLS
            
        df['code']=code
        df=df.set_index('code')
        
        df=df.replace('',np.nan)
        df=df.applymap(lambda x:wt._tofl(x))
        df=df.sort_values(by=['date'],ascending=True)
        df['code']=df.index
        df=df.set_index('date')
        return df
    except Exception as e:
        print(e)



def get_financeindex_all_THS(year,qt):
    yqt=seasons[qt]%year
    #print(yqt)

    url='http://data.10jqka.com.cn/financial/yjgg/date/{0}/board/ALL/field/DECLAREDATE/order/desc/page/1/ajax/1/'.format(yqt)
    r=requests.get(url,timeout=10,headers=hds())
    text=r.text
    html=lxml.html.parse(StringIO(text))
    res=html.xpath('//table[@class="m-table J-ajax-table J-canvas-table"]/tbody//tr')
    if PY3:
        sarr = [etree.tostring(node).decode('utf-8') for node in res]
    else:
        sarr = [etree.tostring(node) for node in res]
    sarr = ''.join(sarr)
    sarr = '<table>%s</table>'%sarr
    df = pd.read_html(sarr)[0]
    
    
    pages=html.xpath('//div[@class="m-page J-ajax-page"]//span/text()')
    pages=int(pages[0].split('/')[1])
    #print('Total pages %s'%pages)
    if pages>1:
        for i in range(2,pages+1):
            url='http://data.10jqka.com.cn/financial/yjgg/date/{0}/board/ALL/field/DECLAREDATE/order/desc/page/{1}/ajax/1/'.format(yqt,i)
            r=requests.get(url,timeout=10,headers=hds())
            #print(url)
            text=r.text
            html=lxml.html.parse(StringIO(text))
            res=html.xpath('//table[@class="m-table J-ajax-table J-canvas-table"]/tbody//tr')
            if PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>'%sarr
            df = df.append(pd.read_html(sarr)[0])
            #print(df.tail())
    
    df=df.drop([0,15],axis=1)
    df.columns=['code','name','pdate','rev','rev_yoy','rev_hb','profit','profit_yoy','profit_hb','eps','nav','roe','cf_ps','margin']
    df=df.applymap(lambda x:_str2fl(x))
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    df=df.set_index('code')
    return df

def get_pepb_all_THS():
    #yqt=seasons[qt]%year
    #print(yqt)

    url='http://data.10jqka.com.cn/market/ggsyl/field/syl/order/asc/page/1/ajax/1/'
    r=requests.get(url,timeout=10,headers=hds())
    text=r.text
    #print(text)
    html=lxml.html.parse(StringIO(text))
    res=html.xpath('//table[@class="m-table J-ajax-table"]/tbody/tr')
    if PY3:
        sarr = [etree.tostring(node).decode('utf-8') for node in res]
    else:
        sarr = [etree.tostring(node) for node in res]
    sarr = ''.join(sarr)
    sarr = '<table>%s</table>'%sarr
    df = pd.read_html(sarr)[0]

    pages=html.xpath('//div[@class="m-page J-ajax-page"]//span/text()')
    pages=int(pages[0].split('/')[1])
    print('Total pages %s'%pages)
    if pages>1:
        for i in range(2,pages+1):
            url='http://data.10jqka.com.cn/market/ggsyl/field/syl/order/asc/page/{0}/ajax/1/'.format(i)
            r=requests.get(url,timeout=10,headers=hds())
            text=r.text
            html=lxml.html.parse(StringIO(text))
            res=html.xpath('//table[@class="m-table J-ajax-table"]/tbody/tr')
            if PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(sarr)
            sarr = '<table>%s</table>'%sarr
            df = df.append(pd.read_html(sarr)[0])
    
    df=df.drop(0,axis=1)
    df.columns=['code','name','pe','pe_ttm','price','chg','turnover']
    df=df.applymap(lambda x:_str2fl(x))
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    df=df.set_index('code')
    df=df.replace('--',np.nan)
    return df


def get_position_industry_THS(code,mtype='hy2',last=1):
    """
    获得公司所在行业的基本信息情况，如每股收益、
    净资产、净利润、营业收益、总资产、
    净资产收益率、股东权益比率、销售毛利率和总股本等信息
    -----------------------------------
    code:上海、深圳交易所的股票代码
    mtype:行业类型,hy3--3级行业分类,hy2--2级行业分类
    last：1--最新报告期，2--前一报告期
    """
    url='http://stockpage.10jqka.com.cn/{0}/field/'.format(code)

    r=requests.get(url,headers=hds(),timeout=10)

    soup=BeautifulSoup(r.text,'lxml')
    tb=soup.find(id='%s_table_%s'%(mtype,last))

    df=pd.read_html(str(tb))[0]
    df=df.applymap(lambda x:wt._str2fl(x))
    df.columns=['code','name','rank','eps','nav','cf_ps','np','rev','Total.A','Roe','Equit.D.R','Margin','Total.Sh']
    df=df.drop('rank',axis=1)
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    df=df.set_index('code')
    return df

def get_forecast_data_THS(year,quarter):
    """获得业绩预告的信息数据
    """
    quarter=int(quarter)
    yqt=seasons[quarter]%year
    url='http://data.10jqka.com.cn/financial/yjyg/date/{0}/ajax/1/'.format(yqt)
    r=requests.get(url,timeout=10,headers=hds())
    text=r.text
    html=lxml.html.parse(StringIO(text))
    res=html.xpath('//table[@class="m-table J-ajax-table J-canvas-table"]/tbody/tr')

    """
    if PY3:
        sarr = [etree.tostring(node).decode('utf-8') for node in res]
    else:
        sarr = [etree.tostring(node) for node in res]
    sarr = ''.join(str(sarr))
    sarr = '<table>%s</table>'%sarr
    """
    soup=BeautifulSoup(text,'lxml')
    sarr=soup.find('table')
    df = pd.read_html(str(sarr))[0]
    
    
    pages=html.xpath('//div[@class="m-page J-ajax-page"]//span/text()')
    pages=int(pages[0].split('/')[1])
    print('Total pages %s'%pages)
    if pages>1:
        for i in range(2,pages+1):
            url='http://data.10jqka.com.cn/financial/yjyg/date/{0}/ajax/{1}/'.format(yqt,i)
            r=requests.get(url,timeout=10,headers=hds())
            #print(url)
            text=r.text
            """
            html=lxml.html.parse(StringIO(text))
            res=html.xpath('//table[@class="m-table J-ajax-table J-canvas-table"]/tbody//tr')
            if PY3:
                sarr = [etree.tostring(node).decode('utf-8') for node in res]
            else:
                sarr = [etree.tostring(node) for node in res]
            sarr = ''.join(str(sarr))
            sarr = '<table>%s</table>'%sarr
            """
            soup=BeautifulSoup(text,'lxml')
            sarr=soup.find('table')
            df = df.append(pd.read_html(str(sarr))[0])
            #print(df.tail())
    
    #
    try:
        df.columns=['No.','code','name','type','summary','range%','np_last','date']
        df=df.drop('No.',axis=1)
        #df=df.applymap(lambda x:x.strip())
        df=df.applymap(lambda x:_str2fl(x))
        df['code']=df['code'].map(lambda x:str(x).zfill(6))
        df=df.set_index('code')
    except:
        pass
        
    return df    

def _income(text1):
    dataset=[]
    data=[]
    for i in range(len(text1)):
            
        ds=text1[i].split('\n\n\n')
        data.extend(ds)
        #print(data)
            
    for j in range(len(data)):
        tem=data[j].split('\n')
        if len(tem) == 7:
            tem.insert(0,'')
            dataset.append(tem)
        elif len(tem) ==8:
            dataset.append(tem)

    df=pd.DataFrame(dataset)
    df=df.replace('',np.nan)
    df=df.fillna(method='ffill')
    df.columns=['class','name','rev','rev.r','cost','cost.r','profit.r','margin']
    df=df.applymap(lambda x:x.strip())
    df=df.replace('-',np.nan)
    return df

def get_income_THS(code,mtype='op1'):
    """
    获取公司的存货情况、应收收入、成本等构成情况，利润率构成情况以及毛利率水平。
    ----------------------------
    code:  公司的股票代码
    mtype: op表示存货情况，1代表累计是，2代表期末值
           as应收收入、成本等构成情况，1代表最近1期，2代表上期，3代表上上期。
  Return：
     DataFrame：
     
    """
    
    url='http://stockpage.10jqka.com.cn/{0}/operate/'.format(code)
    r=requests.get(url,headers=hds(),timeout=10)

    text=r.text

    soup=BeautifulSoup(text,'lxml')
    #tables=soup.find_all('table',attrs={'class':'m_table m_hl'})
    soupp=soup.find(id="analysis")
    tabless=soupp.find_all('table')

    if mtype=='op1':
        try:
            table=soup.find(id='operate_table')
            df=pd.read_html(str(table))[0]
            return df
        except Exception as e:
            print(e)
            pass
        
    elif mtype== 'op2':
        try:
            table=soup.find(id='operate_table1')
            df=pd.read_html(str(tables[1]))[0]
            return df
        except Exception as e:
            print(e)
            pass
        
    elif mtype=='as1':
        try:
            text1=tabless[1].text.split('\n\n\n\n\r\n')[1].split('\n\n\n\r\n')
            df=_income(text1)
            return df
        except Exception as e:
            print(e)
            pass
    elif mtype=='as2':
        try:
            text1=tabless[2].text.split('\n\n\n\n\r\n')[1].split('\n\n\n\r\n')
            df=_income(text1)
            return df
        except Exception as e:
            print(e)
            pass        
    elif mtype=='as3':
        try:
            text1=tabless[3].text.split('\n\n\n\n\r\n')[1].split('\n\n\n\r\n')
            df=_income(text1)
            return df
        except Exception as e:
            print(e)
            pass        


if __name__=="__main__":
    #df=get_finance_index_THS(sys.argv[1],mtype='simple')
    #dd=get_financeindex_all_THS(year=2017,qt=2)
    #df=get_pepb_all_THS()
    #df=get_position_industry_THS(sys.argv[1],sys.argv[2],sys.argv[3])
    #df=get_forecast_data_THS(sys.argv[1],sys.argv[2])
    df=get_income_THS(sys.argv[1],sys.argv[2])
