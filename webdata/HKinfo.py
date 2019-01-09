#!/usr/bin/env python3
# -*-coding:utf-8-*-
import pandas as pd
import numpy as np
import webdata as wd
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import abc,datetime
import pickle,sys,re
from matplotlib.font_manager import FontProperties
#font = FontProperties(fname=r"C:\\WINDOWS\\Fonts\\simsun.ttc", size=8)

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
days = mdates.DayLocator()
yearsFmt = mdates.DateFormatter('%m')

s1=re.compile(r'\d+股合併為\d+股|\d+股供\d+股', re.UNICODE)

def pgplott(df):
    dd=df.groupby(['Type','Price'])['Volume'].sum()
    d=dd.unstack().T
    fig=plt.figure(figsize=(10,5))
    fig.subplots_adjust(hspace=0.15, wspace=0.05,left=0.10,right=0.99,top=0.97,bottom=0.09)
    ax1=fig.add_subplot(311)
    d['A'].plot(kind='bar',ax=ax1,label='buy')
    plt.grid(True)
    labels = ax1.get_xticklabels()
    plt.setp(labels, rotation=45, fontsize=5)#,visual=False)
    plt.legend()
    ax2=fig.add_subplot(312)
    d['B'].plot(kind='bar',ax=ax2,label='sell')#,visual=False)
    plt.grid(True)
    labels = ax2.get_xticklabels()
    ax2.set_ylabel("Volume")
    plt.setp(labels, rotation=45, fontsize=5)
    plt.legend()
    
    try:
        ax3=fig.add_subplot(313)
        d['U'].plot(kind='bar',ax=ax3,label='unkown')
        plt.grid(True)
        labels = ax3.get_xticklabels()
        plt.setp(labels, rotation=45, fontsize=8)
        plt.legend()
    except:
        pass
    
    plt.show()
    return

