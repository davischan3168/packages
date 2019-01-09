#!/usr/bin/env python3
# -*-coding:utf-8-*-

import pandas as pd
#pd.set_option("mode.use_inf_as_null",True)
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import webdata.stock.trading as wt
import webdata.stock.fundamental as wf
import statsmodels.api as sm
import webdata.puse.jqka as ths
from statsmodels.sandbox.regression.predstd import wls_prediction_std
#import tushare as ts
import os,sys
try:
    import Quandl
except:
    import quandl as Quandl
import datetime,time
try:
    from io import StringIO
except:
    from pandas.compat import StringIO
import matplotlib.pyplot as plt

def OLSV2A(code):
    df=wt.get_h_data(code,start='2001-01-01')
    #df=get_hist_csv(code)
    df=df.sort_index()
    df.index=pd.to_datetime(df.index)
    df=df.drop_duplicates(keep=False)
    print ('\n,Caculating the analysing 1/4 statistics:\n')
    print (df.describe(),'\n')
    
    if code[0] in ['6','9']:
        ticker='000001'
    elif code[0] in ['0','2','3']:
        ticker='399001'
    dfi=wt.get_h_data(ticker,index=True,start='2001-01-01')
    dfi=dfi.sort_index()
    dfi.index=pd.to_datetime(dfi.index)

    df['cpct']=df['close'].pct_change()*100
    df['lpct']=df['cpct'].shift(1)
    df['llpct']=df['lpct']**2
    df['sina']=np.sin(df['lpct'])
    df['vpct']=df['volume'].pct_change()*100
    dfi['indpct']=dfi['close'].pct_change()*100

    try:
        rets=pd.concat([df['cpct'],df['lpct'],df['llpct'],df['sina'],dfi['indpct'],df['vpct'],df['turnover']],axis=1)
        rets=rets.dropna(how='any')
        X=np.array(rets.iloc[:,1:])
        X=sm.add_constant(X)
    except:
        rets=pd.concat([df['cpct'],df['lpct'],df['llpct'],df['sina'],dfi['indpct'],df['vpct']],axis=1)
        rets=rets.dropna(how='any')
        X=np.array(rets.iloc[:,1:])
        X=sm.add_constant(X)        
    

    Y=np.array(rets.iloc[:,0])
    model=sm.OLS(Y,X)
    results=model.fit()
    print (results.summary())
    
    print ("The params for the model:",results.params)
    print ("The std for the model:",results.bse)

    #df['predict']=''
    #df.iloc[1:,df.columns.get_loc('predict')]=results.predict()
    #dd=df[['close','cpct','predict']]
    
    return results

def OLSV2_HA(code):
    """
    code is 6 strings or 4 strings
    conclude the share listed in mainland and hongkong exchange
    """
    if len(code)==6:
        if (code[0]=='6')|(code[0]=='9'):
            code='SS_'+code
            _get_index_data('000001')
            index1='SS_000001'
        else:
            code='SZ_'+code
            _get_index_data('399001')
            index1='SZ_399001'
    elif len(code)==4:
        code='HK_'+code
        index1='HK_HSI'
    else:
        print('Input Wrong code.')

    pre_code='YAHOO/'
    ticker=pre_code+code
    index1=pre_code+index1

    fn='./Quandl/'+ticker+'.csv'
    ind='./Quandl/'+index1+'.csv'

    df=pd.read_csv(fn,parse_dates=True,index_col=0)
    dff1=df[['Open','High','Low','Close','Volume','Adjusted Close']].copy()
    print ('Caculating the analysing 1/4 statistics:')
    print (dff1.describe(),'\n')
    dfi=pd.read_csv(ind,parse_dates=True,index_col=0)
    df['cpct']=df['Close'].pct_change()
    df['vpct']=df['Volume'].pct_change()
    dfi['indpct']=dfi['Close'].pct_change()

    rets=pd.concat([df['cpct'],dfi['indpct'],df['vpct']],axis=1)
    rets=rets.dropna(how='any')
    #print (rets)

    X=np.array(rets.iloc[:,1:3])
    X=sm.add_constant(X)
    #print(X)

    Y=np.array(rets.iloc[:,0])


    #y=np.dot(X,beta)+e
    model=sm.OLS(Y,X)
    results=model.fit()
    print (results.summary())
    
    print ("The params for the model:",results.params)
    print ("The std for the model:",results.bse)
    return results
