#!/usr/bin/env python3
# -*-coding:utf-8-*-

import requests,json
from io import StringIO
import re,sys,os
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import lxml.html
from lxml import etree
import datetime as dt
import webdata.puse.qqpy.cont as wt
from webdata.util.hds import user_agent as hds
import datetime as dt
today=dt.datetime.today()
today=today.strftime('%Y%m%d')



def get_preview_qq(code):
    """
    获得公司业绩预增的信息
    """

    url='http://stock.finance.qq.com/corp1/yjyg.php?zqdm={0}'.format(code)
    #print(url)

    r=requests.get(url,headers=hds())
    text=r.content.decode('gbk')

    soup=BeautifulSoup(text,'lxml')
    tables=soup.findAll('table')
    urls=tables[1].findAll('a')
    #print(urls)
    
    tables=[]
    df=pd.DataFrame()
    
    for rl in urls:
        url=rl.get('href')
        #print(url)
        rr=requests.get(url,headers=hds())
        text=rr.content.decode('gbk')

        soup=BeautifulSoup(text,'lxml')
        tbs=soup.findAll('table',attrs={"class":"list list_d"})
        tables.extend(tbs)

    for tb in tables:
        dd=pd.read_html(str(tb))[0]
        dd.columns=dd.iloc[1,0:]
        dd=dd.drop(1,axis=0)
        dd=dd.set_index('报告期')
        #dd=dd.set_index('报告期')
        #print(dd)
        if df.empty:
            df=df.append(dd)
        else:
            try:
                df=pd.concat([df,dd],axis=1)
            except:
                pass
    df=df.T
    
    return df

