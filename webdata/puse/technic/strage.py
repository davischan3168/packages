#!/usr/bin/env python3
# -*-coding:utf-8-*-

import pandas as pd
import numpy as np
import sys
import matplotlib.pyplot as plt
import webdata.puse.myapp as wd
import webdata.puse.quandldata as wq
import webdata.stock.trading as wt
import matplotlib as mpl
import pickle

def _write_file(c,m='a'):
    f=open('buy_code.txt',m)
    f.write(c+'\n')
    f.flush()

def _position_code(stock_data,code,W=False):
    if (stock_data.iloc[-1]['Sign']==1)&(stock_data.iloc[-2]['Sign']==1):
        print ('持有这只股票Holding code %s'%code)
    elif (stock_data.iloc[-1]['Sign']==1)&(stock_data.iloc[-2]['Sign']==0):
        print ('开始买进这只股票Buy code %s'%code)
        if W:
            _write_file(code)
    elif (stock_data.iloc[-1]['Sign']==0)&(stock_data.iloc[-2]['Sign']==1):
        print ('开始卖出这只股票Sell code %s'%code)
    else:
        print ('保持空仓Keeping Short Position code %s' %code)
    return

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

def EMWA_STD(df,label='Close',window=12,times=1.5,fee=0.0005,path='',plot=True):
    """
    输入参数：
    df：为DataFrame数据类型，为股票的交易数据
    label：为所采用的列，open,high,close,low 或是Adj Close
    window：为计算平均数的周期
    times：为移动平均数的倍数
    fee：为交易的费率
    path:生成文件保存的地址及文件名，默认是不保存文件
    """
    if isinstance(df,pd.DataFrame):
        df=df.sort_index(ascending=True)
        df=df.drop_duplicates()
        df=df.reset_index()
        df=df.rename(columns=lambda x: str(x).lower())
        label=label.lower()        
        df.loc[:,'emwa']=pd.Series.rolling(df[label],window=window,center=False,min_periods=0).mean()
        df.loc[:,'std']=pd.Series.rolling(df[label],window=window).std()
        
        df.loc[:,'up']=df['emwa']+times*df['std']
        df.loc[:,'down']=df['emwa']-times*df['std']
        buyi=df[df['close']<df['down']].index
        df.loc[buyi,'Sign']=0
        #表示不再持仓            
        seli=df[df['close']>df['up']].index
        df.loc[seli,'Sign']=1
        #表示可以持仓，在第一次改为1时，表示买进
        df['Sign'].fillna(method='ffill',inplace=True)
        dfi=df.shape[0]
        if df.ix[dfi-2,'Sign']==0 and df.ix[dfi-1,'Sign']==1:
            print("\n the share Can be buy.")
        elif df.ix[dfi-2,'Sign']==1 and df.ix[dfi-1,'Sign']==0:
            print("\n The share can be sell.")
        df['position']=df['Sign'].shift(1) #交易的费率，为万分之8.5
        df['ptc']=df['close']/df['close'].shift(1)-1
        df['cash_index']=(1+(df['ptc']-fee)*df['position']).cumprod()
        df['vov']=pd.Series.rolling(df['ptc'],window=window,center=False).std()
        df=df.set_index('date')
        if path != '':
            df.to_csv(path)
        #print(df.tail(2))
        if plot:
            fig=plt.figure(figsize=(10,6),grid=True)
            ax1=fig.add_subplot(311)
            df[[label,'up','down','emwa']].plot(kind='line',ax=ax1)
            plt.grid(True)
            ax2=fig.add_subplot(312)
            df[['ptc','vov']].plot(kind='line',ax=ax2)
            plt.grid(True)
            ax3=fig.add_subplot(313)
            df['cash_index'].plot(kind='line')
            plt.grid(True)
            plt.show()
    return

