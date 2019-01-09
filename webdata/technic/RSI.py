#!/usr/bin/env python3
# -*-coding:utf-8-*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os,sys,time
import webdata.stock.trading as wt
import webdata.puse.quandldata as wq

def _position(stock_data):
    if (stock_data.iloc[-1]['Sign']==1)&(stock_data.iloc[-2]['Sign']==1):
        print ('持有这只股票Holding code')
    elif (stock_data.iloc[-1]['Sign']==1)&(stock_data.iloc[-2]['Sign']==0):
        print ('开始买进这只股票Buy code')
    elif (stock_data.iloc[-1]['Sign']==0)&(stock_data.iloc[-2]['Sign']==1):
        print ('开始卖出这只股票Sell code')
    else:
        print ('保持空仓Keeping Short Position code')
    return

def _RSI(df,label,window):
    df.loc[:,'diff']=df[label]-df[label].shift(1)
    df.loc[:,'plus']=df.loc[:,'diff']
    df['minus']=df['diff']
    N=df.shape[0]

    for i in range(N):
        if df.loc[i,'plus']<0:
            df.loc[i,'plus']=0
        if df.loc[i,'minus']>0:
            df.loc[i,'minus']=0

    df['S_plus']=pd.Series.rolling(df['plus'],window=window).sum()
    df['S_minus']=pd.Series.rolling(df['minus'],window=window).sum()

    df['RSI_%s'%window]=(df['S_plus']/(df['S_plus']-df['S_minus']))*100

    df=df.drop(['diff','plus','minus','S_plus','S_minus'],axis=1)
    return df
    
    

def RSIdf(df,label='Close',fee=0.0003,longd=26,shortd=12,plot=True):
    """
    """
    label=label.lower()
    df.columns=[str(x).lower() for x in df.columns]

    if 'p_change' not in df.columns:
        df['p_change']=df[label].pct_change()

    df=_RSI(df,label,shortd)
    df=_RSI(df,label,longd)

    buyi=df[(df['RSI_%s'%shortd]>df['RSI_%s'%longd])&(df['RSI_%s'%shortd].shift(-1)<df['RSI_%s'%longd].shift(-1))].index
    selli=df[(df['RSI_%s'%shortd]<df['RSI_%s'%longd])&(df['RSI_%s'%shortd].shift(-1)>df['RSI_%s'%longd].shift(-1))].index
    df.loc[buyi,'Sign']=0
    df.loc[selli,'Sign']=1
    df['Sign'].fillna(method='ffill',inplace=True)

    df['position']=df['Sign'].shift(1)

    df['Cash_ind']=(1+(df['p_change']-fee)*df['position']).cumprod()

    _position(df)
    
    if plot:
        fig=plt.figure(figsize=(10,5))
        fig.subplots_adjust(hspace=0.15, wspace=0.05,\
                            left=0.06,right=0.99,\
                            top=0.97,bottom=0.09)
    
        ax1=fig.add_subplot(311)
        df[label].plot(ax=ax1,label=label)
        plt.grid(True)
        labels = ax1.get_xticklabels()
        plt.setp(labels, rotation=45, fontsize=5)
        plt.legend()
        
        ax2=fig.add_subplot(312)
        df[['RSI_%s'%shortd,'RSI_%s'%longd]].plot(ax=ax2)
        plt.grid(True)
        labels = ax2.get_xticklabels()
        plt.setp(labels, rotation=45, fontsize=5)
        plt.legend()

        ax3=fig.add_subplot(313)
        df['Cash_ind'].plot(ax=ax3)
        plt.grid(True)
        labels = ax3.get_xticklabels()
        plt.setp(labels, rotation=45, fontsize=5)
        plt.legend()
    
        plt.show()
        
    return df

def RSIcode(code,label='Close',fee=0.0003,longd=26,shortd=12,plot=True):

    try:
        df=wt.get_k_data(code)
        RSIdf(df,label,fee,longd,shortd,plot)
    except:
        if len(code)==6:
            if code[0]=='0' or code[0]=='3':
                code='YAHOO/SZ_'+code
            elif code[0]=='6':
                code='YAHOO/SS_'+code
        elif len(code)==4:
            code='YAHOO/HK_'+code
        df=wq.quandlyd(code)
        RSIdf(df,label,fee,longd,shortd,plot)
    return

if __name__=="__main__":
    df=wt.get_k_data('000039')
    d=RSIdf(df)
    
