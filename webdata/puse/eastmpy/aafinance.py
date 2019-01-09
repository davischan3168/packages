#!/usr/bin/env python3
# -*-coding:utf-8-*-

import pandas as pd
import numpy as np
import sys,requests,os
import lxml.html
from lxml import etree
import json
import re,time
import datetime as dt
from webdata.util.hds import user_agent as hds
from io import StringIO
from bs4 import BeautifulSoup
import webdata.puse.eastmpy.cont as wt

bsname={'ch':'存货(元)', 'chdjzb':'存货跌价准备(元)', 'cqfzhj':'长期负债合计(元)',
        'cqgqtz':'长期股权投资(元)', 'fzhj':'负债合计(元)', 'gdqyhj':'股东权益合计(元)',
        'gdzc':'固定资产(元)', 'hbzj':'货币资金(元)',
       'ldbl':'流动比率', 'ldfzhj':'流动负债合计(元)',
        'ldzchj':'流动资产合计(元)', 'ljzj':'累计折旧(元)',
        'qtysk':'其它应收款(元)', 'sszb':'负债合计(元)', 'wxzc':'无形资产(元)',
        'yfzk':'应付账款(元)','yszk':'应收账款(元)', 'yszk1':'预收账款(元)',
        'yygjj':'盈余公积金金(元)', 'zbgjj':'资本公积金(元)', 'zczj':'资产总计(元)'}

incname={'cwfy':'财务费用(元)', 'glfy':'管理费用(元)', 'gsmgssyzjlr':'归属母公司所有者净利润(元)', 'lrze':'利润总额(元)', 'sds':'所得税(元)', 'tzsy':'投资收益(元)', 'xsfy':'销售费用(元)', 'yycb':'营业成本(元)',
       'yylr':'营业利润(元)', 'yysr':'营业收入(元)', 'zcjzss':'资产减值损失(元)'}

cfname={'chzwzfdxj':'偿还债务支付的现金(元)', 'czhdcsdxjllje':'筹资活动产生的现金流量净额(元)',
     'czhdxjlcxj':'筹资活动现金流出小计(元)', 'czhdxjlrxj':'筹资活动现金流入小计(元)',
     'fpzfdxj':'分配股利、利润或偿付利息支付的现金(元)',
     'gmspjslwzfdxj':'购买商品、接受劳务支付的现金(元)', 'jyhdcsdxjllje':'经营活动产生的现金流量净额(元)', 'jyhdxjlcxj':'经营活动现金流出小计(元)', 'jyhdxjlrxj':' 经营活动现金流入小计(元)',
    'qdjksddxj':'取得借款收到的现金(元)', 'qdtzsyssddxj':'投资:取得投资收益所收到的现金(元)',
    'sddsffh':'收到的税费返还(元)',
     'sddxj':'经营:销售商品、提供劳务收到的现金(元)', 'sdqtdxj':'收到其他与经营活动有关的现金(元)',
     'shdxjje':'处置固定资产、无形资产和其他长期资产收回的现金',
    'tzhdcsdxjllje':"投资活动产生的现金流量净额(元)", 'tzhdxjlcxj':'投资活动现金流出小计(元)', 'tzhdxjlrxj':'投资活动现金流入小计(元)', 'tzzfdxj':'投资支付的现金(元)', 'xstzsddxj':'筹资:吸收投资收到的现金(元)',
    'zfdgxsf':'支付的各项税费(元)', 'zfdxj':'购建固定资产、无形资产和其他长期资产支付的现金(元)',
     'zfdxjje':'投资支付的现金(元)', 'zfgzgyjwzgzfdxj':'支付给职工以及为职工支付的现金(元)', 'zfqtyjyhdygdxj':'支付其他与经营活动有关的现金(元)'}
ss=re.compile(r'(-?\d+.?\d*)%')

quarter={1:'%s-03-31',2:'%s-06-30',3:'%s-09-30',4:'%s-12-31'}