def KDJv1_df(df=None,label='close',window=9,fee=0.0005,path='',plot=True):
    """
    df:为输入的DataFrame数据
    label：为所采用的列，open,high,close,low 或是Adj Close
    window：为计算平均数的周期
    fee:为交易的费率
    path:生成文件保存的地址及文件名，默认是不保存文件

    """
    if df is None:
        sys.exit()
    
    if isinstance(df,pd.DataFrame):
        df=df.sort_index(ascending=True)
        df=df.drop_duplicates()
        try:
            df=df.drop('date',axis=1)
        except:
            pass
        df=df.reset_index()
        df=df.rename(columns=lambda x: str(x).lower())
        label=label.lower()
        stock_dataT=df

        if 'p_change' not in df.columns:
            stock_dataT['p_change']=(stock_dataT[label]/stock_dataT[label].shift(1)-1)*100
        stock_data=stock_dataT.loc[:,('date', 'high', 'low', label,'p_change')].copy()
        # 计算KDJ指标
        stock_data['low_list'] = pd.Series.rolling(stock_data['low'],window=window,center=False).min()
        stock_data['low_list'].fillna(value=stock_data['low'].expanding(min_periods=1).min())
        stock_data['high_list']=pd.Series.rolling(stock_data['high'],window=window,center=False).max()
        stock_data['high_list'].fillna(value=stock_data['high'].expanding(min_periods=1).max())
        stock_data['rsv'] = (stock_data[label] - stock_data['low_list']) / (stock_data['high_list'] - stock_data['low_list']) * 100
        stock_data['KDJ_K'] = pd.Series.ewm(stock_data['rsv'],ignore_na=False,min_periods=0,adjust=True,com=2).mean()
        stock_data['KDJ_D'] = pd.Series.ewm(stock_data['KDJ_K'],ignore_na=False,min_periods=0,adjust=True,com=2).mean()
        stock_data['KDJ_J'] = 3 * stock_data['KDJ_K'] - 2 * stock_data['KDJ_D']
        # 计算KDJ指标金叉、死叉情况
        ###通常就敏感性而言，J值最强，K值次之，D值最慢，而就安全性而言，J值最差，K值次之，D值最稳
        ##金叉用1表示，死叉用0表示
        buyi=stock_data[(stock_data['KDJ_K'] > stock_data['KDJ_D'])&(stock_data['KDJ_K'].shift(-1) < stock_data['KDJ_D'].shift(-1))].index
        stock_data.loc[buyi,'Sign'] = 0
        selli=stock_data[(stock_data['KDJ_K'] < stock_data['KDJ_D'])&(stock_data['KDJ_K'].shift(-1) > stock_data['KDJ_D'].shift(-1))].index
        stock_data.loc[selli,'Sign'] = 1
        stock_data['Sign'].fillna(method='ffill', inplace=True)
        ##测试反向操作的效果，即买进信号则卖出，卖出信号则买进。
        stock_data['position']=stock_data['Sign'].shift(1)
        #stock_data['position'].fillna(method='ffill', inplace=True)
        #当仓位为1时，已当天的开盘价买入股票，当仓位为0时，以收盘价卖出该股份。计算从数据期内的收益
        stock_data['Cash_index'] = ((stock_data['p_change']/100  -fee) * \
                                    stock_data['position']+1).cumprod()
        #initial_idx = stock_data.iloc[0]['close'] / (1 + (stock_data.iloc[0]['p_change']/100))
        initial_idx = 1
        stock_data['Cash_index'] *= initial_idx

        stock_data=stock_data.set_index('date')
        _position(stock_data)
        """
        if (stock_data.iloc[-1]['position']==1)&(stock_data.iloc[-2]['position']==1):
            print ('持有这只股票Holding code')
        elif (stock_data.iloc[-1]['position']==1)&(stock_data.iloc[-2]['position']==0):
            print ('开始买进这只股票Buy code')
        elif (stock_data.iloc[-1]['position']==0)&(stock_data.iloc[-2]['position']==1):
            print ('开始卖出这只股票Sell code')
        else:
            print ('保持空仓Keeping Short Position code')
        """
    
        if path != '':
            stock_data.to_csv(path)
        stock_data['vov']=pd.Series.rolling(stock_data['p_change'],window=window,center=False).std()
        if plot:
            stock_data[[label,'p_change','vov','Cash_index']].plot(subplots=True,figsize=(9,5),grid=True)
            plt.grid(True)
            plt.show()            
        return stock_data
        