def get_cwfx_qq(code,mtype='ylnl'):
    """
    从腾讯财务获得相应的 指标
    ---------------------------------------
    code:上海、深圳交易所的股票代码
    mtype: mgzb--每股指标
           ylnl--盈利能力
           yynl--营运能力
           cznl--成长能力
           djcw--单季财务
           czzb--偿债及资本结构
    --------------------------------------------
    return:
         DataFrame:
            ylnl: 
                  cbfylrl:成本费用利润率(%)
                  fjcxsybl:非经常性损益比率(%)
                  jlrkc:扣除非经常性损益后的净利润(元)
                  jzcsyljq:净资产收益率(加权)(%)
                  sxfyl:三项费用率(%)
                  xsjll:销售净利率(%)
                  xsmll:销售毛利率(%)
                  xsqlr:息税前利润(%)
                  xsqlrl:息税前利润率(%) 
                  yylrl:营业利润率(%)
                  zzclrl:总资产利润率(%)
                  ylnlname=['Cost.Profit.R','Net.oper.R','Profit_d','ROE','Three.Cost.R','Profit.R','Gross.Margin.R','Profit_bTax','Profit_rate_bTax','O.Profit.Rate','ROA']

           mgzb:  
                  jbmgsy:基本每股收益(元)
                  jqmgsy: 每股收益(加权)(元)
                  jqmgsykc: 加权每股收益(扣除)(元)
                  mgjzc: 每股净资产(元)
                  mgxjll: 每股现金流量(元)
                  mgxssr: 每股销售收入(元)
                  tbmgsy:摊薄每股收益(元)
                  tbmgsykc: 摊薄每股收益(扣除)(元)	
                  tzhmgjzc: 调整后每股净资产(元)
                  xsmgsy:稀释每股收益(元)
                  mgzbname=['EPS','W.EPS','W.EPS.D','Net.A.PS','CF_PS','Rev.PS','EPS.Dilute','EPS.Dilute.D','Net.A.PS.Adj','D.EPS']

           yynl:
                  chzcgcl: 存货资产构成率(%)
                  chzzl: 存货周转率(%)
                  chzzts: 存货周转天数(天)
                  gdqyzzl: 股东权益周转率(%)
                  gdzczzl: 固定资产周转率(%)
                  ldzczzl:流动资产周转率(%)
                  ldzczzts: 流动资产周转天数(天)	
                  yszkzzl: 应收账款周转率(%)
                  yszkzzts: 应收账款周转天数(天)	
                  zzczzl: 总资产周转率(%)
                  zzczzts:总资产周转天数(天)
                  yynlname=['Invt_Asset_rate','Invt_turnover_rate','Invt_turnover_day','Shareholder_turnover_rate','Fixed_turnover_rate','Curr_Asset_turnover_rate','Curr_Asset_turnover_day','Receivable_turnover_ratio','Receivable_turnover_day','Asset_turnover_ratio,'Asset_turnover_day']

           cznl:
                  jlr: 净利润增长率(%)
                  lrze: 利润总额增长率(%)
                  mgsy: 每股收益增长率(%)
                  mgxj: 每股现金流增长率(%)
                  xsqlr: 息税前利润增长率(%)
                  yylr: 营业利润增长率(%)
                  zysr: 主营收入增长率(%)
                  zzc:总资产增长率(%)	
                  cznlname=['Net.profit_yoy','T.profit_yoy','Rev.PS_yoy','CF_PS_yoy',Profit.bTax_yoy','Rev.Profit_yoy','Rev_yoy',Asset_yoy']

           djcw:
                  jzcsyl: 净资产收益率(%)
                  jzcsylkc: 净资产收益率(扣除)(%)	
                  mgsykctb: 每股收益（扣除后摊薄）(元)	
                  mgsytb: 每股收益(摊薄)(元)
                  mgxssr: 每股销售收入(元)
                  sqzzcsyl: 税前总资产收益率(%)
                  xsjll: 销售净利率(%)
                  xsmll: 销售毛利率(%)
                  xsqlr: 息税前利润(元)
                  xsqlrl:息税前利润率(%) 
                  zzcsyl:总资产收益率(%)
                  djcwname=['ROE','ROE.D','EPS.DD','EPS.D','Rev.PS','ROA.bTax',Rev.NetProfit.R','Rev.Gr.Profit.R','Profit.bTax','Profit.bTax.R','ROA']

           czzb:
                  cqbl: 产权比率(%)
                  czyzb: 长期债务与营运资金比率(%)	
                  gdzcbl: 固定资产比率(%)
                  gzjzl: 固定资产净值率(%
                  ldbl: 流动比率(%)
                  qsjzbl: 清算价值比率(%)
                  sdbl: 速动比率(%)
                  xjbl:现金比率(%)
                  zbgbbl: 资本固定化比率(%)
                  zbhbl: 资本化比率(%)
                  zcfzl: 资产负债率(%)
                  zzc:总资产(元)
                  czzbname=['Debt_Equit_R','L.Debt_Work.Capital_R','Fix.Asset.R','Net.Asset.R','Curr_Rate','Liquidation_ratio','Quick_Rate','Cash_Rate','Capital_fixed_ratio','Capitalization_R','Assets_Debt_R','Asset']

    """
    if code[0] in ['0','2','3']:
        code='sz'+code
    elif code[0] in ['6','9']:
        code='sh'+code
    else:
        print("Input the right code, like 600000")

    url='http://comdata.finance.gtimg.cn/data/{1}/{0}'.format(code,mtype)

    r=requests.get(url,headers=hds())
    text=r.text
    text=text.split('=')[1].replace("]}};","]}}")

    data=json.loads(text)
    yearlist=data['data']['nflb']

    df=pd.DataFrame()

    for y in yearlist:
        url='http://comdata.finance.gtimg.cn/data/{1}/{0}/{2}'.format(code,mtype,y)
        r=requests.get(url,headers=hds())
        #print(url)
        text=r.text
        text=text.split('=')[1].replace("]}};","]}}")

        data=json.loads(text)
        dd=pd.DataFrame(data['data'][mtype])
        df=df.append(dd)
        
    df=df.set_index('bgrq')
    df=df.sort_index()
    df=df.replace('--',np.nan)
    df=df.applymap(lambda x:wt._tofl(x))
    #df=df.applymap(lambda x:np.where(x=='--',np.nan,float(x)))

    df.columns=wt.named[mtype]
    df=df.applymap(lambda x:wt._tofl(x))
    return df    

def get_reportlistjson_qq(code):

    url='http://message.finance.qq.com/report/get_hq_report_jgyc.php?n=5000&zqdm={0}&seq=0&format=json&r=0.38097072788514197'.format(code)
    r=requests.get(url)
    text=r.text.split('=')[1]
    data=json.loads(text)
    df=pd.DataFrame(data['data']['report'])
    df=df.applymap(lambda x:wt._tofl(x))
    return df