f9url={'djzb':'http://soft-f9.eastmoney.com/soft/gp14.php?code={0}&exp=0&tp=',
       'zhzb':'http://soft-f9.eastmoney.com/soft/gp13.php?code={0}&exp=0&tp='}

def get_finance_index_EM(year,qu):
    yq=quarter[qu]%year
    url='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=YJBB&fd=%s&st=13&sr=-1&p=1&ps=5000000'%yq
    #print(url)
    
    r=requests.get(url,headers=hds())
    text=r.text.replace('(["','').replace('"])','')
    text=text.replace('","','\n')
    df=pd.read_csv(StringIO(text),header=None)
    df=df.drop([14,15,18],axis=1)
    df.columns=['code','name','eps','eps_d','rev','rev_yoy','rev_hb','profit','profit_yoy','profit_hb','nav_ps','roe','cf_ps','margin','pulish','report']
    df=df.applymap(lambda x:wt._tofl(x))
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    df=df.set_index('code')
    df=df.replace('-',np.nan)
    return df

def get_forcast_EM(year,qu):
    yq=quarter[qu]%year
    url='http://datainterface.eastmoney.com/EM_DataCenter/JS.aspx?type=SR&sty=YJYG&fd=%s&st=4&sr=-1&p=1&ps=500000'%yq
    #print(url)
    
    r=requests.get(url,headers=hds())
    text=r.text.replace('(["','').replace('"])','')
    text=text.replace('","','\n')
    df=pd.read_csv(StringIO(text),header=None)
    #df=df.drop([14,15,18],axis=1)
    df.columns=['code','name','describe','change_period','type','prof_l','ttype','pulish','date']

    df=df.replace('-',np.nan)
    df['cc']=df['change_period'].map(lambda x:ss.findall(str(x)))
    df['Down']=np.nan
    df['Up']=np.nan
    for i in range(df.shape[0]):
        if len(df.iloc[i,df.columns.get_loc('cc')])==2:
            df.iloc[i,df.columns.get_loc('Down')]=df.iloc[i,df.columns.get_loc('cc')][0]
            df.iloc[i,df.columns.get_loc('Up')]=df.iloc[i,df.columns.get_loc('cc')][1]
        elif len(df.iloc[i,df.columns.get_loc('cc')])==1:
            df.iloc[i,df.columns.get_loc('Down')]=df.iloc[i,df.columns.get_loc('cc')][0]
            df.iloc[i,df.columns.get_loc('Up')]=df.iloc[i,df.columns.get_loc('cc')][0]

    del df['cc']
    df=df[['code','name','change_period','Down','Up','type','prof_l','ttype','describe','pulish','date']]
    df=df.applymap(lambda x:wt._tofl(x))
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    df=df.set_index('code')    
    return df

def get_financeindex_f10_EM(code,mtype=0):
    """
    code:公司的代码
    mtype:0--报告期的数据，1--按年度的报告数据，2--按单季的报告数据
    --------------------------------------------------------------
    return:
       DataFrame
    """

    if code[0] in ['6','9']:
        code='sh'+code
    elif code[0] in ['0','2','3']:
        code='sz'+code
        
    url='http://emweb.securities.eastmoney.com/PC_HSF10/FinanceAnalysis/MainTargetAjax?code={0}&type={1}'.format(code,mtype)

    r=requests.get(url,headers=hds())
    data=json.loads(r.text)
    df=pd.DataFrame(data['Result'])
    df.rename(columns={'chzzts':'存货周转率', 'gsjlr':'归属净利润',\
                       'gsjlrgdhbzz':'归属净利润滚动环比增长%',
                       'gsjlrtbzz':'归属净利润同比增长%', 'jbmgsy':'基本每股收益', 'jll':'净利率',
                       'jqjzcsyl':'加权净资产收益率%',
                       'jyxjlyysr':'经营现金流/营业收入',
                       'kfjlr':'扣非净利润',
                       'kfjlrgdhbzz':'扣除净利润滚动环比增长%', 'kfjlrtbzz':'扣除净利润同比增长%',
                       'kfmgsy':'扣非每股收益', 'ldbl':'流动比率',
                       'ldzczfz':'流动负债/总负债%',
                       'mggjj':'每股净资产','mgjyxjl':'每股经营现金流','mgjzc':'每股净资产',
                       'mgwfply':'每股为分配利润', 'mll':'毛利率%', 'mlr':'毛利润%', 'sdbl':'速动比率', 'sjsl':'实际税负%',
                       'tbjzcsyl':'摊薄净资产收益率%','tbzzcsyl':'摊薄总资产收益率%',
                       'xsmgsy':'稀释每股收益', 'xsxjlyysr':'销售现金流/营业收入', 'yskyysr':'预收款/营业收入',
                       'yszkzzts':'应收账款周转天数',
                       'yyzsr':'营业收入',    'yyzsrgdhbzz':'营业总收入滚动环比增长%',
                       'yyzsrtbzz':'营业总收入同比增长', 'zcfzl':'资产负债率', 'zzczzy':'总资产周转率'},inplace=True)
    df=df.set_index('date')
    df=df.sort_index()
    df=df.T
    return df

