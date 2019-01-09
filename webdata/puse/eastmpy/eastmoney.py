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
quarter={1:'%s-03-31',2:'%s-06-30',3:'%s-09-30',4:'%s-12-31'}
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

def get_currency_data():
    """
    获取当前汇率数据
    """
    _write_head()
    df =  _get_curr_data(pd.DataFrame())
    if df is not None:
        return df


def _get_curr_data(dataArr):
    _write_console()
    try:
        url='http://hq2gjqh.eastmoney.com/EM_Futures2010NumericApplication/Index.aspx?jsName=fxrc&Type=S&SortType=A&pageSize=2000&page=1&style=28AllRate&_g=0.9714039387626267'
        #print(url)
        r=requests.get(url,timeout=10)
        r=r.text#.decode('gbk','ignore').encode('gbk')
        #print r
        text=r
        r=r.split('={rank:["',1)[1]
        r=r.split('],pages',1)[0]
        r=r.replace('",','\n')
        r=r.replace('"','')
        #print r
        df = pd.read_csv(StringIO(r),header=None,encoding='utf8')
        df=df.drop(0,axis=1)
        df=df.drop(8,axis=1)
        df=df.drop(10,axis=1)
        df=df.drop(11,axis=1)
        df=df.drop(12,axis=1)
        df=df.drop(13,axis=1)
        df=df.drop(14,axis=1)
        df=df.drop(15,axis=1)
        df=df.drop(16,axis=1)
        df=df.drop(19,axis=1)
        df=df.drop(20,axis=1)
        df=df.drop(21,axis=1)
        df=df.drop(22,axis=1)
        df=df.drop(23,axis=1)
        df=df.drop(24,axis=1)
        df=df.drop(25,axis=1)
        df=df.drop(26,axis=1)
        df=df.drop(28,axis=1)
        df.columns=REPORT_COLS
        df['code']=df['code'].astype(str)#map(lambda x:str(x))
        df['time']=pd.to_datetime(df['time'])
        return df
    except Exception as e:
        print(e)

def _handle_cashflow(r):
    r=r.split("data:[",1)[1]
    r=r.replace('var vIlEropE={pages:2,data:[','')
    r=r.replace('var WzYQPLmv={pages:1,data:[','')
    r=r.replace('var uywRInNK={pages:59,date:"2014-10-22",data:[','')
    r=r.replace('var uywRInNK={pages:59,date:"2014-10-22",data:[','')
    r=r.replace('var SVNsQJPa={pages:4,data:[','')
    r=r.replace(']}','')
    r=r.replace('",','\n')
    r=r.replace('"','')
    r=r.replace(',-,','')
    return r

def get_hangye_list():
    """
    获取行业的现金流情况
    """
    Darr=pd.DataFrame()
    try:
        for i in range(1,3,1):
            url="http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C._BKHY&type=ct&st=%28BalFlowMain%29&sr=-1&p={0}&ps=50&js=var%20vIlEropE={1}&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITABK&rt=48581414".format(i,'{pages:%28pc%29,data:[%28x%29]}')
            print (url)
            r=requests.get(url)
            r=r.text
            r=_handle_cashflow(r)
            df=pd.read_csv(StringIO(r),header=None)
            Darr=Darr.append(df)

        Darr.columns=REPORT_COLS1
        Darr.drop_duplicates(subset='mark',inplace=True)
        Darr=Darr.sort_values(by='main_buy',ascending=False)
        Darr=Darr.set_index('mark')
        Darr=Darr.sort_values(by='pchg',ascending=False)
        del Darr['N1']
        return Darr
    except Exception as e:
        print(e)
        
def get_diyu_list():
    """
    获取地域的现金流情况
    """
    Darr=pd.DataFrame()
    try:
        for i in range(1,3,1):
            url="http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C._BKDY&type=ct&st=%28BalFlowMainNet5%29&sr=-1&p={0}&ps=50&js=var%20WzYQPLmv={1}&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITABK5&rt=48581407".format(i,'{pages:%28pc%29,data:[%28x%29]}')
            print (url)
            r=requests.get(url)
            r=r.text
            r=_handle_cashflow(r)
            df=pd.read_csv(StringIO(r),header=None)
            Darr=Darr.append(df)

        Darr.columns=REPORT_COLS1
        Darr.drop_duplicates(subset='mark',inplace=True)
        Darr=Darr.sort_values(by='main_buy',ascending=False)
        Darr=Darr.set_index('mark')
        del Darr['N1']
        Darr=Darr.sort_values(by='pchg',ascending=False)
        return Darr
    except Exception as e:
        print(e)

def get_gainian_list():
    """
    获取概念的现金流情况
    """
    Darr=pd.DataFrame()
    try:
        for i in range(1,3,1):
            url="http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cmd=C._BKGN&type=ct&st=%28BalFlowMain%29&sr=-1&p={0}&ps=50&js=var%20SVNsQJPa={1}&token=894050c76af8597a853f5b408b759f5d&sty=DCFFITABK&rt=48583857".format(i,'{pages:%28pc%29,data:[%28x%29]}')
            print (url)
            r=requests.get(url)
            r=r.text
            r=_handle_cashflow(r)
            df=pd.read_csv(StringIO(r),header=None)
            Darr=Darr.append(df)

        Darr.columns=REPORT_COLS1
        Darr.drop_duplicates(subset='mark',inplace=True)
        Darr=Darr.sort_values(by='main_buy',ascending=False)
        Darr=Darr.set_index('mark')
        del Darr['N1']
        Darr=Darr.sort_values(by='pchg',ascending=False)
        return Darr
    except Exception as e:
        print(e)