def get_reportjson_qq(code):
    """
    code:上海深圳交易所的股票代码
    ----------------------------
        Return：
           fbrq:发布日期
           fxs：分析师
           jgdm：评估机构
           jgjc：机构代码
           mbjg：买入价格
           mgsy1：每股收益（预测最近一年收益）
           mgsy2：每股收益（预测最近第二年的收益）
           syl1：收益率预测最近一期
           syl2：收益率预测最近2期
    """
    uu='http://message.finance.qq.com/report/get_report_search.php?n=5000&seq=0&format=json&r=0.9851241884753108&zqdm={0}'.format(code)
    tr=requests.get(uu)
    text1=tr.text.split('=')[1]
    data1=json.loads(text1)
    df1=pd.DataFrame(data1['data']['report'])
    del df1['jgdm']
    return df1

def get_belong_concept_qq(code):
    """
    获得公司所在行业的信息
    """
    url='http://stock.finance.qq.com/corp1/plate.php?zqdm={0}'.format(code)
    r=requests.get(url,headers=hds())
    text=r.text
    #print(text)
    soup=BeautifulSoup(text,'lxml')
    table=soup.find_all('table')
    df=pd.read_html(str(table[1]),header=0)[0]
    #print(df)
    return df

def get_income_composition_qq(code,mtype='cp'):
    """
    获得公司收入构成情况表
    ----------------
    mtype: 查询的分类数据
         cp:按产品对收入进行归类
         hy:按行业对收入进行归类
         dy:按地域对收入进行归类
    return :
    ---------------------
         DataFrame()
    """
    url='http://stock.finance.qq.com/corp1/income.php?zqdm={0}'.format(code)
    r=requests.get(url,headers=hds())
    text=r.text
    #print(text)
    soup=BeautifulSoup(text,'lxml')
    table=soup.find_all('table')
    #print(len(table))

    if mtype == 'cp':
        df=pd.read_html(str(table[1]),header=None,skiprows=5)[0]
    elif mtype == 'hy':
        df=pd.read_html(str(table[4]),header=None,skiprows=5)[0]
    elif mtype == 'dy':
        df=pd.read_html(str(table[7]),header=None,skiprows=5)[0]
        
    df=df.drop([0],axis=0)
    name=['name','Rev(10k)','Rev.Rate','Cost','Rev.Profit','Rev.Pro.Rate','Margin.Rate']
    
    df=df.iloc[:,:7]
    df.columns=name
    df=df.applymap(lambda x:wt._tofl(x))
    df=df.replace('',np.nan)
    df=df.dropna(how='all',axis=1)
    df['code']=code
    #print(df)
    return df

def get_forcast_qq(code=None,report='20170630',mtype=0):
    """获取企业的业绩预告信息
    code:股票代码6个字符
    report：报告期,like 20170630
    mtype:  类型,0-全部的业绩预告,1-预增的业绩预告,2-预减的业绩预告,
                 3-预盈的业绩预告,4-预亏的业绩预告,5-大幅上升的业绩预告,
                 6-大幅下降的业绩预告,7-扭亏的业绩预告,8-减亏的业绩预告,
                 9-无大变的业绩预告,10-不确定的业绩预告
    """
    if code is None:
        url='http://message.finance.qq.com/stock/jbnb/get_yjyg.php?gpdm=&type={1}&bgq={0}&p=1&lmt=50&sort_name=ggrq&order=desc'.format(report,mtype)
    elif isinstance(code,str):
        url='http://message.finance.qq.com/stock/jbnb/get_yjyg.php?gpdm={0}&type={2}&bgq={1}&p=1&lmt=50&sort_name=ggrq&order=desc'.format(code,report,mtype)
        
    r=requests.get(url,headers=hds())
    #print(url)
    text=r.text.split("yjyg=")[1]
    data=json.loads(text)
    df=pd.DataFrame(data['data']['data'])
    tpage=data['data']['totalPages']
    
    if tpage>1:
        tpage=tpage+1
        for i in range(2,tpage):
            if code is None:
                url='http://message.finance.qq.com/stock/jbnb/get_yjyg.php?gpdm=&type={1}&bgq={0}&p={2}&lmt=50&sort_name=ggrq&order=desc'.format(report,mtype,i)
            elif isinstance(code,str):
                url='http://message.finance.qq.com/stock/jbnb/get_yjyg.php?gpdm={0}&type={3}&bgq={1}&p={2}&lmt=50&sort_name=ggrq&order=desc'.format(code,report,i,mtype)
                
            r=requests.get(url,headers=hds())
            text=r.text.split("yjyg=")[1]
            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']['data']))

    try:
        df.columns=['report.D','publish.D','code','name','eps_last','type','describe']
        df['code']=df['code'].map(lambda x:str(x).zfill(6))
    except:
        pass
    
    df=df.applymap(lambda x:wt._tofl(x))
    return df