class HKSecurity(object):
    def __init__(self,code=None,m=12,n=6,md=3,\
                     window=5,start='2016-12-31',end='2017-03-31'):
        self.__ld=m
        self.__sd=n
        self.__md=md
        self.__window=window
        self.__st=start
        self.__end=end
        self.__code=code
        self.__trade_data=None
        self.__tick=None
        self.__review=None
        self.__freview=None
        self.__tL=None
        self.__mypeer=None

    def setcode(self,code):
        if isinstance(code,str):
            self.__code=code
            self.__trade_data=None
            self.__review=None
            self.__freview=None
            self.__tL=None
            self.__mypeer=None

    def basic_info(self,code=None):
        """
        获取公司的基本信息
        
        """
        if code is not None:
            self.setcode(code)
            
        df=wd.HK_basic_info_AAS(self.__code,'company-profile')
        text=df.iloc[4,1]
        return text

    def Future(self,code=None):
        if code is not None:
            self.setcode(code)
            
        df=wd.HK_Preview_EM(self.__code)
        d=list(wd.HK_Preview_EM(self.__code).iloc[0:8,1])
        text='\n'.join(d)
        return text
        
    def dividens(self,code=None):
        """
        获取公司的分红记录
        """
        if code is not None:
            self.setcode(code)        
        df=wd.HK_divs_AAST(self.__code)#[['Date','Items','Particular','Payable Date']]
        #df=df.set_index('Date')
        #df=df.sort_index()
        #text=''.join(df.loc[:,'Particular'].tolist())
        #t=s1.findall(text)
        #if len(t)>0:
        #    print(t)
        return df#,t

    def tradeLog(self,url):
        """
        每一笔的交易明细
        """
        self.tL=wd.HK_TradeLog_AAS(url)
        pgplott(self.tL)
        return self.tL

    def tick(self,code=None):
        if code is not None:
            self.setcode(code)        
        self.__tick=wd.HK_tick_AAST(self.__code)
        return self.__tick
        
        
    def cashfl(self,code=None):
        """
        获取公司股票交易的现金流情况
        """
        if code is not None:
            self.setcode(code)        
        df=wd.HK_cashfl_AAST(self.__code)
        return df

    def fin_index(self,code=None):
        """
        获取公司的主要财务指标数据
        """
        if code is not None:
            self.setcode(code)        
        df=wd.HK_earsummary_data_AAST(self.__code)
        del df['Currency']
        del df['Currency Conversion']
        return df

    def peer(self,code=None):
        """
        获取同行业公司的财务数据
        """
        if code is not None:
            self.setcode(code)        
        df=wd.HK_peer_AAS(self.__code,1)
        df=df.dropna(how='any',axis=0)
        self.__mypeer=df.dropna(how='any',axis=1)
        return self.__mypeer

    def hold_inst(self,code=None):
        """
        机构持股变动情况
        """
        if code is not None:
            self.setcode(code)        
        df=wd.HK_inst_qq(self.__code)
        return df

    def FinanceS(self,code=None):
        """
        查询公司的财务指标分析摘要
        """
        if code is not None:
            self.setcode(code)        
        df=wd.HK_Summary_EM(self.__code)
        df=df.sort_index(axis=1)        
        return df

    def EpsIndex(self,code=None):
        """
        查询公司的每股指标
        """
        if code is not None:
            self.setcode(code)        
        df=wd.HK_EPS_Index_EM(self.__code)
        df=df.sort_index(axis=1)
        df=df.replace('-',np.nan)
        df=df.dropna(how='all',axis=0)        
        return df

    def ProfitQ(self,code=None):
        """盈利能力和收益质量
        """
        df=wd.HK_Profit_Quantity_EM(self.__code)
        df=df.sort_index(axis=1)
        df=df.replace('-',np.nan)
        df=df.dropna(how='all',axis=0)        
        return df

    def Zbjg(self,code=None):
        """资本结构与偿债能力
        """
        if code is not None:
            self.setcode(code)        
        df=wd.HK_Captital_Repay_EM(self.__code)
        df=df.sort_index(axis=1)
        df=df.replace('-',np.nan)
        df=df.dropna(how='all',axis=0)        
        return df

    def Cznl(self,code=None):
        """成长能力
        """
        if code is not None:
            self.setcode(code)        
        df=wd.HK_Grow_Ability_EM(self.__code)
        df=df.sort_index(axis=1)
        df=df.replace('-',np.nan)
        df=df.dropna(how='all',axis=0)
        df=df[['基本每股收益同比增长率(%)','毛利同比增长率(%)','税前利润同比增长率(%)', '股东权益合计同比增长率(%)', '营业利润同比增长率(%)', '营业收入同比增长率(%)']]
        return df
    
    
    def buy_back(self,code=None):
        """
        上市公司回购股份情况
        """
        df=wd.HK_buyback_data_AAST(self.__code)
        return df

    def Assanl(self,code=None):
        """价值估算分析
        """
        if code is not None:
            self.setcode(code)        
        dd=wd.HK_Value_Ass_EM(self.__code)
        dd=dd.set_index('IndexName')
        dd=dd.dropna(how='all',axis=0)
        #dd=dd.drop(['市盈率(PE,TTM)','市盈率(PE,LYR)','市净率(PB,MRQ)','市净率(PB,LYR)','市销率(PS,TTM)','市现率(PCF,TTM)','市现率(PCF,LYR)'],axis=1)
        
        dd=dd.T
        return dd
    
    def InvestRating(self,code=None):
        """投资评级
        """
        if code is not None:
            self.setcode(code)        
        df=wd.HK_Invest_Rating_qq(self.__code)

        try:
            df=df.loc[:,['DEPARTMENT_NAME',\
                         'AIM_PRICE','EVA_RANK',\
                         'FORE_IS_INCRES', \
                         'FORE_RANK_IS_INCRES']]
            return df
        except Exception as e:
            print(e)
        
    def news(self,code=None):
        """
        有关上市公司的新闻资讯
        """
        if code is not None:
            self.setcode(code)        
        df=wd.HK_news_AAS(self.__code)
        return df
    
    def notice(self,code=None):
        """
        有关上市公司的公告资讯
        """
        if code is not None:
            self.setcode(code)        
        df=wd.HK_notice_qq(self.__code)[['symbol', 'time','title']]
        return df

    def pepb(self,code=None):
        if code is not None:
            self.setcode(code)        
        if self.__mypeer is None:
            self.peer()
        df=self.__mypeer
        PE=df.loc[self.__code,'P/E(x)']
        PB=df.loc[self.__code,'P/B(x)']
        dd=wd.HK_peer_AAS(self.__code,4)
        ROA=dd.loc[self.__code,'ROA']
        ROE=dd.loc[self.__code,'ROE']
        d6=wd.HK_peer_AAS(self.__code,6)
        Rev=d6.loc[self.__code,'Revenue']
        Rev_yoy=d6.loc[self.__code,'R. Growth YOY']
        OPM=d6.loc[self.__code,'Operating P. Margin']
        EPS=d6.loc[self.__code,'EPS']
        EPS_yoy=d6.loc[self.__code,'EPS Growth YOY(%)']
        NPM=d6.loc[self.__code,'NP Margin']
        Price=d6.loc[self.__code,'Last']
        MC=df.loc[self.__code,'Market Cap']
        PEG=PE/EPS_yoy
        try:
            PS=MC/Rev
            text1='%s, Price is %.2f, PE is %.2f, EPS_yoy is %s, PEG is %.2f,\n PB is %.2f, Rev_yoy is %.2f'%( self.__code,Price,PE,EPS_yoy,PEG,PB,Rev_yoy)
            text2='ROA is %.2f, ROE is %.2f, PS is %.2f'%(ROA,ROE,PS)
        except:
            text1='The Price is %.2f, PE is %.2f, EPS_yoy is %s, PEG is %.2f,\n PB is %.2f, Rev_yoy is %.2f'%( Price,PE,EPS_yoy,PEG,PB,Rev_yoy)
            text2='ROA is %.2f, ROE is %.2f'%(ROA,ROE)
        
        text= text1+'\n'+text2
        return text
        
        
    def trade(self,code=None):
        if code is not None:
            self.setcode(code)        
        df=wd.HK_trade_data_EM(self.__code)[['CHG', 'HIGH', 'LOW', 'NEW',\
                                             'OPEN', 'PCHG','TNUM']]
        df['date']=df.index
        self.__trade_data=df
        return self.__trade_data

    def MACD(self,code=None):
        if code is not None:
            self.setcode(code)        
        try:
            if self.__trade_data is None:
                self.trade()
        except:
            pass
        df=wd.MACDv1_df(self.__trade_data.iloc[-760:,:],label='NEW',ld=self.__ld,sd=self.__sd,md=self.__md)

    def KDJ(self,code=None):
        if code is not None:
            self.setcode(code)        
        try:
            if self.__trade_data is None:
                self.trade()
        except:
            pass
        #dd=self.__trade_data.iloc[-760:,:]
        df=wd.KDJv1_df(self.__trade_data.iloc[-760:,:],label='New',window=self.__window)
    
if __name__=="__main__":
    hk=HKSecurity(sys.argv[1])
