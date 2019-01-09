#!/usr/bin/env python3
# -*-coding:utf-8-*-

import pandas as pd
import numpy as np
import webdata as wd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import abc,datetime,re
import pickle,sys,requests
import lxml.html
from lxml import etree
from io import StringIO
from webdata.util.hds import user_agent as hds
from matplotlib.font_manager import FontProperties
#font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\simsun.ttc", size=8)

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
days = mdates.DayLocator()
yearsFmt = mdates.DateFormatter('%m')
# 中文乱码和坐标轴负号的处理
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def _totime(x):
    try:
        day=datetime.datetime.strptime(x,'%Y%m%d')
        return day
    except:
        return x

def pgplott(df):
    dd=df.groupby(['type','price'])['volume'].sum()
    d=dd.unstack().T
    fig=plt.figure(figsize=(10,5))
    fig.subplots_adjust(hspace=0.15, wspace=0.05,left=0.06,right=0.99,top=0.97,bottom=0.09)
    ax1=fig.add_subplot(311)
    d['B'].plot(kind='bar',ax=ax1,label='buy')
    plt.grid(True)
    labels = ax1.get_xticklabels()
    plt.setp(labels, rotation=45, fontsize=5)#,visual=False)
    plt.legend()
    ax2=fig.add_subplot(312)
    d['S'].plot(kind='bar',ax=ax2,label='sell')#,visual=False)
    plt.grid(True)
    labels = ax2.get_xticklabels()
    ax2.set_ylabel("Volume")
    plt.setp(labels, rotation=45, fontsize=5)
    plt.legend()
    
    try:
        ax3=fig.add_subplot(313)
        d['M'].plot(kind='bar',ax=ax3,label='unkown')
        plt.grid(True)
        labels = ax3.get_xticklabels()
        plt.setp(labels, rotation=45, fontsize=8)
        plt.legend()
    except:
        pass
    
    plt.show()
    return
        