def get_finance_index_qq(code=None,rpday='20170630'):
    """获取年报季报的基本指标数据，按年获取
    """
    if code is None:
        url='http://stock.finance.qq.com/cgi-bin/sstock/q_yjgg_js?c=&d={0}&b=&p=1&l=&o='.format(rpday)
    else:
        url='http://stock.finance.qq.com/cgi-bin/sstock/q_yjgg_js?c={0}&d={1}&b=&p=2&l=&o='.format(code,rpday)
        
    r=requests.get(url,headers=hds())
    text=r.text.split("_datas:[[")[1].replace("]],_o:0};\n","")
    text=text.replace("],[",'\n')
    df=pd.read_csv(StringIO(text),header=None)

    tps=int(r.text.split(",_pages:")[1].split(",_num:")[0])
    tpss=tps+1
    if tps > 1:
        for i in range(2,tpss):
            if code is None:
                url='http://stock.finance.qq.com/cgi-bin/sstock/q_yjgg_js?c=&d={0}&b=&p={1}&l=&o='.format(rpday,i)
            else:
                url='http://stock.finance.qq.com/cgi-bin/sstock/q_yjgg_js?c={0}&d={1}&b=&p={2}&l=&o='.format(code,rpday,i)

            r=requests.get(url,headers=hds())
            text=r.text.split("_datas:[[")[1].replace("]],_o:0};\n","")
            text=text.replace("],[",'\n')
            df=df.append(pd.read_csv(StringIO(text),header=None))
        
    df=df.drop([0,11],axis=1)
    df.columns=['code','name','report.d','publish.d','eps','nav.ps','cf.ps','roe','cost.pro.rate','Rev.p.yoy%','dispatch']
    
    df=df.replace('--',np.nan)
    df=df.applymap(lambda x:wt._tofl(x))
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    return df

def get_drogan_tiger_qq(code=None,start=None,end=None):
    """查看龙虎榜的信息
    ------------------------
    code : 查询股票的代码
    start：开始查询的时间，20170101
    end  :截止查询的时间，20170630
    """
    if (code is None) and (start is None) and (end is None):
        url='http://stock.finance.qq.com/cgi-bin/sstock/q_lhb_js?t=0&c=&b=&e=&p=1&l=&ol=6&o=desc'
    if (start is not None) and (end is not None):
        if code is None:
            code=''
            url='http://stock.finance.qq.com/cgi-bin/sstock/q_lhb_js?t=2&c={0}&b={1}&e={2}&p=1&l=&ol=6&o=desc'.format(code,start,end)
        else:
            url='http://stock.finance.qq.com/cgi-bin/sstock/q_lhb_js?t=1&c={0}&b={1}&e={2}&p=1&l=&ol=6&o=desc'.format(code,start,end)

    #print(url)
    r=requests.get(url,headers=hds())
    text=r.text
    df=_text2pd(text)

    tps=int(r.text.split(",_pages:")[1].split(",_num:")[0])
    tpss=tps+1
    if tps > 1:
        for i in range(2,tpss):
            if (code is None) and (start is None) and (end is None):
                url='http://stock.finance.qq.com/cgi-bin/sstock/q_lhb_js?t=0&c=&b=&e=&p={0}&l=&ol=6&o=desc'.format(i)
            if (start is not None) and (end is not None):
                if code is None:
                    code=''
                    url='http://stock.finance.qq.com/cgi-bin/sstock/q_lhb_js?t=2&c={0}&b={1}&e={2}&p={3}&l=&ol=6&o=desc'.format(code,start,end,i)
                else:
                    url='http://stock.finance.qq.com/cgi-bin/sstock/q_lhb_js?t=1&c={0}&b={1}&e={2}&p={3}&l=&ol=6&o=desc'.format(code,start,end,i)
            r=requests.get(url,headers=hds())
            text=r.text
            df=df.append(_text2pd(text))

    df=df.drop(4,axis=1)
    df.columns=['date','code','name','descrise','price','chg%']
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    df=df.set_index('date')
    df=df.sort_index()
    df=df.applymap(lambda x:wt._tofl(x))
    return df
    

