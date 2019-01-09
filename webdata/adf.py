#!/usr/bin/env python3
# -*-coding:utf-8-*-

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARMA, ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.stats.diagnostic import acorr_ljungbox

def test_stochastic(ts):
    p_value = acorr_ljungbox(ts, lags=1)[1] #lags可自定义
    return p_value

def proper_model(data_ts, maxLag):
    init_bic = float("inf")
    init_p = 0
    init_q = 0
    init_properModel = None
    for p in np.arange(maxLag):
        for q in np.arange(maxLag):
            model = ARMA(data_ts, order=(p, q))
            try:
                results_ARMA = model.fit(disp=-1, method='css')
            except:
                continue
            bic = results_ARMA.bic
            if bic < init_bic:
                init_p = p
                init_q = q
                init_properModel = results_ARMA
                init_bic = bic
    return init_bic, init_p, init_q, init_properModel


def test_ts(ts, w, title='test_ts'):
    roll_mean = ts.rolling(window = w).mean()
    roll_std = ts.rolling(window = w).std()
    pd_ewma = pd.Series.ewm(ts, span=w).mean()

    plt.clf()
    plt.figure()
    plt.grid()
    plt.plot(ts, color='blue',label='Original')
    plt.plot(roll_mean, color='red', label='Rolling Mean')
    plt.plot(roll_std, color='black', label = 'Rolling Std')
    plt.plot(pd_ewma, color='yellow', label = 'EWMA')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    #plt.show()
    plt.savefig('PDF/'+title+'.pdf', format='pdf')

def draw_acf_pacf(ts, w):
    """
    ts:Array of time-series values
    w:int or array_like, optional
    """
    plt.clf()
    fig = plt.figure()
    ax1 = fig.add_subplot(211)
    plot_acf(ts, ax = ax1, lags=w)
    ax2 = fig.add_subplot(212)
    plot_pacf(ts, ax=ax2, lags=w)

    #plt.show()
    plt.savefig('PDF/test_acf_pacf.pdf', format='pdf')    

def adf_test(ts_diff):
    adftest=adfuller(ts_diff,autolag='AIC')
    adf_res = pd.Series(adftest[0:4], index=['Test Statistic','p-value','Lags Used','Number of Observations Used'])
    for key, value in adftest[4].items():
        adf_res['Critical Value (%s)' % key] = value
    return adf_res

def draw_ar(ts, w):
    arma = ARMA(ts, order=(w,0)).fit(disp=-1)
    ts_predict = arma.predict()

    plt.clf()
    plt.plot(ts_predict, label="PDT")
    plt.plot(ts, label = "ORG")
    plt.legend(loc="best")
    plt.title("AR Test %s" % w)
    plt.savefig("test_ar_"+ str(w) +".pdf", format='pdf')

def draw_ma(ts, w):
    ma = ARMA(ts, order=(0, w)).fit(disp = -1)
    ts_predict_ma = ma.predict()

    ar = ARMA(ts, order=(w,0)).fit(disp=-1)
    ts_predict_ar = ar.predict()

    plt.clf()
    plt.plot(ts_predict_ar, label="AR")
    plt.plot(ts_predict_ma, label="MA")
    #plt.plot(ts, label = "ORG")
    plt.legend(loc="best")
    plt.title("MA Test %s" % w)
    plt.savefig("test_ma_"+ str(w) +".pdf", format='pdf')

    return ts_predict_ma

def test_stationarity(timeseries):
    
    #Determing rolling statistics
    rolmean = pd.rolling_mean(timeseries, window=12)
    rolstd = pd.rolling_std(timeseries, window=12)

    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)
    
    #Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)

def test_stationarityv(timeseries):
    dftest = adfuller(timeseries, autolag='AIC')
    return dftest[1]
                  
def best_diff(df, maxdiff = 8):
    p_set = {}
    for i in range(0, maxdiff):
        temp = df.copy() #每次循环前，重置
        if i == 0:
            temp['diff'] = temp[temp.columns[1]]
        else:
            temp['diff'] = temp[temp.columns[1]].diff(i)
            temp = temp.drop(temp.iloc[:i].index) #差分后，前几行的数据会变成nan，所以删掉
        pvalue = test_stationarityv(temp['diff'])
        p_set[i] = pvalue
        p_df = pd.DataFrame.from_dict(p_set, orient="index")
        print(p_df)
        p_df.columns = ['p_value']
    i = 0
    while i < len(p_df):
        if p_df['p_value'][i]<0.01:
            bestdiff = i
            print(bestdiff)
            break
        i += 1
    return bestdiff

if __name__=="__main__":
    df=pd.read_csv('/home/chen/AirPasseger.csv')
    dates=pd.date_range('1949-01-01','1961-01-01',freq='M')
    df=df.drop('Unnamed: 0',axis=1)
    df.index=dates
    ss=best_diff(df)
    

