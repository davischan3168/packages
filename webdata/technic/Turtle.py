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

def Tutledf(df=None,label='Close',N1=20,N2=10,fee=0.0005,path='',plot=True):
    """
    df:为输入的DataFrame数据
    label：为所采用的列，open,high,close,low 或是Adj Close
    N1,N2：为计算平均数的周期
    fee:为交易的费率
    path:生成文件保存的地址及文件名，默认是不保存文件
    """
    if df is None:
        sys.exit()
    if isinstance(df,pd.DataFrame):

        # 保留这几个需要的字段：'date', 'high', 'low', 'close', 'change'
        df=_pre_set_df(df,label)
        df = df[['date','open', 'high', 'low', label, 'p_change']]
    
        df.loc[:,'High_Close_Price_N1_Day'] =  pd.Series.rolling(df['high'],window=N1,center=False).max()
        df['High_Close_Price_N1_Day'].fillna(value=df['high'].expanding(min_periods=1).max())
        df.loc[:,'Low_Close_Price_N2_Day'] =  pd.Series.rolling(df['low'],window=N2,center=False).min()
        df['Low_Close_Price_N2_Day'].fillna(value=df['low'].expanding(min_periods=1).min())
        #df['Low_Close_Price_N2_Day']=df['Low_Close_Price_N2_Day'].shift()
        # 当当天的【close】> 昨天的【最近N1个交易日的最高点】时，将【收盘发出的信号】设定为1
        buy_index = df[df['close'] > df['High_Close_Price_N1_Day'].shift(1)].index
        df.loc[buy_index, 'Signal'] = 1
        # 当当天的【close】< 昨天的【最近N2个交易日的最低点】时，将【收盘发出的信号】设定为0
        sell_index = df[df['close'] < df['Low_Close_Price_N2_Day'].shift(1)].index
        df.loc[sell_index, 'Signal'] = 0
        # 计算每天的仓位，当天持有上证指数时，仓位为1，当天不持有上证指数时，仓位为0
        df['position'] = df['Signal'].shift(1)
        df['position'].fillna(method='ffill', inplace=True)
        #当仓位为1时，已当天的开盘价买入股票，当仓位为0时，以收盘价卖出该股份。计算从数据期内的收益
        df['Cash_index'] = ((df['p_change']/100-fee) * df['position'] + 1.0).cumprod()
        #initial_idx = df.iloc[0]['close'] / (1 + (df.iloc[0]['p_change']/100))
        initial_idx = 1
        df['Cash_index'] *= initial_idx
        _position(df)

        #print ('The turtle methon Signal:')
        if path != '':
            df.to_csv(path)
        # ==========计算每年指数的收益以及海龟交易法则的收益
        df['p_change_turtle'] = (df['p_change']) * df['position']
        df=df.reset_index(drop=True)
        df=df.set_index('date')
        if plot:
            df[[label,'p_change','Cash_index']].plot(subplots=True,figsize=(9,5))
            plt.grid(True)
            plt.show()    
    return df
    



def Tutlecode(code,label='Close',N1=20,N2=10,fee=0.0005,path='',plot=True):

    try:
        df=wt.get_k_data(code)
        d=Tutledf(df,label,N1,N2,fee,path,plot)
    except:
        if len(code)==6:
            if code[0]=='0' or code[0]=='3':
                code='YAHOO/SZ_'+code
            elif code[0]=='6':
                code='YAHOO/SS_'+code
        elif len(code)==4:
            code='YAHOO/HK_'+code
        df=wq.quandlyd(code)
        d=Tutledf(df,label,N1,N2,fee,path,plot)
    return

if __name__=="__main__":
    df=wt.get_k_data('000039')
    d=RSIdf(df)
    
