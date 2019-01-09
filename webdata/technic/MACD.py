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

def plott(df,label):
    fig=plt.figure(figsize=(10,5))
    fig.subplots_adjust(hspace=0.15, wspace=0.05,\
                        left=0.06,right=0.99,\
                        top=0.97,bottom=0.09)
    
    ax1=fig.add_subplot(411)
    df[label].plot(ax=ax1,label=label)
    plt.grid(True)
    labels = ax1.get_xticklabels()
    plt.setp(labels, rotation=45, fontsize=5)
    plt.legend()
    
    ax2=fig.add_subplot(412)
    df[['DIF','DEA']].plot(ax=ax2)
    plt.grid(True)
    labels = ax2.get_xticklabels()
    plt.setp(labels, rotation=45, fontsize=5)
    plt.legend()

    ax3=fig.add_subplot(413)
    df['Cash_ind'].plot(ax=ax3)
    plt.grid(True)
    labels = ax3.get_xticklabels()
    plt.setp(labels, rotation=45, fontsize=5)
    plt.legend()
    
    ax4=fig.add_subplot(414)
    df['Bar'].plot(kind='bar',ax=ax4)
    plt.grid(True)
    labels = ax4.get_xticklabels()
    plt.setp(labels, rotation=45, fontsize=5)
    plt.legend()
    
    plt.show()
    return

def MACDcode(code,label='Close',fee=0.0003,longd=26,shortd=12,difd=9,position='Case4',plot=True):
    """
    code:     上海交易所和深圳交易所的股票代码
    label:    Close
    fee:      手续费,0.0003
    longd:    慢周期，26
    shortd:   快周期，12
    difd:     DIF 的周期时间,9,
    position: 判断买入的方式,Case1 以位置,Case2 为交叉,Case3 MACD柱行图
    """
    try:
        df=wt.get_k_data(code)
        MACDdf(df,label,fee,longd,shortd,difd,position,plot)
    except:
        if len(code)==6:
            if code[0]=='0' or code[0]=='3':
                code='YAHOO/SZ_'+code
            elif code[0]=='6':
                code='YAHOO/SS_'+code
        elif len(code)==4:
            code='YAHOO/HK_'+code
        df=wq.quandlyd(code)
        MACDdf(df,label,fee,longd,shortd,difd,position,plot)
    return

def MACDdf(df,label='Close',fee=0.0003,longd=26,shortd=12,difd=9,position='Case4',plot=True):
    """
    df:       DataFrame
    label:    Close
    fee:      手续费,0.0003
    longd:    慢周期，26
    shortd:   快周期，12
    difd:     DIF 的周期时间,9,
    position: 判断买入的方式,Case1 以位置,Case2 为交叉,Case3 MACD柱行图
    """
    label=label.lower()
    df.columns=[str(x).lower() for x in df.columns]

    if 'p_change' not in df.columns:
        df['p_change']=df[label].pct_change()
    
    df['longd']=pd.Series.rolling(df[label],window=longd).mean()
    df['shortd']=pd.Series.rolling(df[label],window=shortd).mean()
    
    df['EMA_s']=(df['shortd'].shift(1)*(shortd-1)+df[label]*2)/(shortd+1)
    df['EMA_l']=(df['longd'].shift(1)*(longd-1)+df[label]*2)/(longd+1)
    df['DIF']=df['EMA_s']-df['EMA_l']
    df['EMA_dif']=pd.Series.rolling(df['DIF'],window=difd).mean()
    df['DEA']=(df['EMA_dif']*(difd-1)+df['DIF']*2)/(difd+1)
    df['Bar']=(df['DIF']-df['DEA'])*2

    if position=='Case1':
        #位置
        buyi=df[(df['DIF']>df['DIF'].shift(1))&\
                (df['DEA']>df['DEA'].shift(1))].index
        selli=df[(df['DIF']<df['DIF'].shift(1))&\
                 (df['DEA']<df['DEA'].shift(1))].index
        df.loc[buyi,'Sign']=1
        df.loc[selli,'Sign']=0

    elif position=='Case2':
        #交叉情况
        buyi=df[(df['DIF']>df['DIF'].shift(1))&\
                ((df['DIF'].shift(1)<df['DEA']) & \
                 (df['DIF']>df['DEA']))].index
        selli=df[(df['DIF']<df['DIF'].shift(1))&\
                 ((df['DIF'].shift(1)>df['DEA']) & \
                  (df['DIF']<df['DEA']))].index
        df.loc[buyi,'Sign']=1
        df.loc[selli,'Sign']=0

    elif position=='Case3': 
        #柱型图判断
        buyi=df[((df['Bar']>0) & (df['Bar']>df['Bar'].shift(1))) | \
                ((df['Bar']<0) & (df['Bar']>df['Bar'].shift(1))) | \
                ((df['Bar'].shift(1)<0) & (df['Bar']>0))].index
        selli=df[((df['Bar']<0) & (df['Bar']<df['Bar'].shift(1))) | \
                 ((df['Bar']>0) & (df['Bar']<df['Bar'].shift(1))) | \
                 ((df['Bar'].shift(1)>0 ) & ( df['Bar']<0))].index
        df.loc[buyi,'Sign']=1
        df.loc[selli,'Sign']=0

    elif position=='Case4':
        #交叉情况
        buyi=df[(df['DIF'].shift(-1)<df['DEA'].shift(-1)) & \
                 (df['DIF']>df['DEA'])].index
        selli=df[((df['DIF'].shift(-1)>df['DEA'].shift(-1)) & \
                  (df['DIF']<df['DEA']))].index
        df.loc[buyi,'Sign']=0
        df.loc[selli,'Sign']=1        
    
    df['Sign'].fillna(method='ffill',inplace=True)
    df['position']=df['Sign'].shift(1)

    df['Cash_ind']=(1+(df['p_change']-fee)*df['position']).cumprod()

    _position(df)
    
    df=df.set_index('date')

    if plot:
        plott(df,label)

    return

if __name__=="__main__":
    df=wt.get_k_data('601166')
    MACDdf(df,position='Case4')
    #MACDcode('601166')
    