def KDJv2_code(code=None,label='close',window=9,fee=0.0005,path='',plot=True,Wr=False):
    """
    code:为输入的股份代码，6位的为境内的代码，4位的为香港的代码
    label：为所采用的列，open,high,close,low 或是Adj Close
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
            
    if isinstance(df,pd.DataFrame):
        df=df.sort_index(ascending=True)
        df=df.drop_duplicates()
        df=df.reset_index()
        df=df.rename(columns=lambda x: str(x).lower())
        label=label.lower()
        stock_dataT=df

        if 'p_change' not in df.columns:
            stock_dataT['p_change']=(stock_dataT[label]/stock_dataT[label].shift(1)-1)*100
        stock_data=stock_dataT.loc[:,('date', 'high', 'low', label,'p_change')].copy()
        # 计算KDJ指标
        stock_data['low_list'] = pd.Series.rolling(stock_data['low'],window=window,center=False).min()
        stock_data['low_list'].fillna(value=stock_data['low'].expanding(min_periods=1).min())
        stock_data['high_list']=pd.Series.rolling(stock_data['high'],window=window,center=False).max()
        stock_data['high_list'].fillna(value=stock_data['high'].expanding(min_periods=1).max())
        stock_data['rsv'] = (stock_data[label] - stock_data['low_list']) / (stock_data['high_list'] - stock_data['low_list']) * 100
        stock_data['KDJ_K'] = pd.Series.ewm(stock_data['rsv'],ignore_na=False,min_periods=0,adjust=True,com=2).mean()
        stock_data['KDJ_D'] = pd.Series.ewm(stock_data['KDJ_K'],ignore_na=False,min_periods=0,adjust=True,com=2).mean()
        stock_data['KDJ_J'] = 3 * stock_data['KDJ_K'] - 2 * stock_data['KDJ_D']
        # 计算KDJ指标金叉、死叉情况
        ###通常就敏感性而言，J值最强，K值次之，D值最慢，而就安全性而言，J值最差，K值次之，D值最稳
        ##金叉用1表示，死叉用0表示
        buyi=stock_data[(stock_data['KDJ_K'] > stock_data['KDJ_D'])&(stock_data['KDJ_K'].shift(-1) < stock_data['KDJ_D'].shift(-1))].index
        stock_data.loc[buyi,'Sign'] = 0
        selli=stock_data[(stock_data['KDJ_K'] < stock_data['KDJ_D'])&(stock_data['KDJ_K'].shift(-1) > stock_data['KDJ_D'].shift(-1))].index
        stock_data.loc[selli,'Sign'] = 1
        stock_data['Sign'].fillna(method='ffill', inplace=True)
        ##测试反向操作的效果，即买进信号则卖出，卖出信号则买进。
        stock_data['position']=stock_data['Sign'].shift(1)
        #stock_data['position'].fillna(method='ffill', inplace=True)
        #当仓位为1时，已当天的开盘价买入股票，当仓位为0时，以收盘价卖出该股份。计算从数据期内的收益
        stock_data['Cash_index'] = ((stock_data['p_change']/100  -fee) * \
                                    stock_data['position']+1).cumprod()
        #initial_idx = stock_data.iloc[0]['close'] / (1 + (stock_data.iloc[0]['p_change']/100))
        initial_idx = 1
        stock_data['Cash_index'] *= initial_idx

        stock_data=stock_data.set_index('date')
        _position_code(stock_data,code,W=Wr)
        """
        if (stock_data.iloc[-1]['position']==1)&(stock_data.iloc[-2]['position']==1):
            print ('持有这只股票Holding code')
        elif (stock_data.iloc[-1]['position']==1)&(stock_data.iloc[-2]['position']==0):
            print ('开始买进这只股票Buy code')
        elif (stock_data.iloc[-1]['position']==0)&(stock_data.iloc[-2]['position']==1):
            print ('开始卖出这只股票Sell code')
        else:
            print ('保持空仓Keeping Short Position code')   
        """
        if path != '':
            stock_data.to_csv(path)
        stock_data['vov']=pd.Series.rolling(stock_data['p_change'],window=window,center=False).std()
        if plot:
            stock_data[[label,'p_change','vov','Cash_index']].plot(subplots=True,figsize=(9,5),grid=True)
            plt.grid(True)
            plt.show()            
        return
    
def Tutlev1_df(df=None,label='Close',N1=20,N2=10,fee=0.0005,path='',plot=True):
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
        df=df.sort_index(ascending=True)
        df=df.drop_duplicates()
        df=df.reset_index()
        df=df.rename(columns=lambda x: str(x).lower())
        label=label.lower()
        index_data=df
        if 'p_change' not in df.columns:
            index_data['p_change']=(index_data[label]/index_data[label].shift(1)-1)*100
        # 保留这几个需要的字段：'date', 'high', 'low', 'close', 'change'
        index_data = index_data[['date','open', 'high', 'low', label, 'p_change']]
    
        index_data.loc[:,'High_Close_Price_N1_Day'] =  pd.Series.rolling(index_data['high'],window=N1,center=False).max()
        index_data['High_Close_Price_N1_Day'].fillna(value=index_data['high'].expanding(min_periods=1).max())
        index_data.loc[:,'Low_Close_Price_N2_Day'] =  pd.Series.rolling(index_data['low'],window=N2,center=False).min()
        index_data['Low_Close_Price_N2_Day'].fillna(value=index_data['low'].expanding(min_periods=1).min())
        #index_data['Low_Close_Price_N2_Day']=index_data['Low_Close_Price_N2_Day'].shift()
        # 当当天的【close】> 昨天的【最近N1个交易日的最高点】时，将【收盘发出的信号】设定为1
        buy_index = index_data[index_data['close'] > index_data['High_Close_Price_N1_Day'].shift(1)].index
        index_data.loc[buy_index, 'Sign'] = 1
        # 当当天的【close】< 昨天的【最近N2个交易日的最低点】时，将【收盘发出的信号】设定为0
        sell_index = index_data[index_data['close'] < index_data['Low_Close_Price_N2_Day'].shift(1)].index
        index_data.loc[sell_index, 'Sign'] = 0
        # 计算每天的仓位，当天持有上证指数时，仓位为1，当天不持有上证指数时，仓
        # 位为0
        index_data['Sign'].fillna(method='ffill', inplace=True)
        index_data['position'] = index_data['Sign'].shift(1)
        #index_data['position'].fillna(method='ffill', inplace=True)
        #当仓位为1时，已当天的开盘价买入股票，当仓位为0时，以收盘价卖出该股份。计算从数据期内的收益
        index_data['Cash_index'] = ((index_data['p_change']/100-fee) * index_data['position'] + 1.0).cumprod()
        #initial_idx = index_data.iloc[0]['close'] / (1 + (index_data.iloc[0]['p_change']/100))
        initial_idx = 1
        index_data['Cash_index'] *= initial_idx
        _position(index_data)

        #print ('The turtle methon Signal:')
        if path != '':
            index_data.to_csv(path)
        # ==========计算每年指数的收益以及海龟交易法则的收益
        index_data['p_change_turtle'] = (index_data['p_change']) * index_data['position']
        index_data=index_data.reset_index(drop=True)
        index_data=index_data.set_index('date')
        if plot:
            index_data[[label,'p_change','Cash_index']].plot(subplots=True,figsize=(9,5),grid=True)
            plt.grid(True)
            plt.show()    
    return

def Tutlev2_code(code=None,label='Close',N1=20,N2=10,fee=0.0005,path='',plot=True,Wr=False):
    """
    code:为输入的股票代码，大陆的为6个数字代码，香港的为4个数字代码。
         like：string 600036,0005
    df:为输入的DataFrame数据
    label：为所采用的列，open,high,close,low 或是Adj Close
    N1,N2：为计算平均数的周期
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
    
    if isinstance(df,pd.DataFrame):
        df=df.sort_index(ascending=True)
        df=df.drop_duplicates()
        df=df.reset_index()
        df=df.rename(columns=lambda x: str(x).lower())
        label=label.lower()
        index_data=df
        if 'p_change' not in df.columns:
            index_data['p_change']=(index_data[label]/index_data[label].shift(1)-1)*100
        # 保留这几个需要的字段：'date', 'high', 'low', 'close', 'change'
        index_data = index_data[['date','open', 'high', 'low', label, 'p_change']]
    
        index_data.loc[:,'High_Close_Price_N1_Day'] =  pd.Series.rolling(index_data['high'],window=N1,center=False).max()
        index_data['High_Close_Price_N1_Day'].fillna(value=index_data['high'].expanding(min_periods=1).max())
        index_data.loc[:,'Low_Close_Price_N2_Day'] =  pd.Series.rolling(index_data['low'],window=N2,center=False).min()
        index_data['Low_Close_Price_N2_Day'].fillna(value=index_data['low'].expanding(min_periods=1).min())
        #index_data['Low_Close_Price_N2_Day']=index_data['Low_Close_Price_N2_Day'].shift()
        # 当当天的【close】> 昨天的【最近N1个交易日的最高点】时，将【收盘发出的信号】设定为1
        buy_index = index_data[index_data['close'] > index_data['High_Close_Price_N1_Day'].shift(1)].index
        index_data.loc[buy_index, 'Sign'] = 1
        # 当当天的【close】< 昨天的【最近N2个交易日的最低点】时，将【收盘发出的信号】设定为0
        sell_index = index_data[index_data['close'] < index_data['Low_Close_Price_N2_Day'].shift(1)].index
        index_data.loc[sell_index, 'Sign'] = 0
        # 计算每天的仓位，当天持有上证指数时，仓位为1，当天不持有上证指数时，仓位为0
        index_data['Sign'].fillna(method='ffill', inplace=True)
        index_data['position'] = index_data['Sign'].shift(1)
        #index_data['position'].fillna(method='ffill', inplace=True)
        #当仓位为1时，已当天的开盘价买入股票，当仓位为0时，以收盘价卖出该股份。计算从数据期内的收益
        index_data['Cash_index'] = ((index_data['p_change']/100-fee) * index_data['position'] + 1.0).cumprod()
        #initial_idx = index_data.iloc[0]['close'] / (1 + (index_data.iloc[0]['p_change']/100))
        initial_idx = 1
        index_data['Cash_index'] *= initial_idx
        _position_code(index_data,code)

        #print ('The turtle methon Signal:')
        if path != '':
            index_data.to_csv(path)
        # ==========计算每年指数的收益以及海龟交易法则的收益
        index_data['p_change_turtle'] = (index_data['p_change']) * index_data['position']
        index_data=index_data.reset_index(drop=True)
        index_data=index_data.set_index('date')
        if plot:
            index_data[[label,'p_change','Cash_index']].plot(subplots=True,figsize=(9,5),grid=True)
            plt.grid(True)
            plt.show()    
    return