def get_all_list():
    """
    获取所有股票的现金流情况
    """
    Darr=pd.DataFrame()
    try:
        for i in range(1,2,1):
            url="http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=%28BalFlowMain%29&sr=-1&p={0}&ps=100000&js=var%20uywRInNK={1}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA&rt=4858136".format(i,'{pages:%28pc%29,date:%222014-10-22%22,data:[%28x%29]}')
            print (url)
            r=requests.get(url)
            r=r.text
            r=_handle_cashflow(r)
            df=pd.read_csv(StringIO(r),header=None,encoding='utf8')
            Darr=Darr.append(df)
            time.sleep(0.01)
        Darr.columns=SH_COLS
        Darr.drop_duplicates(subset='code',inplace=True)
        Darr['code']=Darr['code'].map(lambda x:str(x).zfill(6))
        Darr=Darr.set_index('code')
        Darr['date']=pd.to_datetime(Darr['date'])
        del Darr['N1']
        
        return Darr
    except Exception as e:
        print(e)

def _handle_usa(r):
    r=r.split("={rank:[",1)[1]
    r=r.replace('],pages:1}','')
    r=r.replace('",','\n')
    r=r.replace('"','')
    #r=r.decode('gb18030')
    return r

def get_usa_list():
    """
    获取美股股票信息流情况
    """
    Darr=pd.DataFrame()
    try:
        for i in range(1,3,1):
            url="http://hq2gjgp.eastmoney.com/EM_Quote2010NumericApplication/Index.aspx?jsName=UsStockJs&dataName=rank&Type=s&style=70&sortType=C&sortRule=-1&page={0}&pageSize=50000&_g=0.297812950635049".format(i)
            print (url)
            r=requests.get(url)
            r=r.text
            r=_handle_usa(r)
            dd=pd.read_csv(StringIO(r),header=None)
            Darr=Darr.append(dd)
        #"""
        Darr=Darr.drop(0,axis=1)
        Darr=Darr.drop(8,axis=1)
        Darr=Darr.drop(12,axis=1)
        Darr=Darr.drop(14,axis=1)
        Darr=Darr.drop(15,axis=1)
        Darr=Darr.drop(16,axis=1)
        Darr=Darr.drop(19,axis=1)
        Darr=Darr.drop(20,axis=1)
        Darr=Darr.drop(26,axis=1)
        Darr=Darr.drop(27,axis=1)
        Darr=Darr.drop(29,axis=1)
        Darr=Darr.drop(32,axis=1)
        #"""
        Darr.columns=REPORT_usa1
        for label in REPORT_usa2:
            try:
                Darr[label]=Darr[label].astype(float)
            except:
                pass
        #print Darr
        for label in ['code','name','time']:
            Darr[label]=Darr[label].astype(str)
        Darr['only']=Darr['code']+Darr['time']
        Darr=Darr.drop_duplicates(subset=['only'])
        del Darr['only']
        return Darr
    except Exception as e:
        print(e)
        
def _handle_index(r):
    r=r.split("quotation:[",1)[1]
    r=r.replace(']}','')
    r=r.replace('",','\n')
    r=r.replace('"','')
    #r=r.decode('gb18030')
    r=r.replace("%",'')
    return r
def _hapd(dd):
    dd=dd.drop(0,axis=1)
    dd=dd.drop(8,axis=1)
    dd=dd.drop(9,axis=1)
    dd=dd.drop(12,axis=1)
    dd=dd.drop(14,axis=1)
    dd=dd.drop(15,axis=1)
    dd=dd.drop(16,axis=1)
    dd=dd.drop(17,axis=1)
    dd=dd.drop(22,axis=1)
    dd=dd.drop(18,axis=1)
    dd=dd.drop(19,axis=1)
    dd=dd.drop(20,axis=1)
    dd=dd.drop(21,axis=1)
    dd=dd.drop(23,axis=1)
    dd=dd.drop(24,axis=1)
    dd=dd.drop(25,axis=1)
    dd=dd.drop(26,axis=1)
    dd=dd.drop(27,axis=1)
    dd=dd.drop(29,axis=1)
    dd=dd.drop(30,axis=1)
    dd=dd.drop(31,axis=1)
    dd=dd.drop(32,axis=1)
    dd.columns=REPORT_index1
    for label in REPORT_index2:
        dd[label]=dd[label].astype(float)
    #print Darr
    for label in ['code','name','time']:
        dd[label]=dd[label].astype(str)
    dd['only']=dd['code']+dd['time']
    dd=dd.drop_duplicates(subset=['only'])
    del dd['only']
    return dd

