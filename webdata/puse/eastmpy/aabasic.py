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

def get_coreconcept_f10_EM(code):
    """
    核心题材
    --------------------------
    code:为股票代码，为6位数
    """
    if code[0] in ['6','9']:
        code='SH'+code
    if code[0] in ['0','2','3']:
        code = 'SZ'+code
        
    #url='http://f10.eastmoney.com/f10_v2/CoreConception.aspx?code={0}'.format(code)
    url='http://emweb.securities.eastmoney.com/PC_HSF10/CoreConception/CoreConceptionAjax?code={0}'.format(code)
 
    r=requests.get(url,headers=hds())
    text=r.text

    data=json.loads(text)

    df=pd.DataFrame(data['hxtc'])
    df=df.replace('--',np.nan)
    df=df.dropna(how='all',axis=1)
    
    return df

def get_forcast_f10_EM(code):
    """
    股票业绩预测
    --------------------------
    code:为股票代码，为6位数
    """
    if code[0] in ['6','9']:
        code='SH'+code
    if code[0] in ['0','2','3']:
        code = 'SZ'+code
        
    #url='http://f10.eastmoney.com/f10_v2/CoreConception.aspx?code={0}'.format(code)
    url='http://emweb.securities.eastmoney.com/PC_HSF10/ProfitForecast/ProfitForecastAjax?code={0}'.format(code)
 
    r=requests.get(url,headers=hds())
    text=r.text

    data=json.loads(text)

    #print(data.keys())
    
    df=pd.DataFrame(data['Result']['pjtj'])
    df=df.replace('--',np.nan)
    df=df.dropna(how='all',axis=1)
    
    return df

def get_shareholderResearch_f10_EM(code):
    """
    股票股东研究
    --------------------------
    code:为股票代码，为6位数
    """
    if code[0] in ['6','9']:
        code='SH'+code
    if code[0] in ['0','2','3']:
        code = 'SZ'+code
        
    #url='http://f10.eastmoney.com/f10_v2/CoreConception.aspx?code={0}'.format(code)
    url='http://emweb.securities.eastmoney.com/PC_HSF10/ShareholderResearch/ShareholderResearchAjax?code={0}'.format(code)
 
    r=requests.get(url,headers=hds())
    text=r.text

    data=json.loads(text)

    df=pd.DataFrame(data['gdrs'])
    df=df.replace('--',np.nan)
    df=df.dropna(how='all',axis=1)
    
    return df



def get_businessanalysis_f10_EM(code):
    """
    题材，主营业务分析
    --------------------------
    code:为股票代码，为6位数
    """
    if code[0] in ['6','9']:
        code='SH'+code
    if code[0] in ['0','2','3']:
        code = 'SZ'+code
        
    url='http://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/BusinessAnalysisAjax?code={0}'.format(code)
 
    r=requests.get(url,headers=hds())
    text=r.text

    data=json.loads(text)

    zyfw=data['zyfw'][0]['ms']

    jyps=data['jyps'][0]['ms']

    
    df=pd.DataFrame()
    for i in range(5):
        for mt in ['hy','cp','qy']:
            df=df.append(pd.DataFrame(data['zygcfx'][i][mt]))
    df=df.replace('--',np.nan)
    df=df.dropna(how='all',axis=1)
    
    return df,zyfw,jyps