def _text2pd(text):
    text=text.split("_datas:[[")[1].replace("]],_o:0};","")
    text=text.replace("],[",'\n')
    #print(text)
    df=pd.read_csv(StringIO(text),header=None)
    return df

def get_TobefreeTrade_qq(code=None,start=today,end='20191231'):
    """大小非解禁时间表
    ------------------
    code : 查询股票的代码,code is None,查询该时间段所有的股票解禁时间表
    start：开始查询的时间，20170101
    end  :截止查询的时间，20170630    
    """
    if code is None:
        code = ''
        
    url='http://stock.finance.qq.com//sstock/list/view/dxf.php?c={0}&b={1}&e={2}'.format(code,start,end)

    r=requests.get(url,headers=hds())
    text=r.text.split('=[[')[1].replace("]];",'')
    text=text.replace('],[','\n')
    df=pd.read_csv(StringIO(text),header=None)

    df=df.drop(6,axis=1)
    df.columns=['code','name','Free.date','Free.S(10K)','Free.MV(10K)','Curr.S(10K)','Source','F.S/Curr.S.%']
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    df=df.applymap(lambda x:wt._tofl(x))
    return df

def get_bigtradeinfo_qq(code=None,start='20010120',end=today):
    """大宗交易
    """
    
    if code is None:
        code=''
        
    url='http://stock.finance.qq.com/sstock/list/view/dzjy.php?b={1}&e={2}&p=1&o=0&c={0}'.format(code,start,end)

    r=requests.get(url,headers=hds())
    text=r.text
    #print(text)
    df=_text2pd(text)

    tps=int(r.text.split(",_pages:")[1].split(",_num:")[0])
    tpss=tps+1
    if tps > 1:
        for i in range(2,tpss):
            if  code is None:
                code=''
                
            url='http://stock.finance.qq.com/sstock/list/view/dzjy.php?b={1}&e={2}&p={3}&o=0&c={0}'.format(code,start,end,i)
            r=requests.get(url,headers=hds())
            text=r.text
            df=df.append(_text2pd(text))

    df.columns=['date','code','name','price','amount(10K)','volume(10K)','buy_inst','sell_inst']
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    df=df.set_index('date')
    df=df.sort_index()
    df=df.applymap(lambda x:wt._tofl(x))
    return df

def get_holders_num_qq(rpdate='2017-06-30'):

    url='http://web.ifzq.gtimg.cn/fund/zcjj/zcjj/allzc?colum=3&order=desc&page=1&pagesize=50&bgrq={0}&_var=v_jjcg'.format(rpdate)

    r=requests.get(url,headers=hds())
    text=r.text.split("jjcg=")[1]
    data=json.loads(text)
    df=pd.DataFrame(data['data']['data'])
    tpage=data['data']['totalPages']
    
    if tpage>1:
        tpage=tpage+1
        for i in range(2,tpage):
            url='http://web.ifzq.gtimg.cn/fund/zcjj/zcjj/allzc?colum=3&order=desc&page={1}&pagesize=50&bgrq={0}&_var=v_jjcg'.format(rpdate,i)
            r=requests.get(url,headers=hds())
            text=r.text.split("jjcg=")[1]
            data=json.loads(text)
            df=df.append(pd.DataFrame(data['data']['data']))
    df.columns=['Total.Num(10K)','change(10K)','inst.Num','Curr.Rate%','code','name']
    df['date']=rpdate
    df['code']=df['code'].map(lambda x:str(x).zfill(6))
    return df
    