def MACDv1_df(df,label='Close',fee=0.0005,ld=26,sd=12, md=9,path='',plot=True):
    """
    df:为输入的DataFrame数据
    label：为所采用的列，open,high,close,low 或是Adj Close, Close
    ld,sd,md：为计算平均数的周期,以及dea 的计算周期
    fee:为交易的费率
    path:生成文件保存的地址及文件名，默认是不保存文件
    """    
    df=df.drop_duplicates()
    df.index=pd.to_datetime(df.index)
    try:
        df=df.drop('date',axis=1)
    except:
        pass
    df=df.reset_index()
    df=df.rename(columns=lambda x: str(x).lower())
    label=label.lower()
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

    buyi1=df[(df['DIF']>df['DEA'])&(df['DIF'].shift(-1)<df['DEA'].shift(-1))].index
    df.loc[buyi1,'Sign'] = 0
    seli1=df[(df['DIF']<df['DEA'])&(df['DIF'].shift(-1)>df['DEA'].shift(-1))].index
    df.loc[seli1,'Sign']=1

    
    df['Sign'].fillna(method='ffill',inplace=True)
   
    df.loc[:,'position']=df['Sign'].shift(1)
    df.loc[:,'Cash_index']=(1+(df['p_change']-fee)*df['position']).cumprod()
    df.loc[:,'vov']=pd.Series.rolling(df['p_change'],window=9).std()
    df=df.set_index('date')
    
    _position(df)

    if plot:
        fig=plt.figure(figsize=(9,6))
        fig.subplots_adjust(hspace=0.15, wspace=0.05,\
                            left=0.06,right=0.99,\
                            top=0.97,bottom=0.09)        
        ax1=fig.add_subplot(411)
        df[label].plot()
        plt.grid(True)

        ax2=fig.add_subplot(412)
        df[['p_change','vov']].plot(ax=ax2)
        plt.grid(True)
        ax4=fig.add_subplot(414)
        df['BAR'].plot(kind='bar',ax=ax4)
        ax5=ax4.twinx()
        df[['DIF','DEA']].plot(kind='line',ax=ax5)
        plt.grid(True)
        ax3=fig.add_subplot(413)
        df['Cash_index'].plot(ax=ax3)
        plt.grid(True)
        monthsLoc = mpl.dates.MonthLocator()
        weeksLoc = mpl.dates.WeekdayLocator()
        ax4.xaxis.set_major_locator(monthsLoc)
        ax4.xaxis.set_minor_locator(weeksLoc)
        monthsFmt = mpl.dates.DateFormatter('%b')
        ax4.xaxis.set_major_formatter(monthsFmt)
        plt.show()
    if path !='':
        df.to_csv(path)
    return df

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
    #df.index=pd.to_datetime(df.index)
    df=df.reset_index()
    df=df.rename(columns=lambda x: str(x).lower())
    label=label.lower()
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
        
        monthsLoc = mpl.dates.MonthLocator()
        weeksLoc = mpl.dates.WeekdayLocator()
        ax4.xaxis.set_major_locator(monthsLoc)
        ax4.xaxis.set_minor_locator(weeksLoc)
        monthsFmt = mpl.dates.DateFormatter('%b')
        ax4.xaxis.set_major_formatter(monthsFmt)
        plt.show()
    if path !='':
        df.to_csv(path)
    return 

