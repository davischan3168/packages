#!/usr/bin/env python3
# -*-coding:utf-8-*-
import matplotlib.pyplot as plt
import sys
import pandas as pd
import numpy as np
from matplotlib.dates import date2num
from matplotlib.dates import DateFormatter, WeekdayLocator, DayLocator, MONDAY
import webdata.puse.myapp as wd
import webdata.puse.quandldata as wq
import webdata.stock.trading as wt
import matplotlib as mpl

def MACDv2_code(code,label='Close',fee=0.0005,ld=26,sd=12, md=9,path='',plot=True,Wr=False):
    """
    code:为输入的股票代码，大陆的为6个数字代码，香港的为4个数字代码。
         like：string 600036,0005
    label：为所采用的列，open,high,close,low 或是Adj Close, Close
    ld,sd,md：为计算平均数的周期,以及dea 的计算周期
    fee:为交易的费率
    path:生成文件保存的地址及文件名，默认是不保存文件
    """
    if code ==None:
        sys.exit()
    elif isinstance(code,str):
        if len(code)==6:
            df=wt.get_k_data(code)
        elif len(code)==4:
            df=wq.quandlyd(code)
            df=df.iloc[-640:,]
            #print(df)
        else:
            sys.exit()
    
    #df=df.drop_duplicates()
    df.index=pd.to_datetime(df.index)
    #df=df.reset_index()
    df=df.rename(columns=lambda x: str(x).lower())
    label=label.lower()

    mondays = WeekdayLocator(MONDAY)
    alldays = DayLocator()  
    dayFormatter = DateFormatter('%d')
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    if df.index[-1] - df.index[0] < pd.Timedelta('730 days'):
        weekFormatter = DateFormatter('%b %d')  
        ax.xaxis.set_major_locator(mondays)
        ax.xaxis.set_minor_locator(alldays)
    else:
        weekFormatter = DateFormatter('%b %d, %Y')
    ax.xaxis.set_major_formatter(weekFormatter)
    ax.grid(True)    
    
    if 'p_change' not in df.columns:
        df.loc[:,'p_change']=df[label]/df[label].shift(1)-1
    dfi=df.shape[0]
    df.loc[0,'M_ld']=df.loc[0,label]
    df.loc[0,'M_sd']=df.loc[0,label]
    for i in range(1,dfi):
        df.loc[i:,'M_ld']=df.loc[i,label]*2/(ld+1)+df.loc[i-1,'M_ld']*(ld-1)/(ld+1)
        df.loc[i:,'M_sd']=df.loc[i,label]*2/(sd+1)+df.loc[i-1,'M_sd']*(sd-1)/(sd+1)
        
    df.loc[:,'DIF']=df['M_sd']-df['M_ld']
    df.loc[0,'DEA']=df.loc[0,'DIF']
    for i in range(1,dfi):
        df.loc[i,'DEA']=df.loc[i-1,'DEA']*(md-1)/(md+1)+df.loc[i,'DIF']*2/(md+1)
    

    df.loc[:,'BAR']=2*(df['DIF']-df['DEA'])

    buyi1=df[(df['DIF']>df['DEA'])&(df['DIF']>df['DIF'].shift(-1))].index
    df.loc[buyi1,'Sign'] = 0
    seli1=df[(df['DIF']<df['DEA'])&(df['DIF']<df['DIF'].shift(-1))].index
    df.loc[seli1,'Sign']=1

    
    df['Sign'].fillna(method='ffill',inplace=True)
   
    df.loc[:,'position']=df['Sign'].shift(1)
    df.loc[:,'Cash_index']=(1+(df['p_change']-fee)*df['position']).cumprod()
    df.loc[:,'vov']=pd.Series.rolling(df['p_change'],window=9).std()
    df=df.set_index('date')

    _position_code(df,code)

    
    if plot:
        fig=plt.figure(figsize=(9,5))
        fig.subplots_adjust(hspace=0.15, wspace=0.05,\
                            left=0.06,right=0.99,\
                            top=0.97,bottom=0.09)
        ax1=fig.add_subplot(411)
        df[label].plot(ax=ax1)
        plt.grid(True)
        
        ax2=fig.add_subplot(412)
        df['Cash_index'].plot(ax=ax2)
        plt.grid(True)
        
        ax3=fig.add_subplot(413)
        df[['p_change','vov']].plot(ax=ax3)
        plt.grid(True)
        
        ax4=fig.add_subplot(414)
        df['BAR'].plot(kind='bar',ax=ax4)
        
        ax5=ax4.twinx()
        df[['DIF','DEA']].plot(kind='line',ax=ax4)
        plt.grid(True)

        """
        monthsLoc = mpl.dates.MonthLocator()
        weeksLoc = mpl.dates.WeekdayLocator()
        ax4.xaxis.set_major_locator(monthsLoc)
        ax4.xaxis.set_minor_locator(weeksLoc)
        monthsFmt = mpl.dates.DateFormatter('%b')
        ax4.xaxis.set_major_formatter(monthsFmt)"""
        plt.show()
    if path !='':
        df.to_csv(path)
    return 

if __name__=="__main__":
    MACDv2_code(sys.argv[1])