def get_IndustryAnalysis_f10_EM(code,mtype='gsgm'):
    """
    业务分析
    --------------------------
    code:为股票代码，为6位数
    """
    if code[0] in ['6','9']:
        code='sh'+code
    if code[0] in ['0','2','3']:
        code = 'sz'+code
        
    url='http://emweb.securities.eastmoney.com/PC_HSF10/IndustryAnalysis/IndustryAnalysisAjax?code={0}'.format(code)
 
    r=requests.get(url,headers=hds())
    text=r.text

    data=json.loads(text)

    if mtype == 'gsgm':
        df=pd.DataFrame(data['Result']['gsgmltsz'])
        #公司规模在行业中的排名
        df=df.drop('bgq',axis=1)
        df.columns=['code','name','np','TotalValue','rank','Rev','CurrValues']
        
    elif mtype == 'dbfx':
        #杜邦分析排名
        df=pd.DataFrame(data['Result']['dbfxbj']['data'])
        df.columns=['code','name','npr_ls3','npr_ls2','npr_ls1','npr_3mean','rank','qycs', 'qycs1','qycs2', 'qycspj', 'roe_ls3', 'roe_ls2', 'roe_ls1', 'roe_3mean', 'zzczzl', 'zzczzl1','zzczzl2', 'zzczzlpj']        

    elif mtype=='gzbj':
        #估值比较排名
        df=pd.DataFrame(data['Result']['gzbj']['data'])
        df.rename(columns={'dm':'code', 'jc':'name', 'pm':'rank','ssl':'psls', 'ssl1':'ps_n1','ssl2':'ps_n2', 'ssl3':'ps_n3', 'sslTTM':'ps_ttm', 'syl':'pels', 'syl1':'pe_n1', 'syl2':'pe_n2', 'syl3':'pe_n3', 'sylTTM':'pe_ttm'},inplace=True)
        
    elif mtype == 'czxbj':
        #成长性比较排名
        df=pd.DataFrame(data['Result']['czxbj']['data'])
        df.rename(columns={"dm":"code",'jc':'name','pm':'rank','jbmgsyzzl':'epsls1_yoy','jbmgsyzzl1':'epsn1_yoy', 'jbmgsyzzl2':'epsn2_yoy', 'jbmgsyzzl3':'epsn3_yoy','jbmgsyzzlTTM':'eps_ttm','jbmgsyzzlfh':'epsfh3_yoy','yysrzzl':'revA_yoy', 'yysrzzl1':'revn1_yoy','yysrzzl2':'revn2_yoy', 'yysrzzl3':'revn3_yoy', 'yysrzzlTTM':'rev_ttm', 'yysrzzlfh':'revfh3_yoy'},inplace=True)

    elif mtype == 'gmsz':
        df=pd.DataFrame(data['Result']['gsgmzsz'])
        #公司市值排名
        df=df.drop('bgq',axis=1)
        df.columns=['code','name','np','TotalValue','rank','Rev','CurrValues']        
        
    df=df.replace('--',np.nan)
    df=df.dropna(how='all',axis=1)
    
    return df

def get_sharesGroupby_f10_EM(code,mtype='hy'):
    """
    所属行业、概念、地域中的分析、收集同类股票信息
    --------------------------
    code:为股票代码，为6位数
    """
    if code[0] in ['6','9']:
        code='SH'+code
    if code[0] in ['0','2','3']:
        code = 'SZ'+code
    #hy
    if mtype == 'hy':
        url='http://emweb.securities.eastmoney.com/PC_HSF10/StockRelationship/StockRelationshipAjax?code={0}&orderBy=1&isAsc=false'.format(code)

    #dy
    if mtype == 'dy':
        url='http://emweb.securities.eastmoney.com/PC_HSF10/StockRelationship3/StockRelationshipAjax?code={0}&orderBy=1&isAsc=false'.format(code)
    
    #gn
    if mtype=='gn':
        url='http://emweb.securities.eastmoney.com/PC_HSF10/StockRelationship2/GetConceptList?code={0}&orderBy=1&isAsc=true&type=1'.format(code)
        r=requests.get(url,headers=hds())
        data=json.loads(r.text)
        dtt=pd.DataFrame(data["Result"])
        dtt=dtt.set_index('glid')
        print(dtt.loc[:,'glmc'].tolist())
        #for idd in dtt.index:
        bkname=input("输入概念名称:")
        idd=dtt[dtt['glmc']==bkname].index[0]
        url='http://emweb.securities.eastmoney.com/PC_HSF10/StockRelationship2/GetSameConceptStockRankList?code={0}&orderBy=1&typeId={1}&isAsc=false'.format(code,idd)

    #print(url)
    r=requests.get(url,headers=hds())
    text=r.text
    #print(text)
    data=json.loads(text)

    try:
        df=pd.DataFrame(data["Result"]["stockRandList"])
    except:
        df=pd.DataFrame(data["Result"])

    df=df.replace('--',np.nan)
    df=df.dropna(how='all',axis=1)
    
    return df