def get_global_index():
    """
    获取全球股指数据情况
    """
    #Darr=pd.DataFrame()
    try:
        url="http://hq2gjgp.eastmoney.com/EM_Quote2010NumericApplication/Index.aspx?reference=rtj&Type=Z&jsName=quote_global&ids=NKY7,KOSPI7,FSSTI7,TWSE7,SENSEX7,JCI7,VNINDEX7,FBMKLC7,SET7,KSE1007,PCOMP7,CSEALL7,AS517,NZSE50FG7,CASE7,INDU7,SPX7,CCMP7,SPTSX7,MEXBOL7,IBOV7,UKX7,DAX7,CAC7,IBEX7,FTSEMIB7,AEX7,SMI7,OMX7,ICEXI7,ISEQ7,INDEXCF7,ASE7,BEL207,LUXXX7,KFX7,HEX7,OBX7,ATX7,WIG7,PX7"
        print (url)
        r=requests.get(url)
        r=r.text
        r=_handle_index(r)
        dd=pd.read_csv(StringIO(r),header=None,encoding='utf8')
        dd=_hapd(dd)
        dd=dd.set_index('code')
        return dd
    except Exception as e:
        print(e)

def get_mainland_index():
    """
    获大陆股指情况
    """
    #Darr=pd.DataFrame()
    try:
        url="http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/Index.aspx?type=z&jsName=quote_hs&reference=rtj&ids=0000011,3990012,0003001,3990052,3990062"
        print (url)
        r=requests.get(url)
        r=r.text
        r=_handle_index(r)
        dd=pd.read_csv(StringIO(r),header=None,encoding='utf8')
        dd=_hapd(dd)
        dd['code']=dd['code'].map(lambda x: str(x).zfill(6))
        dd=dd.set_index('code')
        return dd
    except Exception as e:
        print(e)
def get_hongkong_index():
    #Darr=pd.DataFrame()
    try:
        url="http://hq2hk.eastmoney.com/EM_Quote2010NumericApplication/Index.aspx?reference=rtj&Type=z&jsName=quote_hk&ids=1100005,1100105,1100305,1100505"
        print (url)
        r=requests.get(url)
        r=r.text
        r=_handle_index(r)
        dd=pd.read_csv(StringIO(r),header=None,encoding='utf8')
        dd=_hapd(dd)
        dd=dd.set_index('code')
        return dd
    except Exception as e:
        print(e)

def _handle_hk_ha(r):
    r=r.split("rank:[",1)[1]
    r=r.split(",pages",1)[0]
    r=r.replace('",','\n')
    r=r.replace('"','\n')
    r=r.replace(']','')
    try:
        r=r.encode('utf8')
    except Exception as e:
        print (e)
    return r

def get_ha_trading_data():
    url='http://hqguba1.eastmoney.com/hk_ah/AHQuoteList.aspx?jsName=quote_data1&page=1&pageSize=10000&sortType=7&sortRule=-1&_g=0.33073830841158103'
    r=requests.get(url=url,timeout=10)
    r=r.text
    r=_handle_hk_ha(r)

    df=pd.read_csv(StringIO(r),header=None)
    df.columns=TRD_COLS
    df['symbol']=df['symbol'].map(lambda x: str(x).zfill(5))
    df['code']=df['code'].map(lambda x: str(x).zfill(6))
    df=df.set_index('symbol')
    return df

def _handle_hgt(r):
    r=r.text
    r=r.split("data:[",1)[1]
    r=r.replace(']}','')
    r=r.replace('",','\n')
    r=r.replace('"','')
    dft=pd.read_csv(StringIO(r),header=None,encoding='utf8')
    dft.columns=REPORT_hgt
    dft=dft.set_index('date')
    del dft['N_O']
    return dft

def get_hhist_data():
    try:
        for i in range(1,2,1):
            url="http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SHT&sty=SHTHPS&st=2&sr=-1&p={0}&ps=30&js=var%20jSKwIjoM={1}&mkt=1&rt=48579990".format(i,'{pages:%28pc%29,data:[%28x%29]}')
            print (url)
            r=requests.get(url)
            df=_handle_hgt(r)
        return df
    except Exception as e:
        print(e)
        
def get_ghist_data():
    try:
        for i in range(1,2,1):
            url="http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SHT&sty=SHTHPS&st=2&sr=-1&p={0}&ps=30&js=var%20Zqpsgzqk={1}&mkt=2&rt=48579996".format(i,'{pages:%28pc%29,data:[%28x%29]}')
            print (url)
            r=requests.get(url)
            df=_handle_hgt(r)
        return df
    except Exception as e:
        print(e)