class ASecurity(object):
    def __init__(self,code=None,m=12,n=6,md=3,window=5,start='2017-12-31',end='2018-03-31'):
        if isinstance(code,str):
            self.__code=code
        self.__ld=m
        self.__sd=n
        self.__md=md
        self.__window=window
        self.__st=start
        self.__end=end
        self.__data=None
        self.__tick=None
        self.__alldata=None
        self.__ths=None
        self.__pepb=None
        self.__rzrq=None
        self.__cf=None
        self.__hdata=None
        self.Bs=None
        self.Is=None
        self.Cs=None
        
    def setcode(self,code):
        if isinstance(code,str):
            if (len(code)==4) or (len(code)==6):
                self.__code=code
                self.__data=None
                self.__tick=None
                self.__ths=None
                self.__alldata=None
                self.__pepb=None
                self.__rzrq=None
                self.__cf=None
                self.__hdata=None
                self.Bs=None
                self.Is=None
                self.Cs=None                
                
    def getcode(self):
        return self.__code
    
    def getk_data(self,code=None):
        if code is not None:
            self.setcode(code)
        if len(self.__code)==4:
            self.__data = wd.quandlyd(self.__code)
        elif len(self.__code)==6:
            self.__data = wd.get_k_data(self.__code)
           

    def getk_tick(self,code=None):
        if code is not None:
            self.setcode(code)
        self.__tick=wd.tick_data_today(self.__code)


    def KDJ(self,code=None):
        if code is not None:
            self.setcode(code)        
        try:
            if self.__data is None:
                self.getk_data()
        except:
            pass
        d=wd.KDJv1_df(self.__data,window=self.__window)

    def MACD(self,code=None):
        if code is not None:
            self.setcode(code)        
        try:
            if self.__data is None:
                self.getk_data()
        except:
            pass
        d=wd.MACDv1_df(self.__data,ld=self.__ld,sd=self.__sd,md=self.__md)

    def tickpgroup(self,code=None):
        if code is not None:
            self.setcode(code)        
        self.getk_tick()
        try:
            pgplott(self.__tick)
        except Exception as e:
            print(e)
            pass

    def __get_pepb_data(self,code=None):
        if code is not None:
            self.setcode(code)        
        self.__pepb=wd.get_sina_pepb()
    
    def pepb(self,code=None,Rturn=False):
        """
        获取个股的PE,PB,PS等指标
        Return:
        --------------------
              PE,PE_TTM,PB,PCF, PS, PEG
        """
        if code is not None:
            self.setcode(code)        
        try:
            if self.__pepb is None:
                self.__get_pepb_data()
        except:
            pass

        dfc=self.__pepb
        Name=dfc.ix[self.__code,'name']
        Price=dfc.ix[self.__code,'trade']
        PE=dfc.ix[self.__code,'pe']
        PE_TTM=dfc.ix[self.__code,'pe_ttm']
        PB=dfc.ix[self.__code,'pb']
        try:
            if self.__ths==None:
                self.getfin_ths()
        except:
            pass
        dfths=wd.PdDataFrame_diff(self.__ths,'cf_ps')
        dfcf=dfths.tail(4)
        cfps=np.sum(dfcf['cf_ps_diff'])
        PCF=Price/cfps
        
        np_yoy=dfths.ix[-1,'np_yoy']
        PEG=Price/np_yoy
        
        dfths=wd.PdDataFrame_diff(self.__ths,'business_income')
        dfbi=dfths.tail(4)
        bi=np.sum(dfbi.ix[:,'business_income_diff'])
        PS=dfc.ix[self.__code,'mktcap']/bi
        
        ROE=dfths.ix[-1,'roe_a']
        print ("\n","%s, Price is %.2f, PE is %.4f, PE_TTM is %.4f, PB is %.4f"%(Name,Price,PE,PE_TTM,PB))
        print("经营性 PCF is %.4f,PS_TTM is %2.4f, PEG is %.4f, the last ROE is %.4f"%(PCF, PS, PEG, ROE))
        if Rturn:
            return {'pe':PE,'pe_ttm':PE_TTM,'pb':PB,'pcf':PCF, 'ps':PS,'peg': PEG,'code':self.__code,'roe':ROE}
        
    def readcsv(self):
        """
        读入新浪的个股全部数据信息
        """
        if code is not None:
            self.setcode(code)               
        fn='./output/xuangu/MergeLast.csv'
        if self.__alldata is None:
            self.__alldata=pd.read_csv(fn,encoding='gbk',index_col=0,header=0,low_memory=False)
            self.__alldata['timeToMarket']=self.__alldata['timeToMarket'].map(lambda x:str(x)[:8])
            self.__alldata['timeToMarket']=self.__alldata['timeToMarket'].map(lambda x:_totime(x))
            self.__alldata['code']=self.__alldata['code'].map(lambda x:str(x).zfill(6))
        return self.__alldata.loc[self.__alldata['code']==self.__code]

    def readpkl(self):
        fn='./output/xuangu/MergeLast.pkl'
        if self.__alldata is None:
            self.__alldata=pd.read_pickle(fn)
            self.__alldata['timeToMarket']=self.__alldata['timeToMarket'].map(lambda x:str(x)[:8])
            self.__alldata['timeToMarket']=self.__alldata['timeToMarket'].map(lambda x:_totime(x))
        return self.__alldata.loc[self.__alldata['code']==self.__code]

    def getfin_sina(self):
        """
        读入新浪的个股全部数据信息
        """
        
        try:
            if self.__alldata.shape[0]>0:
                return self.__alldata
        except:
            self.readcsv()
            return self.__alldata

    def fin_sina(self,code=None):
        """
        读取新浪的个股信息
        """
        if code is not None:
            self.setcode(code)               
        try:
            if self.__alldata == None:
                self.readcsv()
        except:
            pass
        df=self.__alldata
        df=df[df['code']==self.__code]
        df=df[['eps', 'epsg', 'nprg', 'mbrg', 'npr', 'nav',\
               'net_profit_ratio', 'roe','roe.1','Y_Q']]
        df=df.set_index('Y_Q')
        df=df.tail(9)
        #print(df.tail(10))
        return df

    def fin_ths(self,code=None):
        """
        选取同花顺的个股信息
        """
        if code is not None:
            self.setcode(code)               
        try:
            if self.__ths==None:
                self.getfin_ths()
        except:
            pass
        dfths=wd.PdDataFrame_diff(self.__ths,'cf_ps')
        dfths=wd.PdDataFrame_diff(dfths,'eps')
        df=dfths[['eps','eps_diff','np_yoy','bi_yoy','roe','roe_a','sale_margin']].tail(9)
        #print('\n',df)
        return df
        
    def getfin_ths(self,code=None):
        """
        获取同花顺个股的财务指标
        """
        if code is not None:
            self.setcode(code)               
        self.__ths=wd.get_finance_index_ths(self.__code)
        self.__ths=self.__ths.sort_values(by='date')
        return self.__ths

    def rzrq(self,code=None):
        """
        获取个股融资融券的数据
        """
        if code is not None:
            self.setcode(code)               
        self.__rzrq=wd.margins_share(self.__code)
        self.__rzrq=self.__rzrq.dropna(how='all',axis=1)
        self.__rzrq=self.__rzrq.sort_index()
        print(self.__rzrq.tail(4))

    def hynews(self,code=None,ns=5):
        """
        获取行业信息资料
        """
        if code is not None:
            self.setcode(code)               
        df=wd.qqhyxw(self.__code)
        text=[]
        for i in range(ns):
            d=wd.get_text(df.iloc[i,1])
            text.append(df.iloc[i,0]+'\n'+df.iloc[i,2])

        content='\n\n'.join(text)
        return content

    def ggnews(self,code=None,ns=5):
        """
        获取股票个股信息
        """
        if code is not None:
            self.setcode(code)               
        df=wd.finance_share_news(self.__code)
        text=[]
        for i in range(ns):
            d=wd.get_text(df.iloc[i,1])
            text.append(df.iloc[i,0]+'\n'+df.iloc[i,2])

        content='\n\n'.join(text)
        return content

    def holdbyinst(self,code=None):
        """
        获取股票的机构持有情况，可别是近两个季度的机构持股变动情况
        """
        if code is not None:
            self.setcode(code)               
        dfs=wd.holdby_detail(self.__code,self.__st)
        dfend=wd.holdby_detail(self.__code,self.__end)
        ds=dfs[['ShareHDNum',  'TabProRate',  'TabRate','Vposition']].sum()
        de=dfend[['ShareHDNum',  'TabProRate',  'TabRate','Vposition']].sum()
        d=de-ds
        ch=de/ds-1
        
        t1="本季度的机构持股数量为%.2f万股,上季度的机构持股数量为%.2f万股"%(de[0]/10000,ds[0]/10000)
        t2="机构持股数量变动%.2f,所持股票占总股数变动%.2f"%(d[0]/10000,d[1])
        t3="机构持股数量比例变动%.3f,所持股票占总股数比例变动%.3f,所持股票市值比例变动%.3f"%(ch[0],ch[1],ch[3])
        text=[t1,t2,t3]
        content='\n\n'.join(text)
        
        #print("本季度的机构持股数量为%.2f万股,上季度的机构持股数量为%.2f万股"%(de[0]/10000,ds[0]/10000))
        #print("机构持股数量变动%.2f,所持股票占总股数变动%.2f"%(d[0]/10000,d[1]))
        #print("机构持股数量比例变动%.3f,所持股票占总股数比例变动%.3f,所持股票市值比例变动%.3f"%(ch[0],ch[1],ch[3]))
        return content

    def holderschg(self,code=None):
        if code is not None:
            self.setcode(code)               
        df=wd.get_holder_change_EM(self.__code)[['HolderNum','HolderNumChange','HolderNumChangeRate','PreviousHolderNum','RangeChangeRate','HolderAvgStockQuantity']]
        return df
        
    def dadan(self,code=None,opt=4):
        """
        获取股票交易日每笔成交量400股以上的情况
        """
        if code is not None:
            self.setcode(code)               
        try:
            d=wd.get_dadan(self.__code,opt)
            d=d.set_index('time')
            d.sort_index(inplace=True)
        except:
            d=wd.get_dadan_sina(self.__code,opt=1)
        return d

    def div(self,code=None):
        """
        获取股票的利润分配方案，股息率、以及推出该方案后（预告方案、股权登记日前
        10日，股权登记日后30日）的股票的涨跌幅情况
        """
        if code is not None:
            self.setcode(code)               
        #df=wd.get_div(self.__code)
        df=wd.div_share(self.__code)[['SGBL','ZGBL','XJFH','GXL','YAGGRHSRZF','GQDJRQSRZF','CQCXRHSSRZF']]
        df.sort_index(inplace=True)
        #print(df)
        return df

    def preview(self,code=None):
        """
        查看公司的业务展望。
        """
        if code is not None:
            self.setcode(code)               
        df=wd.get_preview_qq(self.__code)
        text=list(df.iloc[0,0:])
        text='\n\n'.join(text)
        return text
    
    def pos_industry(self,code=None):
        """公司在同行业中的地位
        """
        if code is not None:
            self.setcode(code)               
        df=wd.comp2indu(self.__code)
        return df
        

    def research(self,code=None):
        """
        看研究分析员对目标公司的分析
        """
        if code is not None:
            self.setcode(code)               
        df=wd.get_reseachtext_qq(self.__code,n=5)
        return df

    def mgzb(self,code=None):
        """
        查看公司的每股指标数据
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
        """
        if code is not None:
            self.setcode(code)               
        df=wd.get_cwfx_qq(self.__code,mtype='mgzb')
        df=df.dropna(how='all',axis=1)
        return df

    def ylnl(self,code=None):
        """
        查看公司的盈利能力
           ylnl:
                 cbfylrl:成本费用利润率(%)
                 fjcxsybl:非经常性损益比率(%)
                 jlrkc:扣除非经常性损益后的净利润(元)
                 jzcsyljq:净资产收益率(加权)(%)
                 sxfyl:三项费用率(%)
                 xsjll:销售毛利率(%)
                 xsmll:销售毛利率(%)
                 xsqlr:息税前利润率(%)
                 xsqlrl:息税前利润率(%)
                 yylrl:营业利润率(%)
                 zzclrl:总资产利润率(%)
        """
        if code is not None:
            self.setcode(code)               
        df=wd.get_cwfx_qq(self.__code,mtype='ylnl')
        df=df.dropna(how='all',axis=1)
        return df        

    def yynl(self,code=None):
        """
        查看公司的营运能力
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
        """
        if code is not None:
            self.setcode(code)               
        df=wd.get_cwfx_qq(self.__code,mtype='yynl')
        df=df.dropna(how='all',axis=1)
        return df

    def cznl(self,code=None):
        """
        成长能力
           cznl:
                  jlr: 净利润增长率(%)
                  lrze: 利润总额增长率(%)
                  mgsy: 每股收益增长率(%)
                  mgxj: 每股现金流增长率(%)
                  xsqlr: 息税前利润增长率(%)
                  yylr: 营业利润增长率(%)
                  zysr: 主营收入增长率(%)
                  zzc:总资产增长率(%)
        """
        if code is not None:
            self.setcode(code)               
        df=wd.get_cwfx_qq(self.__code,mtype='cznl')
        df=df.dropna(how='all',axis=1)
        return df

    def djcw(self,code=None):
        """
        单季财务指标
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

        """
        if code is not None:
            self.setcode(code)               
        df=wd.get_cwfx_qq(self.__code,mtype='djcw')
        df=df.dropna(how='all',axis=1)
        return df        

    def czzb(self,code=None):
        """
        偿债及资本结构
          czzb:
                 cqbl: 产权比率(%)
                 czyzb: 长期债务与营运资金比率(%)
                 gdzcbl: 固定资产净值率(%)
                 gzjzl: 固定资产净值率(%
                 ldbl: 流动比率(%)
                 qsjzbl: 清算价值比率(%)
                 sdbl: 速动比率(%)
                 xjbl:现金比率(%)
                 zbgbbl: 资本固定化比率(%)
                 zbhbl: 资本化比率(%)
                 zcfzl: 资产负债率(%)
                 zzc:总资产(元)
        """
        if code is not None:
            self.setcode(code)               
        df=wd.get_cwfx_qq(self.__code,mtype='czzb')
        df=df.dropna(how='all',axis=1)
        return df
    
    def histcashfl(self,code=None):
        if code is not None:
            self.setcode(code)               
        if self.__cf is None:
            self.__cf=wd.driver_share_cashflow(self.__code).iloc[:,[2,4,6,8,10]]
            self.__cf=self.__cf.replace('',0)
            #self.__cf.columns=['ZLJLR','CDDJLR','DDJLR','ZDJLR','XDJLR']
        sm=self.__cf.iloc[-10:,]
        print('近10个交易日的交易数据:\n',sm,'\n',sm.sum())
        dd=self.__cf.iloc[-50:,:]
        fig, ax = plt.subplots(figsize=(9,5),dpi=100)
        #dd.plot(kind='bar',stacked=True,ax=ax)
        dd.plot(marker = 'o',ax=ax)
        # legend中显示中文
        #plt.legend(prop={'family':'SimHei','size':6},ax=ax)
        ax.legend(prop={'family':'SimHei','size':6})
        ax.xaxis.set_major_locator(years)
        ax.xaxis.set_major_formatter(yearsFmt)
        ax.xaxis.set_minor_locator(days)

        datemin=dd.index.date.min()
        datemax=dd.index.date.max()
        ax.set_xlim(datemax-datetime.timedelta(days=30), datemax)
        
        ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
        
        ax.axhline(lw=1)
        ax.set_ylabel(u'万元',fontproperties='SimHei',fontsize=6)
        #ylabel 显示中文
        ax.set_xlabel('date',fontsize=6)
        #ax.set_xticks(dd.index)
        #ax.set_xticklabels(dd.index.map(lambda x:str(x)[:10]))
        tt=dd.index.map(lambda x:str(x)[:10])
        dt=[tt[i] for i in range(len(dd)) if i%3==0]
        ax.set_xticks(dt)
        ax.set_xticklabels(dt,fontsize=6)
        ax.set_title('%s 近50个交易日现金流量图'%self.__code,fontproperties='SimHei')
        fig.autofmt_xdate()
        ax.grid()
        #plt.savefig('cash_flow_output.png',dpi=150)
        plt.show()
        

    def gcf(self,code=None):
        """
        获取股票的前100日交易日的数据
        """
        if code is not None:
            self.setcode(code)               
        if self.__cf is None:
            self.__cf=wd.driver_share_cashflow(self.__code).iloc[:,[2,4,6,8,10]]
            self.__cf=self.__cf.replace('',0)
            return self.__cf
        else:
            return self.__cf

    def cashflhy(self,code=None):
        """
        获取行业中前十大资金流入流出的资金情况
        """
        if code is not None:
            self.setcode(code)               
        df=wd.get_cashflhy_m163(self.__code)
        #df=df.sort_values(by='net_amount')
        return df
    
    def radar(self):
        if code is not None:
            self.setcode(code)               
        if self.__code[0] in ['6','9']:
            code='sh'+self.__code
        elif self.__code[0] in ['0','2','3']:
            code='sz'+self.__code
            
        url='http://stock.gtimg.cn/data/index.php?appn=radar&t={0}&d=00000000'.format(code)

        r=requests.get(url)
        text=r.content.decode('gbk').split(",data:'")[1].replace("^'};",'')
        text=text.replace('^','\n')
        text=text.replace('~',',')
        df=pd.read_csv(StringIO(text),header=None)
        return df        

    def cashmin(self,code=None):
        if code is not None:
            self.setcode(code)               
        df=wd.get_cashf_sharehist_min_EM(self.__code)
        df.loc[:,'net']=df.iloc[:,1]+df.iloc[:,2]+df.iloc[:,3]+df.iloc[:,4]
        return df

    def reportlist(self,code=None):
        if code is not None:
            self.setcode(code)               
        df=wd.get_reportlist_EM(self.__code)[["secuFullCode","rate","change","title","sys","syls","insName","author"]]
        return df

    def dxf(self,code=None):
        """查看公司的大小非解禁情况
        """
        if code is not None:
            self.setcode(code)               
        df=wd.get_TobefreeTrade_qq(code=self.__code,start='20160101')
        return df

    def dzjy(self,code=None):
        """查看公司的大宗交易情况
        """
        if code is not None:
            self.setcode(code)               
        df=wd.get_TobefreeTrade_qq(code=self.__code,start='20160101')
        return df



    def income(self,code=None,mtype='cp'):
        """查看公司的收入构成情况
        """
        if code is not None:
            self.setcode(code)           
        df=wd.get_income_composition_qq(self.__code,mtype)
        df=df.replace('--',np.nan)
        df=df.dropna(how='all',axis=1)
        df['pct']=df['Rev(10k)']/df['Rev(10k)'].sum()*100
        df['Rev.Profit']=df['Rev(10k)']-df['Cost']
        del df['code']
        return df

    def lhb(self,code=None,start='20000101',end='20180331'):
        """查看公司的龙虎榜情况
        """
        if code is not None:
            self.setcode(code)           
        df=wd.get_drogan_tiger_qq(self.__code,start=start,end=end)
        return df
    
    def conceptcash(self,code=None,mtype='hy'):
        if code is not None:
            self.setcode(code)           
        df=wd.get_cashf_concept_EM(mtype)
        #df=df.sort_values('Chg%')[['id', 'name', 'Chg%', 'Main.I.net','Su.I.net', 'Big.I.net',  'Mid.I.net',  'Sm.I.net', 'Sec_name', 'code']]
        df=df[['id', 'name', 'Chg%', 'Main.I.net','Su.I.net', 'Big.I.net',  'Mid.I.net',  'Sm.I.net', 'Sec_name', 'code']]
        df=df.set_index('id')
        #print(df.head(10))
        df['Main.I.net'].plot(kind='bar')
        plt.grid()
        plt.show()
        return df

    def conceptindex(self,code=None,year=2018,qt=1):
        """同业行业板块的上市公司股票"""
        if code is not None:
            self.setcode(code)           
        df=wd.get_cashf_alltoday_EM()[['name', 'price', 'Rank.T',\
                                       'Chg%.T','industry', 'indu.ID']]
        idd=df.loc[self.__code,'indu.ID']
        codeset=df[df['indu.ID']==idd].index.tolist()
        fs=wd.get_finance_index_EM(year,qt)
        dtset=pd.DataFrame()
        for code in codeset:
            try:
                dtset=dtset.append(fs.loc[code,:])
            except Exception as e:
                #print(e)
                pass

        dtset=dtset.sort_values(by=['roe','profit_yoy'],ascending=False)
        dtset=dtset.dropna(how='all',axis=1)
        dtset=dtset[[ 'name', 'margin', 'nav_ps',  'rev', 'rev_hb','profit', 'profit_hb', 'cf_ps', 'rev_yoy', 'profit_yoy','eps', 'eps_d','roe']]
        return dtset

    def conceptindex3y(self,code=None,year=2018,qt=1):
        """上市时间超过三年的股票        """
        if code is not None:
            self.setcode(code)           
        df=self.conceptindex(year,qt)

        #df=df[(df['roe']>8)&(df['profit_yoy']>20)&(df['margin']>20)]
        df=df[df['profit_yoy']>10]
        
        #df=df.set_index('code')
        try:
            ds=wd.get_stock_basic()
            #ds=ds.reset_index()
        except:
            if self.__alldata is None:
                self.readpkl()
            ds=self.__alldata
            #print(ds.head())
            ds=ds.drop_duplicates(subset=['code'],keep='last')
            ds=ds.set_index('code')
            
        today=datetime.datetime.today()
        dataset=pd.DataFrame()
        for code in df.index:
            try:
                days=(today-ds.loc[code,'timeToMarket']).days
                if days>1200:
                    try:
                        dataset=dataset.append(df.loc[code,:])
                    except:
                        pass
            except Exception as e:
                print(e)
                pass
        dataset=dataset[[ 'name', 'margin', 'nav_ps',  'rev', 'rev_hb','profit', 'profit_hb', 'cf_ps', 'rev_yoy', 'profit_yoy','eps', 'eps_d',  'roe']]
        return dataset

    def hynewEM(self,code=None):
        if code is not None:
            self.setcode(code)           
        df=wd.get_cashf_alltoday_EM()[['name', 'price', 'Rank.T',\
                                       'Chg%.T','industry', 'indu.ID']]
        hyid=df.loc[self.__code,'indu.ID'][3:6]

        url='http://stock.eastmoney.com/hangye/hy{}.html'.format(hyid)
        r=requests.get(url,headers=hds())
        try:
            text=r.content.decode('gbk')
        except:
            text=r.text
        html=lxml.html.parse(StringIO(text))
        dataset1=[]
    
        hyinfo=html.xpath('//div[@class="americaleft mt10"]/div[1]//div[@class="deta"]/ul/li')

        for hy in hyinfo:
            text=hy.xpath('a/text()')[0]
            print(text)
            href=hy.xpath('a/@href')[0]
            dataset1.append([text,href])

        df=pd.DataFrame(dataset1,columns=['title','href'])

        dataset=[]
        for url in df['href']:
            r=requests.get(url,headers=hds())
            #print(url)
            try:
                text=r.content.decode('utf8')
            except:
                text=r.text
            html=lxml.html.parse(StringIO(text))
            textc=html.xpath('//div[@id="ContentBody"]//text()')
            dataset.append('\n'.join(textc))

        data=[x.strip() for x in dataset]
        text='\n'.join(data)
        text=text.replace('\r','').replace(' ','')
        text1=re.sub(r'\n{1,}',r'\n\n',text)
        f=open('hynewsEM.txt','w')
        f.write(text1)
        f.close()
        return text1

    def vwmp(self,code=None,tp=1,ls=30,mt=None):
        """
        tp:1-表示当天的加权平均价格，2，便是在最近ls个交易日内的加权平均价格
        ls:最近的交易日
        """
        if code is not None:
            self.setcode(code)           
        if tp == 1:
            df=wd.get_dadan(self.__code)
            vpr=(df['amount'].sum()*100)/(df['volume'].sum())
            vpr= float('%.2f' %vpr)
            return vpr
        elif tp == 2:
            if self.__hdata is None:
                df=wd.get_h_data(self.__code,autype=mt,start='2015-01-01')
                self.__hdata=df
            else:
                df=self.__hdata
            df=df.sort_index()
            vpr=(df.iloc[-ls:,df.columns.get_loc('amount')].sum())/(df.iloc[-ls:,df.columns.get_loc('volume')].sum())
            vpr= float('%.2f' %vpr)
            #vpr=lambda x: '%.2f' %x
            return vpr
        else:
            print("Getting Error")

    def getBs(self,code=None):
        """
        获取公司的资产负债表
        """
        if code is not None:
            self.setcode(code)           
        if self.Bs is None:
            self.Bs=wd.BS_sina(self.__code)
            self.Bs=self.Bs.replace('--',np.nan).sort_index()
            self.Bs=self.Bs.applymap(lambda x:float(x))
        return

    def goodwill(self,code=None):
        """查看企业的商誉"""
        if code is not None:
            self.setcode(code)           
        if self.Bs is None:
            self.getBs()
        gw=self.Bs.loc[:,self.Bs.columns.str.contains("商誉")]
        return gw
    
    def payable(self,code=None):
        """查看企业的应付账款"""
        if code is not None:
            self.setcode(code)           
        if self.Bs is None:
            self.getBs()
        gw=self.Bs.loc[:,self.Bs.columns.str.contains("应付款")]
        return gw

    def receivable(self,code=None):
        """查看企业的应收账款"""
        if code is not None:
            self.setcode(code)           
        if self.Bs is None:
            self.getBs()
        gw=self.Bs.loc[:,self.Bs.columns.str.contains("应收款")]
        return gw
    
    def loan(self,code=None):
        """查看企业的借款、贷款"""
        if code is not None:
            self.setcode(code)           
        if self.Bs is None:
            self.getBs()
        gw=self.Bs.loc[:,self.Bs.columns.str.contains("借款")]
        gw1=self.Bs.loc[:,self.Bs.columns.str.contains("贷款")]
        gw=pd.concat([gw,gw1],axis=1)
        return gw        
    
    def getIs(self,code=None):
        """获取公司的利润表"""
        if code is not None:
            self.setcode(code)           
        if self.Is is None:
            self.Is=wd.IS_sina(self.__code)
            self.Is=self.Is.replace('--',np.nan).sort_index()
            self.Is=self.Is.applymap(lambda x:float(x))
        return
    
    def getCs(self,code=None):
        """获取公司的现金流量表"""
        if code is not None:
            self.setcode(code)           
        if self.Cs is None:
            self.Cs=wd.CS_sina(self.__code)
            self.Cs=self.Cs.replace('--',np.nan).sort_index()
            self.Cs=self.Cs.applymap(lambda x:float(x))

        return
    
    def printty(self):
        self.pepb()
        print(30*'--')
        self.fin_ths()
        print(30*'--')
        self.fin_sina()
        print(30*'--')
        self.MACD()
        print(30*'--')
        self.KDJ()
        print(30*'--')
        self.div()
        print(30*'--')
        self.holdbyinst()
        self.hynews()
        
        
if __name__=="__main__":
    aa=ASecurity(sys.argv[1])