def get_bussiAnalys_f10_EM(code):
    """
    核心题材
    --------------------------
    code:为股票代码，为6位数
     return:
          income:按行业、产品、区域分类的收入、成本盈利情况分析
          zyfw:主营业务范围
          jyps：经营评述
    """
    if code[0] in ['6','9']:
        code='sh'+code
    if code[0] in ['0','2','3']:
        code = 'sz'+code

    url='http://emweb.securities.eastmoney.com/PC_HSF10/BusinessAnalysis/BusinessAnalysisAjax?code={0}'.format(code)
    #url='http://emweb.securities.eastmoney.com/CoreConception/Index?type=web&code={0}#'.format(code)
    r=requests.get(url,headers=hds())
    text=r.text
    data=json.loads(text)

    income=pd.DataFrame()

    for dset in data['zygcfx']:
        for label in ['hy','cp','qy']:
            income=income.append(pd.DataFrame(dset[label]))

    income.rename(columns={'cbbl':'cost.r', 'lrbl':'profit.r', 'mll':'margin', 'orderby':'rev1', 'rq':'date', 'srbl':'rev.r', 'zycb':'cost', 'zygc':'type','zylr':'profit', 'zysr':'rev'},inplace=True)

    income=income[[ 'date', 'type', 'rev1','rev', 'rev.r', 'cost','cost.r','margin', 'profit','profit.r', 'dw']]

    zyfw=data['zyfw'][0]['ms']

    jyps=data['jyps'][0]['ms']
    return zyfw,jyps,income


def get_bussinessanalysis_EM(code):
    """
    核心题材
    --------------------------
    code:为股票代码，为6位数
    """
    if code[0] in ['6','9']:
        code='sh'+code
    if code[0] in ['0','2','3']:
        code = 'sz'+code

    url='http://f10.eastmoney.com/f10_v2/BusinessAnalysis.aspx?code={0}'.format(code)
    #url='http://emweb.securities.eastmoney.com/CoreConception/Index?type=web&code={0}#'.format(code)
    r=requests.get(url,headers=hds())
    text=r.text
    html=BeautifulSoup(r.text,'lxml')

    try:
        mainbs=html.find('div',attrs={"class":"section first"})
        mainbs=mainbs.text
    except:
        mainbs=None

    try:
        article=html.find('div',attrs={"class":"article"})
        article=article.text
    except:
        article=None

    try:
        ts=html.find_all('table')
        df=pd.DataFrame()

        for t in ts:
            tbl=str(t)
            #tbl=tbl.replace('<td class="tips-fieldnameL" rowspan="8">按产品分类</td>','')
            #tbl=tbl.replace('<td class="tips-fieldnameL" rowspan="3">按地区分类</td>','')
            #tbl=tbl.replace('<td class="tips-fieldnameL" rowspan="5">按行业分类</td>','')
            dd=pd.read_html(tbl)[0]
        
            df=df.append(dd)
    except:
        df=None

    return mainbs,df,article