def ChaikinADv2_code(code="",label='Close',fee=0.0005, M=5, N=10, path='',plot=True,Wr=False):
    
    if code =="":
        sys.exit()
    elif isinstance(code,str):
        if len(code)==6:
            df=wt.get_k_data(code)
        elif len(code)==4:
            df=wq.quandlyd(code)
            df=df.iloc[-640:,]
        else:
            sys.exit()
            
        
    df=df.sort_index(ascending=True)
    #print(df)
    df=df.drop_duplicates()    
    df=df.reset_index()
    df=df.rename(columns=lambda x: str(x).lower())
    label=label.lower()
    if 'p_change' not in df.columns:
        df.loc[:,'p_change']=df[label]/df[label].shift(1)-1

    df.loc[:,'volume_log']=df['volume'].apply(np.log10)

    
    df.loc[:,'AD_m']=pd.Series.rolling((2*df[label]-df['high']-df['low'])/(df['high']-df['low'])*df['volume_log'],window=M).mean()
    df.loc[:,'AD_n']=pd.Series.rolling((2*df[label]-df['high']-df['low'])/(df['high']-df['low'])*df['volume_log'],window=N).mean()
    df.loc[:,'Chaikin']=df['AD_m']-df['AD_n']

    buyi=df[(df['Chaikin'] > df['Chaikin'].shift(1))|((df['Chaikin']>0) & (df['Chaikin'].shift(1)<0))].index
    #buyi=df[(df['Chaikin'] > df['Chaikin'].shift(1))].index
    df.loc[buyi,'Sign']=1
    selli=df[(df['Chaikin']<df['Chaikin'].shift(1))|((df['Chaikin']<0)&(df['Chaikin'].shift(1)>0))].index
    #selli=df[(df['Chaikin']<df['Chaikin'].shift(1))].index
    df.loc[selli,'Sign']=0
    df['Sign'].fillna(method='ffill',inplace=True)
    df.loc[:,'position']=df['Sign'].shift(1)
    df.loc[:,'Cash_index']=(1+(df['p_change']-fee)*df['position']).cumprod()

    _position_code(df,code,W=False)
    
    df=df.set_index('date')
    #print(df.tail())
    if plot:
        fig=plt.figure(figsize=(9,5))
        fig.subplots_adjust(hspace=0.15, wspace=0.05,\
                            left=0.06,right=0.99,\
                            top=0.97,bottom=0.09)        
        ax1=fig.add_subplot(211)
        df[['AD_m','AD_n']].plot(ax=ax1)
        plt.grid(True)
        ax2=fig.add_subplot(212)
        df['Cash_index'].plot(ax=ax2)
        plt.grid(True)
        plt.show()

    #print(df.tail())
    return

