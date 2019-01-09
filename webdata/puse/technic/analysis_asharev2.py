#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
#QQ: 2089973054
"""
#本程序其实是挑出了所有KDJ金叉的股票，并不是低位KDJ金叉。有人认为低位KDJ金叉效果更好，例如D值小于20时的金叉。在现有程序
#上进行小小的改动就可以挑选出低位KDJ金叉的股票，大家感兴趣可以看看选股效果怎么样，说实话具体怎么样我也没有试过。
from __future__ import division
import os,sys
import pandas as pd
import tushare as ts
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import datetime
today1=time.strftime('%Y-%m-%d')
#stock_code_list = []
#all_stock = pd.DataFrame()
#code = raw_input('Enter share code like xxxxxx-->')

def print_return_next_n_day(dd):
    print
    print '历史上这只股票%s出现买入信号的次数为%d，这股票在：'%(code,dd.shape[0])
    print
    for n in [1, 2, 3, 5, 10, 20]:
        print "金叉之后的%d个交易日内，" % n,
        print "平均涨幅为%.2f%%，" % (dd['CP_next_'+str(n)+'_days'].mean()*100),
        print "最高涨幅为%.2f%%，" % (dd['CP_next_'+str(n)+'_days'].max()*100),
        print "最大跌涨幅为%.2f%%，" % (dd['CP_next_'+str(n)+'_days'].min()*100),
        print "其中上涨的概率是%.2f%%。" % \
            (dd[dd['CP_next_'+str(n)+'_days'] > 0].shape[0]/float(dd.shape[0]) * 100)
        #    print all_stock[all_stock['接下来'+str(n)+'个交易日涨跌幅'] > 0].shape[0],all_stock.shape[0]
        print
    return

def return_for_period(stock_data):
    # ==========计算每年指数的收益以及海龟交易法则的收益
    stock_data['p_change_period'] = (stock_data['p_change']) * stock_data['position']
    year_rtn = stock_data.set_index('date')[['p_change', 'p_change_period']].\
               resample('A', how=lambda x: (x/100+1.0).prod() - 1.0) * 100
    return stock_data

def Make_decision(stock_data):
    if (stock_data.iloc[-1]['position']==1)&(stock_data.iloc[-2]['position']==1):
        print u'持有这只股票Holding %s.'%code
    elif (stock_data.iloc[-1]['position']==1)&(stock_data.iloc[-2]['position']==0):
        print u'开始买进这只股票Buy %s.'%code
    elif (stock_data.iloc[-1]['position']==0)&(stock_data.iloc[-2]['position']==1):
        print u'开始卖出这只股票Sell %s.'%code
    else:
        print u'保持空仓Keeping Short Position %s.'%code
    print '================================================================='
    return


def analysis_kdjv1(code):
    filename='./stockdata/data/last3year/'+code+'.csv'
    stock_dataT = pd.read_csv(filename, parse_dates=['date'],encoding='gbk')
    stock_data=stock_dataT.loc[:,('date', 'high', 'low', 'close', 'p_change')].copy()
    # 计算KDJ指标
    #stock_data['low_list'] = pd.rolling_min(stock_data['low'], 9)
    stock_data['low_list'] = pd.Series.rolling(stock_data['low'],window=9,center=False).min()
    #stock_data['low_list'].fillna(value=pd.expanding_min(stock_data['low']), inplace=True)
    stock_data['low_list'].fillna(value=pd.Series.expanding(stock_data['low'],min_periods=1)).min()
    #stock_data['high_list'] = pd.rolling_max(stock_data['high'], 9)
    stock_data['high_list']=pd.Series.rolling(stock_data['high'],window=9,center=False).max()
    #stock_data['high_list'] = pd.Series.rolling(stock_data['high'],window=9,center=False).max()
    #stock_data['high_list'].fillna(value=pd.expanding_max(stock_data['high']), inplace=True)
    stock_data['high_list'].fillna(value=pd.Series.expanding(stock_data['high'],min_periods=1)).max()
    stock_data['rsv'] = (stock_data['close'] - stock_data['low_list']) / (stock_data['high_list'] - stock_data['low_list']) * 100
    #stock_data['rsv']=(stock_data['close'] - low_list) / (high_list - low_list) * 100
    stock_data['KDJ_K'] = pd.Series.ewm(stock_data['rsv'],ignore_na=False,min_periods=0,adjust=True,com=2).mean()
    stock_data['KDJ_D'] = pd.Series.ewm(stock_data['KDJ_K'],ignore_na=False,min_periods=0,adjust=True,com=2).mean()
    stock_data['KDJ_J'] = 3 * stock_data['KDJ_K'] - 2 * stock_data['KDJ_D']
    # 计算KDJ指标金叉、死叉情况
    ###通常就敏感性而言，J值最强，K值次之，D值最慢，而就安全性而言，J值最差，K值次之，D值最稳
    ##金叉用1表示，死叉用0表示
    buyi=stock_data[(stock_data['KDJ_K'] > stock_data['KDJ_D'])&(stock_data['KDJ_K'].shift(-1) < stock_data['KDJ_D'].shift(-1))].index
    stock_data.loc[buyi,'Signal'] = 0
    selli=stock_data[(stock_data['KDJ_K'] < stock_data['KDJ_D'])&(stock_data['KDJ_K'].shift(-1) > stock_data['KDJ_D'].shift(-1))].index
    stock_data.loc[selli,'Signal'] = 1
    ##测试反向操作的效果，即买进信号则卖出，卖出信号则买进。
    #kdj_position = stock_data['KDJ_K'] > stock_data['KDJ_D']
    #stock_data.loc[kdj_position[(kdj_position == True) & (kdj_position.shift() == False)].index, 'KDJ_BS'] = 1
    #stock_data.loc[kdj_position[(kdj_position == False) & (kdj_position.shift() == True)].index, 'KDJ_BS'] = 0
    stock_data['position']=stock_data['Signal'].shift(1)
    stock_data['position'].fillna(method='ffill', inplace=True)
    #当仓位为1时，已当天的开盘价买入股票，当仓位为0时，以收盘价卖出该股份。计算从数据期内的收益
    stock_data['Cash_index'] = ((stock_data['p_change']/100) * stock_data['position'] + 1.0).cumprod()
    #initial_idx = stock_data.iloc[0]['close'] / (1 + (stock_data.iloc[0]['p_change']/100))
    initial_idx = 1
    stock_data['Cash_index'] *= initial_idx
    print 'The KDJ Forwards methon Signal:'
    Make_decision(stock_data)
    # 通过复权价格计算接下来几个交易日的收益率
    for n in [1, 2, 3, 5, 10, 20]:
        stock_data['CP_next_'+str(n)+'_days'] =(stock_data['close'].shift(-1*n) / stock_data['close'] - 1.0)
        #stock_data.dropna(how='any', inplace=True)# 删除所有有空值的数据行
    dd=stock_data[stock_data['Signal']==1]
    #print_return_next_n_day(dd)
    codedir='./output/A/'+code+os.sep
    if not os.path.exists(codedir):
        os.mkdir(codedir)
    # ===计算每年指数的收益
    stock_data['p_change_period'] = (stock_data['p_change']) * stock_data['position']
    #year_rtn = stock_data.set_index('date')[['p_change', 'p_change_period']].resample('A', how=lambda x: (x/100+1.0).prod() - 1.0) * 100
    year_rtn = stock_data.set_index('date')[['p_change', 'p_change_period']].resample('A').apply(lambda x: ((x/100+1.0).prod() - 1.0) * 100)
    year_rtn.to_csv(codedir+'kdjv1_year.csv', encoding='gbk')
    #按月计算收益
    stock_data['p_change_period_for_Month'] = (stock_data['p_change']) * stock_data['position']
    #year_rtn = stock_data.set_index('date')[['p_change', 'p_change_period_for_Month']].resample('M', how=lambda x: (x/100+1.0).prod() - 1.0) * 100
    year_rtn = stock_data.set_index('date')[['p_change', 'p_change_period_for_Month']].resample('M').apply(lambda x: ((x/100+1.0).prod() - 1.0) * 100)
    year_rtn.to_csv(codedir+'kdjv1_month.csv', encoding='gbk')
    stock_data.to_csv(codedir+'kdjv1.csv',encoding='gbk',index=False)
    stock_data.tail(20).to_csv(codedir+'kdjv1_Signal.csv',encoding='gbk',index=False)
    #print 'the share %s trading sign for KDJV1:'%code
    #print stock_data.tail(2)
    return

def analysis_kdjv2(code):
    filename='./stockdata/data/last3year/'+code+'.csv'
    stock_dataT = pd.read_csv(filename, parse_dates=['date'])
    #stock_dataT.sort('date', inplace=True)
    stock_data=stock_dataT.loc[:,('date', 'high', 'low', 'close', 'p_change')]
    # 计算KDJ指标
    stock_data['low_list'] = pd.rolling_min(stock_data['low'], 9)
    stock_data['low_list'].fillna(value=pd.expanding_min(stock_data['low']), inplace=True)
    stock_data['high_list'] = pd.rolling_max(stock_data['high'], 9)
    stock_data['high_list'].fillna(value=pd.expanding_max(stock_data['high']), inplace=True)
    stock_data['rsv'] = (stock_data['close'] - stock_data['low_list']) / (stock_data['high_list'] - stock_data['low_list']) * 100
    #stock_data['rsv']=(stock_data['close'] - low_list) / (high_list - low_list) * 100
    stock_data['KDJ_K'] = pd.ewma(stock_data['rsv'], com=3)
    stock_data['KDJ_D'] = pd.ewma(stock_data['KDJ_K'], com=3)
    stock_data['KDJ_J'] = 3 * stock_data['KDJ_K'] - 2 * stock_data['KDJ_D']
    # 计算KDJ指标金叉、死叉情况
    ###通常就敏感性而言，J值最强，K值次之，D值最慢，而就安全性而言，J值最差，K值次之，D值最稳
    ##金叉用1表示，死叉用0表示
    buyi=stock_data[(stock_data['KDJ_K'] > stock_data['KDJ_D'])&(stock_data['KDJ_K'].shift(1) < stock_data['KDJ_D'].shift(1))].index
    stock_data.loc[buyi,'Signal'] = 1
    selli=stock_data[(stock_data['KDJ_K'] < stock_data['KDJ_D'])&(stock_data['KDJ_K'].shift(1) > stock_data['KDJ_D'].shift(1))].index
    stock_data.loc[selli,'Signal'] = 0
    #kdj_position = stock_data['KDJ_K'] > stock_data['KDJ_D']
    #stock_data.loc[kdj_position[(kdj_position == True) & (kdj_position.shift() == False)].index, 'KDJ_BS'] = 1
    #stock_data.loc[kdj_position[(kdj_position == False) & (kdj_position.shift() == True)].index, 'KDJ_BS'] = 0
    stock_data['position']=stock_data['Signal'].shift(1)
    stock_data['position'].fillna(method='ffill', inplace=True)
    #当仓位为1时，已当天的开盘价买入股票，当仓位为0时，以收盘价卖出该股份。计算从数据期内的收益
    stock_data['Cash_index'] = ((stock_data['p_change']/100) * stock_data['position'] + 1.0).cumprod()
    initial_idx = 1
    #initial_idx = stock_data.iloc[0]['close'] / (1 + (stock_data.iloc[0]['p_change']/100))
    stock_data['Cash_index'] *= initial_idx
    print 'The KDJ Backwards methon Signal:'
    Make_decision(stock_data)
    # 通过复权价格计算接下来几个交易日的收益率
    for n in [1, 2, 3, 5, 10, 20]:
        stock_data['CP_next_'+str(n)+'_days'] =(stock_data['close'].shift(-1*n) / stock_data['close'] - 1.0)*100
        #stock_data.dropna(how='any', inplace=True)# 删除所有有空值的数据行
        # ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
        ##统计出现买点时点的数据
        dd=stock_data[stock_data['Signal']==1]
    print_return_next_n_day(dd)
    codedir='./output/A/'+code+os.sep
    if not os.path.exists(codedir):
        os.mkdir(codedir)
    # ==========计算每年指数的收益以及海龟交易法则的收益
    stock_data['p_change_KDJV2'] = (stock_data['p_change']) * stock_data['position']
    year_rtn = stock_data.set_index('date')[['p_change', 'p_change_KDJV2']].\
               resample('A', how=lambda x: (x/100+1.0).prod() - 1.0) * 100
    year_rtn.to_csv(codedir+'kdjv2_year.csv', encoding='gbk')
    stock_data.to_csv(codedir+'kdjv2.csv',encoding='gbk',index=False)
    stock_data.tail(20).to_csv(codedir+'kdjv2_Signal.csv',encoding='gbk',index=False)
    print 'the share %s trading sign for KDJV2:'%code
    print stock_data.tail(5)
    return

def analysis_macdv2(code):
    filename='./stockdata/data/last3year/'+code+'.csv'
    stock_data = pd.read_csv(filename, parse_dates=['date'])
    stock_data=stock_data[['date', 'high', 'low', 'close', 'p_change']]
    # 将数据按照交易日期从远到近排序
    #stock_data.sort('date', inplace=True)
    #print 's以2天为间隔，测试范围从2～20天，L以5天为间隔，测试范围从20～120，M以5天为间隔，测试范围5～60'
    #ldema=input('Enter long date for EMA X -->')
    #sdema=input('Enter short date for EMA X-->')
    #md=input('Enter short date for DEA-->')
    ldema=60
    sdema=12
    md=10
    ema_list=[sdema,ldema]
    ##########################################################################
    ####计算指数平滑移动平均线EMA####################
    for ema in ema_list:
        stock_data['EMA_' + str(ema)] = pd.Series.ewm(stock_data['close'],ignore_na=False,span=ema,min_periods=0,adjust=True).mean()
        #stock_data['EMA_' + str(ema)] = pd.ewma(stock_data['close'], span=ema)
    stock_data['DIF']=stock_data['EMA_'+str(sdema)]-stock_data['EMA_'+str(ldema)]
    stock_data['DEA']= pd.Series.ewm(stock_data['DIF'],ignore_na=False, span=md,min_periods=0,adjust=True).mean()
    #stock_data['MACD']=(stock_data['DIF']-stock_data['DEA'])*3
    ##买入信号，用1代表
    #buy_index=stock_data[(stock_data['DIF']>stock_data['DIF'].shift(1))&\
        #                     (stock_data['DIF']>stock_data['DEA'])&\
        #                     (stock_data['DIF'].shift(1)<stock_data['DEA'].shift(1))&\
        #                     (stock_data['DIF']>0)].index
    buy_index=stock_data[(stock_data['DIF']>stock_data['DEA'])&\
                         (stock_data['DIF'].shift(1)<stock_data['DEA'].shift(1))].index
    stock_data.loc[buy_index,'Signal']=1
    #卖出信号，用0代表
    #sell_index=stock_data[(stock_data['DIF']<stock_data['DIF'].shift(1))&\
        #                      (stock_data['DIF']<stock_data['DEA'])&\
        #                      (stock_data['DIF'].shift(1)<stock_data['DEA'].shift(1))&\
        #                      (stock_data['DIF']<0)].index
    sell_index=stock_data[(stock_data['DIF']<stock_data['DEA'])&\
                          (stock_data['DIF'].shift(1)>stock_data['DEA'].shift(1))].index
    stock_data.loc[sell_index,'Signal']=0
    #测试反向操作的效果，即买进信号则卖出，卖出信号则买进。
    # 将数据按照交易日期从近到远排序
    #stock_data.sort('date', ascending=False, inplace=True)
    stock_data['position'] = stock_data['Signal'].shift(1)
    stock_data['position'].fillna(method='ffill', inplace=True)
    #当仓位为1时，已当天的开盘价买入股票，当仓位为0时，以收盘价卖出该股份。计算从数据期内的收益
    stock_data['Cash_index'] = ((stock_data['p_change']/100) * stock_data['position'] + 1.0).cumprod()
    #initial_idx = stock_data.iloc[0]['close'] / (1 + (stock_data.iloc[0]['p_change']/100))
    initial_idx = 1
    stock_data['Cash_index'] *= initial_idx
    print 'The MACD methon Signal:'
    Make_decision(stock_data)
    # 通过复权价格计算接下来几个交易日的收益率
    for n in [1, 2, 3, 5, 10, 20]:
        stock_data['CP_next_'+str(n)+'_days'] = stock_data['close'].shift(-1*n) / stock_data['close'] - 1.0
        #stock_data.dropna(how='any', inplace=True)# 删除所有有空值的数据行
    # ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
    ##统计出现买点时点的数据
    dd=stock_data[stock_data['Signal']==1]
    print_return_next_n_day(dd)
    codedir='./output/A/'+code+os.sep
    if not os.path.exists(codedir):
        os.mkdir(codedir)
    # ==========计算每年指数的收益以及海龟交易法则的收益
    stock_data['p_change_macdV2'] = (stock_data['p_change']) * stock_data['position']
    #year_rtn = stock_data.set_index('date')[['p_change', 'p_change_macdV2']].resample('A', how=lambda x: (x/100+1.0).prod() - 1.0) * 100
    year_rtn = stock_data.set_index('date')[['p_change','p_change_macdV2']].resample('A').apply(lambda x: ((x/100+1.0).prod() - 1.0) * 100)
    year_rtn.to_csv(codedir+'macdv2_year.csv', encoding='gbk')
    # ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
    stock_data.to_csv(codedir+'macdv2.csv', index=False)
    stock_data.tail(20).to_csv(codedir+'macdv2_Signal.csv', index=False)
    print 'the share %s trading sign for MACD:'%code
    print stock_data.tail(5)
    return

def analysis_mav2(code):
    # =从原始csv文件中导入股票数据，以浦发银行sh600000为例
    # 导入数据 - 注意：这里请填写数据文件在您电脑中的路径
    #code = raw_input('Enter share code like xxxxxx-->')
    filename='./stockdata/data/last3year/'+code+'.csv'
    stock_data = pd.read_csv(filename, parse_dates=['date'])
    stock_data=stock_data[['date', 'high', 'low', 'close', 'p_change']]
    # 将数据按照交易日期从远到近排序
    #stock_data.sort('date', inplace=True)
    #print 's以2天为间隔，测试范围从2～20天，L以5天为间隔，测试范围从20～120,量化投资——策略与技术一书中推荐s为4天，L为40天'
    
    #ldma=input('Enter long date for MA X -->')
    #sdma=input('Enter short date for MA X-->')
    ldma=21
    sdma=5
    #################################################################
    ####################计算移动平均线
    # 分别计算5日、20日、60日的移动平均线
    #ma_list = [5, 20, 60, sd, ld]
    ma_list = [sdma, ldma]
    # 计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
    for ma in ma_list:
        #stock_data['MA_' + str(ma)] = pd.rolling_mean(stock_data['close'], ma)
        stock_data['MA_' + str(ma)] = pd.Series.rolling(stock_data['close'],window=ma,center=False).mean()
    #买入信号:SMA(t)>SMA(t-1) and SMA(t)>LMA(t) and SMA(t-1)<LMA(t-1),则是买进信号,用1代表
    #buy_index=stock_data[(stock_data['MA_'+str(sdma)]>stock_data['MA_'+str(ldma)]) &
    #                     (stock_data['MA_'+str(sdma)]>stock_data['MA_'+str(sdma)].shift(1)) &
    #                     (stock_data['MA_'+str(ldma)].shift(1)>stock_data['MA_'+str(sdma)].shift(1))].index
    buy_index=stock_data[(stock_data['MA_'+str(sdma)]>stock_data['MA_'+str(ldma)]) &
                         (stock_data['MA_'+str(sdma)].shift(1)<stock_data['MA_'+str(ldma)].shift(1))].index
    stock_data.loc[buy_index,'Signal']=1
    #卖出信号:LMA(t)<LMA(t-1) and SMA(t)<LMA(t) and SMA(t-1)>LMA(t-1),则是卖出信号，用0代表
    #sell_index=stock_data[(stock_data['MA_'+str(ldma)]<stock_data['MA_'+str(ldma)].shift(1)) &
    #                     (stock_data['MA_'+str(sdma)]<stock_data['MA_'+str(ldma)]) &
    #                     (stock_data['MA_'+str(sdma)].shift(1)<stock_data['MA_'+str(sdma)].shift(1))].index
    sell_index=stock_data[(stock_data['MA_'+str(sdma)]<stock_data['MA_'+str(ldma)]) &
                          (stock_data['MA_'+str(sdma)].shift(1)>stock_data['MA_'+str(ldma)].shift(1))].index
    stock_data.loc[sell_index,'Signal']=0
    
    stock_data['position'] = stock_data['Signal'].shift(1)
    stock_data['position'].fillna(method='ffill', inplace=True)
    #当仓位为1时，已当天的开盘价买入股票，当仓位为0时，以收盘价卖出该股份。计算从数据期内的收益
    stock_data['Cash_index'] = ((stock_data['p_change']/100) * stock_data['position'] + 1.0).cumprod()
    #initial_idx = stock_data.iloc[0]['close'] / (1 + (stock_data.iloc[0]['p_change']/100))
    initial_idx = 1
    stock_data['Cash_index'] *= initial_idx
    print 'The MA methon Signal:'
    Make_decision(stock_data)
    # 通过复权价格计算接下来几个交易日的收益率
    for n in [1, 2, 3, 5, 10, 20]:
        stock_data['CP_next_'+str(n)+'_days'] = stock_data['close'].shift(-1*n) / stock_data['close'] - 1.0
        #stock_data.dropna(how='any', inplace=True)# 删除所有有空值的数据行
    # ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
    ##统计出现买点时点的数据
    dd=stock_data[stock_data['Signal']==1]
    #print_return_next_n_day(dd)
    codedir='./output/A/'+code+os.sep
    if not os.path.exists(codedir):
        os.mkdir(codedir)        
    # ==========计算每年指数的收益以及海龟交易法则的收益
    stock_data['p_change_mav2'] = (stock_data['p_change']) * stock_data['position']
    #year_rtn = stock_data.set_index('date')[['p_change', 'p_change_mav2']].resample('A', how=lambda x: (x/100+1.0).prod() - 1.0) * 100
    year_rtn = stock_data.set_index('date')[['p_change', 'p_change_mav2']].resample('A').apply(lambda x: ((x/100+1.0).prod() - 1.0) * 100)
    year_rtn.to_csv(codedir+'mav2_year.csv', encoding='gbk')
    stock_data.to_csv(codedir+'mav2.csv', index=False)
    stock_data.tail(20).to_csv(codedir+'mav2_Signal.csv', index=False)
    #print 'the share %s trading sign for MA:'%code
    #print stock_data.tail(5)
    return

def analysis_trixv2(code):
    filename='./stockdata/data/last3year/'+code+'.csv'
    stock_data = pd.read_csv(filename, parse_dates=['date'])
    # 将数据按照交易日期从远到近排序
    #stock_data.sort('date', inplace=True)
    stock_data=stock_data[['date', 'high', 'low', 'close', 'p_change']]
    ###############################################################
    #########计算trix指标###在波动行情中会失效
    #print 'N以2天为间隔，测试范围从2～20天，M以5天为间隔，测试范围从20～120'
    #print '量化投资——策略与技术一书中推荐s为4天，L为40天'
    #ntd=input('Enter Ntd for Trix index-->')#参数N设为12
    #mtd=input('Enter Mtd for Trix index-->')#参数M设为20
    ntd=24
    mtd=72
    #stock_data['TR']= pd.ewma(pd.ewma(pd.ewma(stock_data['close'],com=ntd),com=ntd),com=ntd)
    stock_data['TR']=pd.Series.ewm(pd.Series.ewm(pd.Series.ewm(stock_data['close'],ignore_na=False,min_periods=0,adjust=True,com=ntd).mean(),ignore_na=False,min_periods=0,adjust=True,com=ntd).mean(),ignore_na=False,min_periods=0,adjust=True,com=ntd).mean()
    stock_data['TRIX']=(stock_data['TR']-stock_data['TR'].shift(1))*100/stock_data['TR'].shift(1)
    stock_data['MATRIX']= pd.Series.rolling(stock_data['TRIX'],window=mtd,center=False).mean()
    #买入信号：TRIX(t)>TRIX(t-1) & TRIX(t)>MATRIX(t) & TRIX(t-1)<MATRIX(t-1)，用1代表
    #buy_index=stock_data[(stock_data['TRIX']>stock_data['TRIX'].shift(1))&\
        #                     (stock_data['TRIX']>stock_data['MATRIX'])&\
        #                     (stock_data['TRIX'].shift(1)<stock_data['MATRIX'].shift(1))].index
    buy_index=stock_data[(stock_data['TRIX']>stock_data['MATRIX'])&\
                         (stock_data['TRIX'].shift(1)<stock_data['MATRIX'].shift(1))].index
    stock_data.loc[buy_index,'Signal']=1
    stock_data.loc[buy_index,'Signal']=1
    #卖出信号：TRIX(t)<TRIX(t-1) & TRIX(t)<MATRIX(t) & TRIX(t-1)>MATRIX(t-1)，用0代表
    #sell_index=stock_data[(stock_data['TRIX']<stock_data['TRIX'].shift(1))&\
        #                      (stock_data['TRIX']<stock_data['MATRIX'])&\
        #                      (stock_data['TRIX'].shift(1)>stock_data['MATRIX'].shift(1))].index
    sell_index=stock_data[(stock_data['TRIX']<stock_data['MATRIX'])&\
                          (stock_data['TRIX'].shift(1)>stock_data['MATRIX'].shift(1))].index
    stock_data.loc[sell_index,'Signal']=0
    # 将数据按照交易日期从近到远排序
    #stock_data.sort('date', ascending=False, inplace=True)
    stock_data['position'] = stock_data['Signal'].shift(1)
    stock_data['position'].fillna(method='ffill', inplace=True)
    #当仓位为1时，已当天的开盘价买入股票，当仓位为0时，以收盘价卖出该股份。计算从数据期内的收益
    stock_data['Cash_index'] = ((stock_data['p_change']/100) * stock_data['position'] + 1.0).cumprod()
    #initial_idx = stock_data.iloc[0]['close'] / (1 + (stock_data.iloc[0]['p_change']/100))
    initial_idx = 1
    stock_data['Cash_index'] *= initial_idx
    print 'The TRix methon Signal:'
    Make_decision(stock_data)
    # 通过复权价格计算接下来几个交易日的收益率
    for n in [1, 2, 3, 5, 10, 20]:
        stock_data['CP_next_'+str(n)+'_days'] = stock_data['close'].shift(-1*n) / stock_data['close'] - 1.0
    #stock_data.dropna(how='any', inplace=True)# 删除所有有空值的数据行
    # ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
    ##统计出现买点时点的数据
    dd=stock_data[stock_data['Signal']==1]
    print_return_next_n_day(dd)
    codedir='./output/A/'+code+os.sep
    if not os.path.exists(codedir):
        os.mkdir(codedir)   
    stock_data['p_change_trix'] = (stock_data['p_change']) * stock_data['position']
    #year_rtn = stock_data.set_index('date')[['p_change', 'p_change_trix']].resample('A', how=lambda x: (x/100+1.0).prod() - 1.0) * 100
    year_rtn = stock_data.set_index('date')[['p_change', 'p_change_trix']].resample('A').apply(lambda x: ((x/100+1.0).prod() - 1.0) * 100)
    year_rtn.to_csv(codedir+'trixv2_year.csv', encoding='gbk')
    # ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
    stock_data.to_csv(codedir+'trixv2.csv', index=False)
    stock_data.tail(20).to_csv(codedir+'trixv2_Signal.csv', index=False)
    print 'the share %s trading sign:'%code
    print stock_data.tail(5)
    return

def analysis_dm(code):
    filename='./stockdata/data/last3year/'+code+'.csv'
    stock_data = pd.read_csv(filename, parse_dates=['date'])
    # 将数据按照交易日期从远到近排序
    #stock_data.sort('date', inplace=True)
    stock_data=stock_data[['date', 'open','high', 'low', 'close', 'p_change']]
    #########DMA指标的测试############
    #print 's以2天为间隔，测试范围从2～20天，L以5天为间隔，测试范围从20～120，M以5天为间隔，测试范围5～60。推荐s为10天，L为50天,m为10天'
    #lddma=input('Enter long date for DMA X -->')
    #sddma=input('Enter short date for DMA X-->')
    #mddma=input('Enter short date for DMA-->')
    lddma=50
    sddma=10
    mddma=10
    #stock_data['DMA_'+str(sddma)+'_'+str(lddma)]=pd.rolling_mean(stock_data['close'], sddma)-pd.rolling_mean(stock_data['close'], lddma)
    stock_data['DMA_'+str(sddma)+'_'+str(lddma)]=pd.Series.rolling(stock_data['close'], window=sddma,center=False).mean()-pd.Series.rolling(stock_data['close'], window=lddma,center=False).mean()
    stock_data['AMA_'+str(mddma)]=pd.Series.rolling(stock_data['DMA_'+str(sddma)+'_'+str(lddma)],window=mddma,center=False).mean()
    #买入信号：
    buy_index=stock_data[(stock_data['DMA_'+str(sddma)+'_'+str(lddma)]>stock_data['AMA_'+str(mddma)])&\
                         (stock_data['DMA_'+str(sddma)+'_'+str(lddma)].shift(1)<stock_data['AMA_'+str(mddma)].shift(1))].index
    stock_data.loc[buy_index,'Signal']=1
    sell_index=stock_data[(stock_data['DMA_'+str(sddma)+'_'+str(lddma)]<stock_data['AMA_'+str(mddma)])&\
                          (stock_data['DMA_'+str(sddma)+'_'+str(lddma)].shift(1)>stock_data['AMA_'+str(mddma)].shift(1))].index
    stock_data.loc[sell_index,'Signal']=0
    #stock_data.fillna(0, inplace=True)
    stock_data['position'] = stock_data['Signal'].shift(1)
    stock_data['position'].fillna(method='ffill', inplace=True)
    #当仓位为1时，已当天的开盘价买入股票，当仓位为0时，以收盘价卖出该股份。计算从数据期内的收益
    stock_data['Cash_index'] = ((stock_data['p_change']/100) * stock_data['position'] + 1.0).cumprod()
    initial_idx = 1
    #initial_idx = stock_data.iloc[0]['close'] / (1 + (stock_data.iloc[0]['p_change']/100))
    stock_data['Cash_index'] *= initial_idx
    print 'The MA methon Signal:'
    Make_decision(stock_data)
    # 通过复权价格计算接下来几个交易日的收益率
    for n in [1, 2, 3, 5, 10, 20]:
        stock_data['CP_next_'+str(n)+'_days'] = stock_data['close'].shift(-1*n) / stock_data['close'] - 1.0
        # 将数据按照交易日期从近到远排序
        #stock_data.sort('date', ascending=False, inplace=True)
        ##统计出现买点时点的数据
    dd=stock_data[stock_data['Signal']==1]
    if dd.shape[0]>0:
        print_return_next_n_day(dd)
    else:
        print 'There is no Signal for buy this share in the selected period.'
            
    codedir='./output/A/'+code+os.sep
    if not os.path.exists(codedir):
        os.mkdir(codedir)
    stock_data.to_csv(codedir+'dmav2.csv', index=False)
    stock_data.tail(20).to_csv(codedir+'dmav2_Signal.csv', index=False)
    # ==========计算每年指数的收益以及海龟交易法则的收益
    stock_data['p_change_dmaV2'] = (stock_data['p_change']) * stock_data['position']
    #year_rtn = stock_data.set_index('date')[['p_change', 'p_change_dmaV2']].resample('A', how=lambda x: (x/100+1.0).prod() - 1.0) * 100
    year_rtn = stock_data.set_index('date')[['p_change', 'p_change_dmaV2']].resample('A').apply(lambda x: ((x/100+1.0).prod() - 1.0) * 100)
    year_rtn.to_csv(codedir+'dmav2_year.csv', encoding='gbk')
    return

def tutlemethon(code):
    filename='./stockdata/data/last3year/'+code+'.csv'
    #    if len(code)==6:
    index_data = pd.read_csv(filename, parse_dates=['date'])
    # 保留这几个需要的字段：'date', 'high', 'low', 'close', 'change'
    index_data = index_data[['date','open', 'high', 'low', 'close', 'p_change']]
    # 对数据按照【date】交易日期从小到大排序
    #index_data.sort('date', inplace=True)
    # ==========计算海龟交易法则的买卖点
    # 设定海龟交易法则的两个参数，当收盘价大于最近N1天的最高价时买入，当收盘价低于最近N2天的最低价时卖出
    # 这两个参数可以自行调整大小，但是一般N1 > N2
    N1 = 20
    N2 = 10
    # 通过rolling_max方法计算最近N1个交易日的最高价
    #index_data['High_Close_Price_N1_Day'] =  pd.rolling_max(index_data['high'], N1)
    index_data['High_Close_Price_N1_Day'] =  pd.Series.rolling(index_data['high'],window=N1,center=False).max()
    # 对于上市不足N1天的数据，取上市至今的最高价
    #index_data['High_Close_Price_N1_Day'].fillna(value=pd.expanding_max(index_data['high']), inplace=True)
    index_data['High_Close_Price_N1_Day'].fillna(value=pd.Series.expanding(index_data['high'],min_periods=1)).max()
    # 通过相似的方法计算最近N2个交易日的最低价
    #index_data['Low_Close_Price_N2_Day'] =  pd.rolling_min(index_data['low'], N2)
    index_data['Low_Close_Price_N2_Day'] =  pd.Series.rolling(index_data['low'],window=N2,center=False).min()
    # 对于上市不足N2天的数据，取上市至今的最低价
    #index_data['Low_Close_Price_N2_Day'].fillna(value=pd.expanding_min(index_data['low']), inplace=True)
    index_data['Low_Close_Price_N2_Day'].fillna(value=pd.Series.expanding(index_data['low'],min_periods=1)).min()
    # 当当天的【close】> 昨天的【最近N1个交易日的最高点】时，将【收盘发出的信号】设定为1
    buy_index = index_data[index_data['close'] > index_data['High_Close_Price_N1_Day'].shift(1)].index
    index_data.loc[buy_index, 'Signal'] = 1
    # 当当天的【close】< 昨天的【最近N2个交易日的最低点】时，将【收盘发出的信号】设定为0
    sell_index = index_data[index_data['close'] < index_data['Low_Close_Price_N2_Day'].shift(1)].index
    index_data.loc[sell_index, 'Signal'] = 0
    # 计算每天的仓位，当天持有上证指数时，仓位为1，当天不持有上证指数时，仓位为0
    index_data['position'] = index_data['Signal'].shift(1)
    index_data['position'].fillna(method='ffill', inplace=True)
    # 取1992年之后的数据，排出较早的数据
    #index_data = index_data[index_data['date'] >= pd.to_datetime('19930101')]
    #当仓位为1时，已当天的开盘价买入股票，当仓位为0时，以收盘价卖出该股份。计算从数据期内的收益
    index_data['Cash_index'] = ((index_data['p_change']/100) * index_data['position'] + 1.0).cumprod()
    #initial_idx = index_data.iloc[0]['close'] / (1 + (index_data.iloc[0]['p_change']/100))
    initial_idx = 1
    index_data['Cash_index'] *= initial_idx
    print 'The turtle methon Signal:'
    Make_decision(index_data)
    # 通过复权价格计算接下来几个交易日的收益率
    for n in [1, 2, 3, 5, 10, 20]:
        index_data['CP_next_'+str(n)+'_days'] = index_data['close'].shift(-1*n) / index_data['close'] - 1.0
    dd=index_data[index_data['position']==1]
    #print_return_next_n_day(dd)
    # 输出数据到指定文件
    codedir='./output/A/'+code+os.sep
    if not os.path.exists(codedir):
        os.mkdir(codedir)   
    index_data[['date', 'high', 'low', 'close', 'p_change', 'High_Close_Price_N1_Day','Low_Close_Price_N2_Day', 'position', 'Cash_index']].to_csv(codedir+'turtle.csv', index=False, encoding='gbk')
        
    # ==========计算每年指数的收益以及海龟交易法则的收益
    index_data['p_change_turtle'] = (index_data['p_change']) * index_data['position']
    #year_rtn = index_data.set_index('date')[['p_change', 'p_change_turtle']].resample('A', how=lambda x: (x/100+1.0).prod() - 1.0) * 100
    year_rtn = index_data.set_index('date')[['p_change', 'p_change_turtle']].resample('A').apply(lambda x: ((x/100+1.0).prod() - 1.0) * 100)
    year_rtn.to_csv(codedir+'tuetle_year.csv', encoding='gbk')
    index_data.tail(20).to_csv(codedir+'turtle_Signal.csv', index=False, encoding='gbk')
    #print 'the share %s trading sign for Turtle:'%code
    #print index_data.tail(5)
    return

def get_local_code():
    code_list = []
    fpath='./stockdata/data/last3year/'
    for root, dirs, files in os.walk(fpath):# 注意：这里请填写数据文件在您电脑中的路径
        if files:
            for f in files:
                if '.csv' in f:
                    code_list.append(f.split('.csv')[0])
    return code_list

def listgetdata(code):
  filename='./stockdata/data/last3year/'+code+'.csv'
  if not os.path.exists(filename):
    #print 'Getting the data for %s: \n'%code
    df=ts.get_hist_data(code)
    df.sort_index(ascending=True,inplace=True)
    df.to_csv(filename)
  else:
    df=pd.read_csv(filename)
    tem=df.iloc[-1]['date']
    if tem!=today1:
      #print 'Updating the data from%s for %s:'%(tem,code)
      t=time.strptime(tem,'%Y-%m-%d')
      y,m,d=t[0:3]
      tt=datetime.datetime(y,m,d)
      bd=tt+datetime.timedelta(days=1)
      bday=bd.strftime('%Y-%m-%d')
      df=ts.get_hist_data(code,start=bday,end=today1)
      df.sort_index(ascending=True,inplace=True)
      df.to_csv(filename,encoding='gbk',header=None,mode='a')    
  return

def delect_same_rows(code,pf):
    fp=pf+code+'.csv'
    #print 'update file for %s'%code
    if os.path.exists(fp):
        df=pd.read_csv(fp)
        df.drop_duplicates(subset='date',inplace=True)
        df.sort_values(by='date',inplace=True)
        df.to_csv(fp)
    return
