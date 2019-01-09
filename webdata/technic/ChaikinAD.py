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

def ChaikinADdf(df="",label='Close',fee=0.0005, M=5, N=10, path='',plot=True):
    
    df=df.sort_index(ascending=True)
    df=df.drop_duplicates()    
    df=df.reset_index()
    df=df.rename(columns=lambda x: str(x).lower())
    label=label.lower()
    if 'p_change' not in df.columns:
        df.loc[:,'p_change']=df[label]/df[label].shift(1)-1

    df.loc[:,'volume_log']=df['volume'].apply(np.log10)

    df.loc[:,'AD_%s'%M]=pd.Series.rolling((2*df[label]-df['high']-df['low'])/(df['high']-df['low'])*df['volume_log'],window=M).mean()
    df.loc[:,'AD_%s'%N]=pd.Series.rolling((2*df[label]-df['high']-df['low'])/(df['high']-df['low'])*df['volume_log'],window=N).mean()
    df.loc[:,'Chaikin']=df['AD_%s'%M]-df['AD_%s'%N]

    #buyi=df[(df['Chaikin'] > df['Chaikin'].shift(1))|((df['Chaikin']>0) & (df['Chaikin'].shift(1)<0))].index
    #buyi=df[(df['Chaikin'] > df['Chaikin'].shift(1))].index
    buyi=df[(df['Chaikin'] < df['Chaikin'].shift(-1))].index
    df.loc[buyi,'Sign']=1
    #selli=df[(df['Chaikin']<df['Chaikin'].shift(1))|((df['Chaikin']<0)&(df['Chaikin'].shift(1)>0))].index
    #selli=df[(df['Chaikin']<df['Chaikin'].shift(1))].index
    selli=df[(df['Chaikin']>df['Chaikin'].shift(-1))].index
    df.loc[selli,'Sign']=0
    df['Sign'].fillna(method='ffill',inplace=True)
    df.loc[:,'position']=df['Sign'].shift(1)
    df.loc[:,'Cash_index']=(1+(df['p_change']-fee)*df['position']).cumprod()

    df.loc[:,'vov']=pd.Series.rolling(df['p_change'],M).std()

    _position(df)
    
    df=df.set_index('date')
    #print(df.tail())
    if plot:
        fig=plt.figure(figsize=(9,5))
        fig.subplots_adjust(hspace=0.15, wspace=0.05,\
                            left=0.06,right=0.99,\
                            top=0.97,bottom=0.09)        

        ax1=fig.add_subplot(411)
        df['close'].plot(ax=ax1)
        plt.grid(True)
        labels = ax1.get_xticklabels()
        plt.setp(labels, rotation=45, fontsize=8)
        plt.legend()        

        ax2=fig.add_subplot(412)
        df[['AD_%s'%M,'AD_%s'%N]].plot(ax=ax2)
        plt.grid(True)
        labels = ax2.get_xticklabels()
        plt.setp(labels, rotation=45, fontsize=8)
        plt.legend()        
        
        ax3=fig.add_subplot(413)
        df['Cash_index'].plot(ax=ax3)
        plt.grid(True)
        labels = ax3.get_xticklabels()
        plt.setp(labels, rotation=45, fontsize=8)
        plt.legend()        

        ax4=fig.add_subplot(414)
        df['vov'].plot(ax=ax4)
        plt.grid(True)
        labels = ax4.get_xticklabels()
        plt.setp(labels, rotation=45, fontsize=8)
        plt.legend()        
        
        plt.show()

    return df



def ChaikinADcode(code,label='Close',fee=0.0005, M=5, N=10, path='',plot=True):

    try:
        df=wt.get_k_data(code)
        d=ChaikinADdf(df,label,fee,M,N,path,plot)
    except:
        if len(code)==6:
            if code[0]=='0' or code[0]=='3':
                code='YAHOO/SZ_'+code
            elif code[0]=='6':
                code='YAHOO/SS_'+code
        elif len(code)==4:
            code='YAHOO/HK_'+code
        df=wq.quandlyd(code)
        d=ChaikinADdf(df,label,fee,M,N,path,plot)
    return

if __name__=="__main__":
    df=wt.get_k_data('000039')
    d=ChaikinADdf(df)
    