def ChaikinADv1_df(df="",label='Close',fee=0.0005, M=5, N=10, path='',plot=True,Wr=False):
    
    df=df.sort_index(ascending=True)
    #print(df)
    df=df.drop_duplicates()    
    df=df.reset_index()
    df=df.rename(columns=lambda x: str(x).lower())
    label=label.lower()
    if 'p_change' not in df.columns:
        df.loc[:,'p_change']=df[label]/df[label].shift(1)-1

    df.loc[:,'volume_log']=df['volume'].apply(np.log10)

    
    df.loc[:,'AD_m']=pd.Series.rolling((2*df[label]-df['high']-df['low'])/(df['high']-df['low'])*df['volume_log'],window=M).mean()
    df.loc[:,'AD_n']=pd.Series.rolling((2*df[label]-df['high']-df['low'])/(df['high']-df['low'])*df['volume_log'],window=N).mean()
    df.loc[:,'Chaikin']=df['AD_m']-df['AD_n']

    buyi=df[(df['Chaikin'] > df['Chaikin'].shift(1))|((df['Chaikin']>0) & (df['Chaikin'].shift(1)<0))].index
    #buyi=df[(df['Chaikin'] > df['Chaikin'].shift(1))].index
    df.loc[buyi,'Sign']=1
    selli=df[(df['Chaikin']<df['Chaikin'].shift(1))|((df['Chaikin']<0)&(df['Chaikin'].shift(1)>0))].index
    #selli=df[(df['Chaikin']<df['Chaikin'].shift(1))].index
    df.loc[selli,'Sign']=0
    df['Sign'].fillna(method='ffill',inplace=True)
    df.loc[:,'position']=df['Sign'].shift(1)
    df.loc[:,'Cash_index']=(1+(df['p_change']-fee)*df['position']).cumprod()

    _position(df)
    
    df=df.set_index('date')
    #print(df.tail())
    if plot:
        fig=plt.figure(figsize=(9,5))
        fig.subplots_adjust(hspace=0.15, wspace=0.05,\
                            left=0.06,right=0.99,\
                            top=0.97,bottom=0.09)        
        ax1=fig.add_subplot(211)
        df[['AD_m','AD_n']].plot(ax=ax1)
        plt.grid(True)
        ax2=fig.add_subplot(212)
        df['Cash_index'].plot(ax=ax2)
        plt.grid(True)
        plt.show()

    #print(df.tail())
    return df

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

    df.loc[:,'vov']=pd.Series.rolling(df['p_change'],window=shortd).std()

    _position(df)
    
    df=df.set_index('date')    

    if plot:
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
        df[['RSI_%s'%shortd,'RSI_%s'%longd]].plot(ax=ax2)
        plt.grid(True)
        labels = ax2.get_xticklabels()
        plt.setp(labels, rotation=45, fontsize=5)
        plt.legend()

        ax3=fig.add_subplot(413)
        df['vov'].plot(ax=ax3)
        plt.grid(True)
        labels = ax3.get_xticklabels()
        plt.setp(labels, rotation=45, fontsize=5)
        plt.legend()        

        ax4=fig.add_subplot(414)
        df['Cash_ind'].plot(ax=ax4)
        plt.grid(True)
        labels = ax4.get_xticklabels()
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
    #df=wq.quandlyd('300177')
    #df=wd.get_h_csv('300006')
    #dd=df.iloc[-200:,:]
    #EMWA_STD(dd,fee=0.00025,times=2)#,label='close',window=12,times=1.25,fee=0.0025)
    #KDJv2_code('300006')#,label='Adjusted Close',path='tem.csv')
    #df=wt.get_k_data('300019')
    df=MACDv2_code('600497')
    #rsi(df)
    #ChaikinADv1_df(df)
    #ChaikinADv2_code('300006')
    #RSI('300006')
    """
    import tushare as ts
    df=ts.get_gem_classified()
    for code in df.code[:100]:
        print(code)
        KDJv2_code(code,plot=False)"""