def get_bsincf_f10_EM(code,mtype):
    """
    获得报表明细
    """

    if code[0] in ['6','9']:
        code='sh'+code
    elif code[0] in ['0','2','3']:
        code='sz'+code    

    url='http://emweb.securities.eastmoney.com/PC_HSF10/FinanceAnalysis/ReportDetailAjax?code={0}&ctype=0&type={1}'.format(code,mtype)
    #print(url)

    r=requests.get(url,headers=hds())
    data=json.loads(r.text)
    #print(data)
    if mtype in [0,1]:
        inc=pd.DataFrame(data['Result']['lr0'])
        inc=inc.set_index('date')
        cf=pd.DataFrame(data['Result']['xjll0'])
        cf=cf.set_index('date')
        bs=pd.DataFrame(data['Result']['zcfz0'])
        bs=bs.set_index('date')
        bs.rename(columns=bsname,inplace=True)
        inc.rename(columns=incname,inplace=True)
        cf.rename(columns=cfname,inplace=True)
        return bs,inc,cf
    elif mtype == 2:
        inc=pd.DataFrame(data['Result']['lr20'])
        inc=inc.set_index('date')
        cf=pd.DataFrame(data['Result']['xjll20'])
        cf=cf.set_index('date')
        inc.rename(columns=incname,inplace=True)
        cf.rename(columns=cfname,inplace=True)        
        return inc,cf
    elif mtype == 3:
        inc=pd.DataFrame(data['Result']['lr30'])
        inc=inc.set_index('date')
        cf=pd.DataFrame(data['Result']['xjll30'])
        cf=cf.set_index('date')
        inc.rename(columns=incname,inplace=True)
        cf.rename(columns=cfname,inplace=True)        
        return inc,cf
    
def get_financeindex_f9_EM(code,mtype='zhzb'):
    """
    code:公司股票代码
    mtype:类型，有zhzb:按报告期,djzb按单季报告
    """
    if code[0] in ['6','9']:
        code=code+'01'
    elif code[0] in ['0','2','3']:
        code=code+'02'

    url=f9url[mtype].format(code)
    print(url)
    r=requests.get(url,headers=hds())

    text=r.content.decode('utf8')
    soup=BeautifulSoup(text,'lxml')
    tbs=soup.find_all('table')
    df=pd.read_html(str(tbs[0]))[0]
    df.columns=df.iloc[0,:].tolist()
    df=df.drop(0,axis=0)
    df=df.set_index('报告期日期')
    #df=df.applymap(lambda x:wt._tofl(x))
    df=df.dropna(how='all',axis=0)
    df=df.T
    df=df.sort_index()
    return df


    
if __name__=="__main__":
    #df=get_finance_index_EM(2016,2)
    #df=get_forcast_EM(2017,2)
    #df=get_financeindex_f10_EM(sys.argv[1],0)
    #df=get_bsincf_f10_EM(sys.argv[1],1)
    df=get_financeindex_f9_EM(sys.argv[1],'zhzb')