def get_cashfl_industry_qq(mtype=1):
    """获取交易日当天的板块资金流动情况
    -------------------------------
    mtype:整数
      1-按行业主力资金流动情况
      3-按概念主力资金流动情况
      2-按个股的增仓资金流动情况
      4-价跌主力增仓排名
      5-价涨主力减仓排名
      6-主力资金放量股
      ----------------------
      url_cashfl_industry={1'http://stock.gtimg.cn/data/view/flow.php?t=2',
                           2:'http://stock.gtimg.cn/data/view/flow.php?t=4',
                           3:'http://stock.gtimg.cn/data/view/flow.php?t=5',
                           4:'http://stock.gtimg.cn/data/view/flow.php?t=7&d=1',
                           5:'http://stock.gtimg.cn/data/view/flow.php?t=8&d=1',
                           6:'http://stock.gtimg.cn/data/view/flow.php?t=9&d=1'}
    """
    url=wt.url_cashfl_industry[mtype]

    r=requests.get(url,headers=hds())
    text=r.content.decode('gbk')
    if mtype in [1,3]:
        text=text.split("boardzhuli='")[1]
        text=text.split("';var v_s_boardfunds='")
        text='\n'.join(text)
        text=text.replace("'",'')
    if mtype == 2:
        text=text.split("stock_fund_netin_10='")[1]
        text=text.split("; var stock_fund_netout_10='")
        text='\n'.join(text)
        text=text.replace("'",'')

    if mtype ==4:
        text=text.split("PrDwn='")[1].replace("';",'')
    if mtype ==5:
        text=text.split("v_s_PrUp='")[1].replace("';",'')
    if mtype == 6:
        text=text.split("v_s_zlfl_rank='")[1].replace("';",'')
        
    text=text.replace("~",',').replace("^",'\n').replace(";",'')
    df=pd.read_csv(StringIO(text),header=None)
    df=df.drop_duplicates()
    #df=df.replace('--',np.nan)
    df=df.applymap(lambda x:wt._tofl(x))
    return df

def get_profile_qq(code):
    """获得公司的基本资料
    """
    url='http://stock.finance.qq.com/corp1/profile.php?zqdm=%s'%code
    r=requests.get(url,headers=hds())
    text=r.text
    #print(text)
    soup=BeautifulSoup(text,'lxml')
    table=soup.find_all('table')
    df=pd.read_html(str(table[1]),header=0,skiprows=1)[0]
    #print(df)
    return df

def get_inst_hypeizhi_qq(mtype='ins',date='2017-06-30'):
    """mtype='inc' or 'dec';
    """
    url='http://web.ifzq.gtimg.cn/fund/hyconf/hyconf/hypm?type={0}&colum=bdsz&order=desc&rd={1}'.format(mtype,date)

    r=requests.get(url,headers=hds())
    print(url)
    data=json.loads(r.text)
    df=pd.DataFrame(data["data"]["data"])
    df.rename(columns={'bdsz':'Chang', 'ccjj':'inst_num', 'ccsz':'hold_MarketV', 'hymc':"industry_name", 'rd':'date'},inplace=True)
    df=df[['industry_name', 'inst_num','Chang', 'hold_MarketV',  'date']]
    df=df.applymap(lambda x:wt._tofl(x))
    df=df.sort_values(by='Chang')
    return df
     
if __name__=="__main__":
    #df=get_preview_qq(sys.argv[1])
    #dd=get_cwfx_qq(sys.argv[1],sys.argv[2])
    #dd=get_belong_concept_qq(sys.argv[1])
    #df=get_income_composition_qq(sys.argv[1],sys.argv[2])
    #df=get_forcast_qq(sys.argv[1],report='20170630')
    #df=get_finance_index_qq(rpday='20170630')
    #dd=get_drogan_tiger_qq(sys.argv[1],start='20000101',end='20170728')
    #df=get_TobefreeTrade_qq(code=sys.argv[1])
    #dd=get_bigtradeinfo_qq(code=sys.argv[1])
    #dd=get_holders_num_qq()
    #dd=get_cashfl_industry_qq(int(sys.argv[1]))
    #df=get_profile_qq(sys.argv[1])
    df= get_inst_hypeizhi_qq()#(sys.argv[1])