def get_hbf_t(year,qu):
    
    """
    http://data.eastmoney.com/zlsj/qfii.html
    ----------------------------------------------
    机构持股分析
    date format like YYYY-MM,string format.
    """
    _write_head()
    DataArr=pd.DataFrame()
    date=quarter[qu]%year
    
    qf='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=ZLSJ&sty=ZLCC&st=2&sr=-1&p=1&ps=50000000&js=var%20sAenYaSr={0}&stat=2&cmd=1&fd={1}&rt=48822247'.format('{pages:%28pc%29,data:[%28x%29]}',date)
    ss='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=ZLSJ&sty=ZLCC&st=2&sr=-1&p=1&ps=50000000&js=var%20tjesHrgl={0}&stat=3&cmd=1&fd={1}&rt=48822242'.format('{pages:%28pc%29,data:[%28x%29]}',date)
    qs='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=ZLSJ&sty=ZLCC&st=2&sr=-1&p=1&ps=50000000&js=var%20ZmVPrQMu={0}&stat=4&cmd=1&fd={1}&rt=48822240'.format('{pages:%28pc%29,data:[%28x%29]}',date)
    bx='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=ZLSJ&sty=ZLCC&st=2&sr=-1&p=1&ps=50000000&js=var%20UPTprWza={0}&stat=5&cmd=1&fd={1}&rt=48822239'.format('{pages:%28pc%29,data:[%28x%29]}',date)
    xt='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=ZLSJ&sty=ZLCC&st=2&sr=-1&p=1&ps=50000000&js=var%20GCanMloZ={0}&stat=6&cmd=1&fd={1}&rt=48822237'.format('{pages:%28pc%29,data:[%28x%29]}',date)
    jj='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=ZLSJ&sty=ZLCC&st=2&sr=-1&p=1&ps=50000000&js=var%20yhahtDLE={0}&stat=1&cmd=1&fd={1}&rt=48822134'.format('{pages:%28pc%29,data:[%28x%29]}',date)

    lists=[jj,qf,ss,qs,bx,xt]
    t=1
    for i in lists:
        _write_console()
        #print i
        r=requests.get(url=i,timeout=10)
        r=r.text
        r=r.split('data:[',1)[1]
        r=r.replace('",','\n')
        r=r.replace('"','')
        r=r.replace(']}','')
        df=pd.read_csv(StringIO(r),header=None)
        df.columns=['code','name','funds','totals_hbf','tv_hbf/pc_ts','position','ch_amount','ch_percent','date']
        df['ftype']=t
        t=t+1
        DataArr=DataArr.append(df)
    for label in ['totals_hbf','tv_hbf/pc_ts','ch_amount','ch_percent']:
        DataArr[label]=DataArr[label].astype(float)
    DataArr['code']=DataArr['code'].map(lambda x: str(x).zfill(6))
    return DataArr

def get_hbf_d(code,year,qu):
    """
    date like YYYY-MM,string format.
    code is the sharecode listed in shanghai or shenzhen
    """
    date=quarter[qu]%year

    url='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=ZLSJ&sty=CCJGMX&st=2&sr=-1&p=1&ps=30000000&js=var%20IuLulRvA={0}&stat=0&code={1}&fd={2}&rt=48822187'.format('{pages:%28pc%29,data:[%28x%29]}',code,date)
    r=requests.get(url=url,timeout=10)
    r=r.text
    r=r.split('data:[',1)[1]
    r=r.replace('",','\n')
    r=r.replace('"','')
    r=r.replace(']}','')
    df=pd.read_csv(StringIO(r),header=None)
    df.columns=['code','name','fcode','fname','type','totals_hbf','tv_hbf','percent_total_shares','percent_current_shares','date']
    df['code']=df['code'].map(lambda x: str(x).zfill(6))
    df['fcode']=df['fcode'].map(lambda x: str(x).zfill(6))
    for label in ['totals_hbf','tv_hbf','percent_total_shares','percent_current_shares']:
        df[label]=df[label].astype(float)
    return df

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