def get_hynewslist_EM(bkname,mtype='hy'):
    """
    获得行业信息列表
    mtype:hy--行业信息;gg--个股信息
    """
    try:
        df=pd.read_pickle('output/eastmsource/bk.pkl')
    except:
        df=pd.read_csv('output/eastmsource/bk.csv',index_col=0,encoding='gbk')
    idd=df[df['name']==bkname]['id'].tolist()[0]

    url='http://stock.eastmoney.com/hangye/hy{}.html'.format(idd[-3:])
    #print(url)
    r=requests.get(url,headers=hds())
    try:
        text=r.content.decode('gbk')
    except:
        text=r.text
    #print(text)
    html=lxml.html.parse(StringIO(text))
    dataset=[]
    
    if mtype=='hy':
        hyinfo=html.xpath('//div[@class="americaleft mt10"]/div[1]//div[@class="deta"]/ul/li')
    if mtype=='gg':
        hyinfo=html.xpath('//div[@class="americaleft mt10"]/div[2]//div[@class="deta"]/ul/li')

    for hy in hyinfo:
        text=hy.xpath('a/text()')[0]
        href=hy.xpath('a/@href')[0]
        #print(text,href)
        dataset.append([text,href])

    #print(dataset)
    df=pd.DataFrame(dataset,columns=['title','href'])
    return df

def get_newstext_EM(bkname,mtype='hy'):
    """
    获得行业信息文本
    mtype:hy--行业信息;gg--个股信息
    """    
    df=get_hynewslist_EM(bkname,mtype)

    dataset=[]
    for url in df['href']:
        r=requests.get(url,headers=hds())
        print(url)
        try:
            text=r.content.decode('utf8')
        except:
            text=r.text
        #print(text)
        html=lxml.html.parse(StringIO(text))
        textc=html.xpath('//div[@id="ContentBody"]//text()')
        #print(textc)
        dataset.append('\n'.join(textc))

    return dataset
        
    
def get_concept_share_epsforcast_EM(BKid):
    """板块id号，如有色金属的板块ID--BK0478
    """
    url='http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C.{0}1&sty=GEMCPF&st=(AllNum)&p=1&ps=50000&token=3a965a43f705cf1d9ad7e1a3e429d622'.format(BKid)

    r=requests.get(url,headers=hds())
    #print(r.text)
    text=r.text.split('(["')[1].split('"])')[0]
    text=text.replace('","','\n')

    df=pd.read_csv(StringIO(text),header=None)

    return df
    
def get_tick_today_EM(code,mtype=0):
    if code[0] in ['6','9']:
        code=code+'1'
    if code[0] in ['0','2','3']:
        code = code+'2'

    url='http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/CompatiblePage.aspx?Type=OB&stk={0}&Reference=xml&limit={1}&page=1'.format(code,mtype)

    r=requests.get(url,headers=hds())
    text=r.text.split('=')[1]
    data=text.split('data:["')[1].replace('"]};','').replace('","','\n')
    df=pd.read_csv(StringIO(data),header=None)

    page=text.split('{pages:')[1].split(',data:')[0]
    page=int(page)

    if page>1:
        for i in range(2,page+1):
            url='http://hqdigi2.eastmoney.com/EM_Quote2010NumericApplication/CompatiblePage.aspx?Type=OB&stk={0}&Reference=xml&limit={1}&page={2}'.format(code,mtype,i)

            r=requests.get(url,headers=hds())
            text=r.text.split('=')[1]
            data=text.split('data:["')[1].replace('"]};','').replace('","','\n')
            df=df.append(pd.read_csv(StringIO(data),header=None))
    df.columns=['time','price','volume','type']
    df=df.applymap(lambda x:wt._tofl(x))
    return df
    
if __name__=="__main__":
    #df=get_bussinessanalysis_EM(sys.argv[1])
    #dd=get_concept_share_epsforcast_EM('BK0478')
    #df=get_ggnewslist_EM(sys.argv[1])
    #dd=get_newstext_EM(sys.argv[1],'hy')
    #df=get_tick_today_EM(sys.argv[1])
    #df=get_forcast_f10_EM(sys.argv[1])
    df=get_sharesGroupby_f10_EM(sys.argv[1],'gn')
