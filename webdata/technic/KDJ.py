#!/usr/bin/env python3
# -*-coding:utf-8-*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os,sys,time
import webdata.stock.trading as wt
import webdata.puse.quandldata as wq

"""
以这种方式计算的KDJ指标测试不理想，收益率是负数
"""

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

def KDJdf(df,label='Close',fee=0.0003,window=5,plot=True):
    """
    df:       DataFrame
    label:    Close
    fee:      手续费,0.0003
    shortd:   快周期，12
    position: 判断买入的方式,Case1 以位置,Case2 为交叉,Case3 MACD柱行图
    """
    label=label.lower()
    df.columns=[str(x).lower() for x in df.columns]

    if 'p_change' not in df.columns:
        df['p_change']=df[label].pct_change()
    
    df['H']=pd.Series.rolling(df['high'],window=window).max()
    df['L']=pd.Series.rolling(df['low'],window=window).min()
    df['RSV']=(df[label]-df['L'])/(df['H']-df['L'])*100
    
    N=df.shape[0]

    df.loc[0:window,'K']=50
    df.loc[0:window,'D']=50

    for i in range(window-1,N,1):
        df.ix[i,'K']=(2*df.ix[i-1,'K']+df.ix[i,'RSV'])/3
        df.ix[i,'D']=(2*df.ix[i-1,'D']+df.ix[i,'K'])/3
    df['J']=3*df['D']-2*df['K']
    """
    buyi=df[(df['K']>df['D'])&(df['K'].shift(1)<df['D'])&\
             (df['K']>df['K'].shift(1))&(df['D']>df['D'].shift(1))].index
    selli=df[(df['K']<df['D'])&(df['K'].shift(1)>df['D'])&\
             (df['K']<df['K'].shift(1))&(df['D']<df['D'].shift(1))].index
    """
    buyi=df[(df['K']>df['D'])&(df['K'].shift(-1)<df['D'].shift(-1))].index
    selli=df[(df['K']<df['D'])&(df['K'].shift(-1)>df['D'].shift(-1))].index
    
    df.loc[buyi,'Sign']=0
    df.loc[selli,'Sign']=1

    
    df['Sign'].fillna(method='ffill',inplace=True)
    df['position']=df['Sign'].shift(1)

    df['Cash_ind']=(1+(df['p_change']-fee)*df['position']).cumprod()

    _position(df)
    
    df=df.set_index('date')

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
        df[['K','D']].plot(ax=ax2)
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
    return

def KDJcode(code,label='Close',fee=0.0003,window=5,plot=True):
    """
    """
    if len(code)==6:
        if code[0] in ['0','3','2','6','9']:
            df=wt.get_k_data(code)
            KDJdf(df,label,fee,window,plot)
        else:
            sys.exit()
    elif len(code)==4:
        code='YAHOO/HK_'+code
        df=wq.quandlyd(code)
        KDJdf(df,label,fee,window,plot)
    return

    
            

if __name__=="__main__":
    #df=wt.get_k_data('000039')
    #MACDdf(df,position='Case2')
    #kk=KDJdf(df)
    KDJcode('000039')
    