def get_cashflow_emnow():
    """
    Parameters:
    ----------------------------
    return:
          DataFrame:
              code:     股票代码,
              name：    股票名称
              price：   最新价格
              change：  涨跌幅度
              zl_netin：主力净流入净额（万元）
              pc_zl：   主力净流入净占比（%）
              sp_netin：超大单净流入净额（万元）
              pc_sp：   超大单净流入净占比（%）
              b_netin： 大单净流入净额（万元
              pc_b：    大单净流入净占比（%）
              m_netin： 中单净流入净额（万元）
              pc_m：    中单净流入净占比（%）
              sm_netin：小单净流入净额（万元）',
              pc_sm：   小单净流入净占比（%）
              date：    获取数据时间
    """
    url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMain)&sr=-1&p=1&ps=500000&js=var%20xdBNZpGl={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA&rt=49167709'
    r=requests.get(url)
    r=r.text
    r=r.split('data:[')[1]
    r=r.replace('"]}','')
    r=r.replace('",','\n')
    r=r.replace('"','')
    r=r.replace('-,',',')
    df=pd.read_csv(StringIO(r),header=None)
    df=df.drop(0,axis=1)
    df.columns=['code','name','price','change','zl_netin','pc_zl','sp_netin','pc_sp','b_netin','pc_b','m_netin','pc_m','sm_netin','pc_sm','date']
    df.code=df.code.map(lambda x:str(x).zfill(6))
    df=df.set_index('code')
    for label in ['price','change','zl_netin','pc_zl','sp_netin','pc_sp','b_netin','pc_b','m_netin','pc_m','sm_netin','pc_sm']:
        df[label]=df[label].astype(float)
    return df

def get_cashflow_em3days():
    """
    Parameters:
    ----------------------------
    return:
          DataFrame:
              code:     股票代码,
              name：    股票名称
              price：   最新价格
              change：  涨跌幅度
              zl_netin：主力净流入净额（万元）
              pc_zl：   主力净流入净占比（%）
              sp_netin：超大单净流入净额（万元）
              pc_sp：   超大单净流入净占比（%）
              b_netin： 大单净流入净额（万元
              pc_b：    大单净流入净占比（%）
              m_netin： 中单净流入净额（万元）
              pc_m：    中单净流入净占比（%）
              sm_netin：小单净流入净额（万元）',
              pc_sm：   小单净流入净占比（%）
              date：    获取数据时间
    """
    url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMainNet3)&sr=-1&p=1&ps=50000&js=var%20JbHilIth={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA3&rt=49167722'
    r=requests.get(url)
    r=r.text
    r=r.split('data:[')[1]
    r=r.replace('"]}','')
    r=r.replace('",','\n')
    r=r.replace('"','')
    r=r.replace('-,',',')
    df=pd.read_csv(StringIO(r),header=None)
    df=df.drop(0,axis=1)
    df.columns=['code','name','price','change','zl_netin','pc_zl','sp_netin','pc_sp','b_netin','pc_b','m_netin','pc_m','sm_netin','pc_sm','date']
    df.code=df.code.map(lambda x:str(x).zfill(6))
    df=df.set_index('code')
    for label in ['price','change','zl_netin','pc_zl','sp_netin','pc_sp','b_netin','pc_b','m_netin','pc_m','sm_netin','pc_sm']:
        df[label]=df[label].astype(float)
    return df

def get_cashflow_em5days():
    """
    Parameters:
    ----------------------------
    return:
          DataFrame:
              code:     股票代码,
              name：    股票名称
              price：   最新价格
              change：  涨跌幅度
              zl_netin：主力净流入净额（万元）
              pc_zl：   主力净流入净占比（%）
              sp_netin：超大单净流入净额（万元）
              pc_sp：   超大单净流入净占比（%）
              b_netin： 大单净流入净额（万元
              pc_b：    大单净流入净占比（%）
              m_netin： 中单净流入净额（万元）
              pc_m：    中单净流入净占比（%）
              sm_netin：小单净流入净额（万元）',
              pc_sm：   小单净流入净占比（%）
              date：    获取数据时间
    """
    url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMainNet5)&sr=-1&p=1&ps=50000&js=var%20NHMvtYjS={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA5&rt=49167724'
    r=requests.get(url)
    r=r.text
    r=r.split('data:[')[1]
    r=r.replace('"]}','')
    r=r.replace('",','\n')
    r=r.replace('"','')
    r=r.replace('-,',',')
    df=pd.read_csv(StringIO(r),header=None)

    df=df.drop(0,axis=1)
    df.columns=['code','name','price','change','zl_netin','pc_zl','sp_netin','pc_sp','b_netin','pc_b','m_netin','pc_m','sm_netin','pc_sm','date']
    df.code=df.code.map(lambda x:str(x).zfill(6))
    df=df.set_index('code')
    for label in ['price','change','zl_netin','pc_zl','sp_netin','pc_sp','b_netin','pc_b','m_netin','pc_m','sm_netin','pc_sm']:
        df[label]=df[label].astype(float)
    return df

def get_cashflow_em10days():
    """
    Parameters:
    ----------------------------
    return:
          DataFrame:
              code:     股票代码,
              name：    股票名称
              price：   最新价格
              change：  涨跌幅度
              zl_netin：主力净流入净额（万元）
              pc_zl：   主力净流入净占比（%）
              sp_netin：超大单净流入净额（万元）
              pc_sp：   超大单净流入净占比（%）
              b_netin： 大单净流入净额（万元
              pc_b：    大单净流入净占比（%）
              m_netin： 中单净流入净额（万元）
              pc_m：    中单净流入净占比（%）
              sm_netin：小单净流入净额（万元）',
              pc_sm：   小单净流入净占比（%）
              date：    获取数据时间
    """
    url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx/JS.aspx?type=ct&st=(BalFlowMainNet10)&sr=-1&p=1&ps=50000&js=var%20oeyEkNty={pages:(pc),date:%222014-10-22%22,data:[(x)]}&token=894050c76af8597a853f5b408b759f5d&cmd=C._AB&sty=DCFFITA10&rt=49167726'
    r=requests.get(url)
    r=r.text
    r=r.split('data:[')[1]
    r=r.replace('"]}','')
    r=r.replace('",','\n')
    r=r.replace('"','')
    r=r.replace('-,',',')
    df=pd.read_csv(StringIO(r),header=None)
    df=df.drop(0,axis=1)
    df.columns=['code','name','price','change','zl_netin','pc_zl','sp_netin','pc_sp','b_netin','pc_b','m_netin','pc_m','sm_netin','pc_sm','date']
    df.code=df.code.map(lambda x:str(x).zfill(6))
    df=df.set_index('code')
    for label in ['price','change','zl_netin','pc_zl','sp_netin','pc_sp','b_netin','pc_b','m_netin','pc_m','sm_netin','pc_sm']:
        df[label]=df[label].astype(float)
    return df

def get_cashflow_emshare(code):
    """
    Parameters:
          code: 股票代码,like 600422
    ----------------------------
    return:
          DataFrame:
              code:     股票代码,
              name：    股票名称
              price：   最新价格
              change：  涨跌幅度
              zl_netin：主力净流入净额（万元）
              pc_zl：   主力净流入净占比（%）
              sp_netin：超大单净流入净额（万元）
              pc_sp：   超大单净流入净占比（%）
              b_netin： 大单净流入净额（万元
              pc_b：    大单净流入净占比（%）
              m_netin： 中单净流入净额（万元）
              pc_m：    中单净流入净占比（%）
              sm_netin：小单净流入净额（万元）',
              pc_sm：   小单净流入净占比（%）
              date：    获取数据时间
    """
    url='http://data.eastmoney.com/zjlx/%s.html'%code
    r=requests.get(url)
    r=r.content.decode('gb2312')
    html = lxml.html.parse(StringIO(r))
    res = html.xpath("//table[@id='dt_1']/tbody/tr")
    if PY3:
        sarr = [etree.tostring(node).decode('utf-8') for node in res]
    else:
        sarr = [etree.tostring(node) for node in res]
    sarr = ''.join(sarr)
    sarr = '<table>%s</table>'%sarr
    df = pd.read_html(sarr)[0]
    df.columns=['date','price','change','zl_netin','pc_zl','sp_netin','pc_sp','b_netin','pc_b','m_netin','pc_m','sm_netin','pc_sm']
    df=df.set_index('date')
    for label in    ['change','zl_netin','pc_zl','sp_netin','pc_sp','b_netin','pc_b','m_netin','pc_m','sm_netin','pc_sm']:
        #for label in ['zl_netin','sp_netin','b_netin','m_netin','sm_netin']:
        df[label]=df[label].map(lambda x: _str2fl(x))
    return df



    

def get_dividen_allshare_EM(year,qu):
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
    date=quarter[qu]%year
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
    df=df.replace('-',np.nan)
    df=df.applymap(lambda x: _str2fl(x))
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
    df=df.replace('-',np.nan)
    df=df.applymap(lambda x: _str2fl(x))
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
    df=df.replace('-',np.nan)
    df=df.applymap(lambda x: _str2fl(x))    
    return df

def _jjcg(date):
    """
    http://data.eastmoney.com/zlsj/jj.html
    -------------------------------------
    Parameter:
          date: string,like 2016-12-31
    --------------------------
    Return:
          DataFrame:
                  CGChange: 持股变动情况,
                  Count：持有QFII家数(家)
                  LTZB', 
                  LX',
                  LXDM：机构类型
                  RDate', 
                  RateChange：持股变动比例(%)
                  SCode：股票代码
                  SName：股票名称
                  ShareHDNum：持股总数(股) 
                  ShareHDNumChange：持股变动数值(股)	
                  TabRate：占总股本比例(%)
                  VPosition：持股市值(元)
    """
    url='http://data.eastmoney.com/zlsj/zlsj_list.aspx?type=ajax&st=2&sr=-1&p=1&ps=50000000&jsObj=IWmRaQlL&stat=1&cmd=1&date={0}&rt=49825002'.format(date)#基金持股
    html=requests.get(url)
    text=html.text
    text=text.split("IWmRaQlL =")[1]
    text=text.split(',dataUrl:')[0]
    text=text.replace('pages','"pages"')
    text=text.replace('data','"data"')
    text=text+'}'
    #text=text.replace('dataUrl','"dataUrl"')
    data=json.loads(text)
    div=data['data']
    df=pd.DataFrame(div)
    names=['Count', 'LTZB', 'LX', 'RateChange', 'ShareHDNum',\
           'ShareHDNumChange', 'TabRate', 'VPosition']
    for label in names:
        df[label]=df[label].astype(float)
    
    return df

def _qfllcg(date):
    """
    http://data.eastmoney.com/zlsj/jj.html
    -------------------------------------
    Parameter:
          date: string,like 2016-12-31
    --------------------------
    Return:
          DataFrame:
                  CGChange: 持股变动情况,
                  Count：持有QFII家数(家)
                  LTZB', 
                  LX',
                  LXDM：机构类型
                  RDate', 
                  RateChange：持股变动比例(%)
                  SCode：股票代码
                  SName：股票名称
                  ShareHDNum：持股总数(股) 
                  ShareHDNumChange：持股变动数值(股)	
                  TabRate：占总股本比例(%)
                  VPosition：持股市值(元)
    """    
    url='http://data.eastmoney.com/zlsj/zlsj_list.aspx?type=ajax&st=2&sr=-1&p=1&ps=50000000&jsObj=JYNvFVcs&stat=2&cmd=1&date={0}&rt=49825012'.format(date)#Qfll
    #持股
    html=requests.get(url)
    text=html.text
    text=text.split("YNvFVcs = ")[1]
    text=text.split(',dataUrl:')[0]
    text=text.replace('pages','"pages"')
    text=text.replace('data','"data"')
    text=text+'}'
    data=json.loads(text)
    div=data['data']
    df=pd.DataFrame(div)
    names=['Count', 'LTZB', 'LX','RateChange', 'ShareHDNum',\
           'ShareHDNumChange', 'TabRate', 'VPosition']
    for label in names:
        df[label]=df[label].astype(float)    
    return df

def _hbcg(date):
    """
    http://data.eastmoney.com/zlsj/jj.html
    社保持股情况
    -------------------------------------
    Parameter:
          date: string,like 2016-12-31
    --------------------------
    Return:
          DataFrame:
                  CGChange: 持股变动情况,
                  Count：持有QFII家数(家)
                  LTZB', 
                  LX',
                  LXDM：机构类型
                  RDate', 
                  RateChange：持股变动比例(%)
                  SCode：股票代码
                  SName：股票名称
                  ShareHDNum：持股总数(股) 
                  ShareHDNumChange：持股变动数值(股)	
                  TabRate：占总股本比例(%)
                  VPosition：持股市值(元)
    """    
    url='http://data.eastmoney.com/zlsj/zlsj_list.aspx?type=ajax&st=2&sr=-1&p=1&ps=50000000&jsObj=bhRLTSOI&stat=3&cmd=1&date={0}&rt=49825041'.format(date)
    html=requests.get(url)
    text=html.text
    text=text.split("bhRLTSOI = ")[1]
    text=text.split(',dataUrl:')[0]
    text=text.replace('pages','"pages"')
    text=text.replace('data','"data"')
    text=text+'}'
    data=json.loads(text)
    div=data['data']
    df=pd.DataFrame(div)
    names=['Count', 'LTZB', 'LX', 'RateChange', 'ShareHDNum',\
           'ShareHDNumChange', 'TabRate', 'VPosition']
    for label in names:
        df[label]=df[label].astype(float)
    return df

def _qscg(date):
    """
    券商持股情况
    ---------------------------------
    Parameter:
          date: string,like 2016-12-31
    --------------------------
    Return:
          DataFrame:
                  CGChange: 持股变动情况,
                  Count：持有QFII家数(家)
                  LTZB', 
                  LX',
                  LXDM：机构类型
                  RDate', 
                  RateChange：持股变动比例(%)
                  SCode：股票代码
                  SName：股票名称
                  ShareHDNum：持股总数(股) 
                  ShareHDNumChange：持股变动数值(股)	
                  TabRate：占总股本比例(%)
                  VPosition：持股市值(元)
    """
    url='http://data.eastmoney.com/zlsj/zlsj_list.aspx?type=ajax&st=2&sr=-1&p=1&ps=50000000&jsObj=SKRGEYpf&stat=4&cmd=1&date={0}&rt=49825050'.format(date)
    html=requests.get(url)
    text=html.text
    text=text.split("SKRGEYpf = ")[1]
    text=text.split(',dataUrl:')[0]
    text=text.replace('pages','"pages"')
    text=text.replace('data','"data"')
    text=text+'}'    

    data=json.loads(text)
    div=data['data']
    df=pd.DataFrame(div)
    names=['Count', 'LTZB', 'LX', 'RateChange', 'ShareHDNum',\
           'ShareHDNumChange', 'TabRate', 'VPosition']
    for label in names:
        df[label]=df[label].astype(float)    
    return df

def _bxcg(date):
    """
    保险持股情况
    ------------------------
    Parameter:
          date: string,like 2016-12-31
    --------------------------
    Return:
          DataFrame:
                  CGChange: 持股变动情况,
                  Count：持有QFII家数(家)
                  LTZB', 
                  LX',
                  LXDM：机构类型
                  RDate', 
                  RateChange：持股变动比例(%)
                  SCode：股票代码
                  SName：股票名称
                  ShareHDNum：持股总数(股) 
                  ShareHDNumChange：持股变动数值(股)	
                  TabRate：占总股本比例(%)
                  VPosition：持股市值(元)
    """
    url='http://data.eastmoney.com/zlsj/zlsj_list.aspx?type=ajax&st=2&sr=-1&p=1&ps=50000000&jsObj=RYWOKLru&stat=5&cmd=1&date={0}&rt=49825064'.format(date)
    html=requests.get(url)
    text=html.text
    text=text.split("RYWOKLru = ")[1]
    text=text.split(',dataUrl:')[0]
    text=text.replace('pages','"pages"')
    text=text.replace('data','"data"')
    text=text+'}'    

    data=json.loads(text)
    div=data['data']
    df=pd.DataFrame(div)
    names=['Count', 'LTZB', 'LX', 'RateChange', 'ShareHDNum',\
           'ShareHDNumChange', 'TabRate', 'VPosition']
    for label in names:
        df[label]=df[label].astype(float)    
    return df

def _xtcg(date):
    """
    信托持股情况
    ------------------------
    Parameter:
          date: string,like 2016-12-31
    --------------------------
    Return:
          DataFrame:
                  CGChange: 持股变动情况,
                  Count：持有QFII家数(家)
                  LTZB', 
                  LX',
                  LXDM：机构类型
                  RDate', 
                  RateChange：持股变动比例(%)
                  SCode：股票代码
                  SName：股票名称
                  ShareHDNum：持股总数(股) 
                  ShareHDNumChange：持股变动数值(股)	
                  TabRate：占总股本比例(%)
                  VPosition：持股市值(元)
    """
    url='http://data.eastmoney.com/zlsj/zlsj_list.aspx?type=ajax&st=2&sr=-1&p=1&ps=50000000&jsObj=yZbUvvlr&stat=6&cmd=1&date={0}&rt=49825070'.format(date)
    html=requests.get(url)
    text=html.text
    text=text.split("yZbUvvlr = ")[1]
    text=text.split(',dataUrl:')[0]
    text=text.replace('pages','"pages"')
    text=text.replace('data','"data"')
    text=text+'}'    
    data=json.loads(text)
    div=data['data']
    df=pd.DataFrame(div)
    names=['Count', 'LTZB', 'LX', 'RateChange', 'ShareHDNum',\
           'ShareHDNumChange', 'TabRate', 'VPosition']
    for label in names:
        df[label]=df[label].astype(float)    
    return df    

def holdby_total(date='2017-03-31'):
    """
    机构持股变动情况
    http://data.eastmoney.com/zlsj/jj.html
    -------------------------------------
    Parameter:
          date: string,like 2016-12-31
    --------------------------
    Return:
          DataFrame:
                  CGChange: 持股变动情况,
                  Count：持有QFII家数(家)
                  LTZB', 
                  LX',
                  LXDM：机构类型
                  RDate', 
                  RateChange：持股变动比例(%)
                  SCode：股票代码
                  SName：股票名称
                  ShareHDNum：持股总数(股) 
                  ShareHDNumChange：持股变动数值(股)	
                  TabRate：占总股本比例(%)
                  VPosition：持股市值(亿元)
    
    """
    jj=_jjcg(date)
    qf=_qfllcg(date)
    hb=_hbcg(date)
    qs=_qscg(date)
    bx=_bxcg(date)
    xt=_xtcg(date)
    df=[jj,qf,hb,qs,bx,xt]
    df=pd.concat(df,axis=0)
    
    df['RDate'] = df['RDate'].map(lambda x: _totime(x))
    return df
    
def holdby_detail(code,date='2016-12-31'):
    """
    某只股票的在季度末时，机构持有的数量情况。
    http://data.eastmoney.com/zlsj/detail/2017-03-31-2-600132.html
    -----------------------------------------
    Parameter:
             code, string,在深圳和上海交易所的股票代码。
             date, string,like 2016-12-31、03-31,06-30,09-30
    ---------------------------------------
    Return:
          DataFrame:    
              BuyState:  买入状况
              IndtCode：基金机构代码
              InstSName：基金机构名称
              RDate：持有披露时间
              SCode：股票代码
              SHCode：机构代码
              SHName：机构名称
              SName：股票名称
              ShareHDNum：持股总数(股)
              TabProRate：占总股本比例(%)
              TabRate：占流通股本比例(%)
              Type：机构属性
              TypeCode：机构代码
              Vposition：持股市值(元)
    """
    url='http://data.eastmoney.com/zlsj/detail.aspx?type=ajax&st=2&sr=-1&p=1&ps=3000&jsObj=iiaMClTz&stat=0&code={0}&date={1}&rt=49825193'.format(code,date)
    html=requests.get(url)
    text=html.text
    text=text.split("iiaMClTz = ")[1]
    text=text.split(',dataUrl:')[0]
    text=text.replace('pages','"pages"')
    text=text.replace('data','"data"')
    text=text+'}'    
    data=json.loads(text)
    div=data['data']
    df=pd.DataFrame(div)
    names=['ShareHDNum', 'TabProRate', 'TabRate', 'Vposition']
    for label in names:
        df[label]=df[label].astype(float)
    df['RDate'] = df['RDate'].map(lambda x: _totime(x))
    return df
    
def controller_increase():
    """
    查阅控股股东增减持情况
    http://data.eastmoney.com/executive/gdzjc.html
    -------------------------------------
    Return：
      DataFrame：
      -------------------------
        code:股票代码
        name 股票名称
        close: 最新价
        pchg: 涨跌幅
        holder_name:股东名称
        zj：增减持
        sl：持股变动变动数量（万股）
        zlbl：占流通股比例（%）
        zcly：持股变动来源（二级、增发）
        cgzs：变动后持股持股总数（万股）
        zbl： 变动后持股占总股本比例（%）
        cltgsl：变动后持股持流通股数量（万股）
        zltbl：变动后持股占流通股比例
        bdrq：开始变动日
        bdjzr：变动截止日
        ggr：公告日
        zzgbbl:持股变动占总股本的比例（%）
    """
    i=1
    Df=pd.DataFrame()
    while True:
        try:
            url='http://data.eastmoney.com/DataCenter_V3/gdzjc.ashx?pagesize=5000&page={0}&js={1}=&sortRule=-1&sortType=BDJZ&tabid=all&code=&name=&rt=49887843'.format(i,'var%20vwDvQnNt&param')
            print(url)
            r=requests.get(url,headers=hds())
            text=r.text
            text=text.split('data:[')[1]
            text=text.split('] ,')[0]
            text=text.replace('",','"\n')
            text=text.replace('"','')
            df=pd.read_csv(StringIO(text),header=None)
            Df=Df.append(df)
            i += 1
        except Exception as e:
            print(e)
            break
    name=['code','name','close','pchg','holder_name','zj','sl','zlbl','zcly','cgzs','zbl','cltgsl','zltbl','bdrq','bdjzr','ggr','zzgbbl']
    Df.columns=name
    return Df
    
    
def _str2fl(x):
    try:
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
        else:
            x=float(x)
        return x
    except:
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
