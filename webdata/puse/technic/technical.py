#!/usr/bin/env python3
# -*-coding:utf-8-*-

import numpy,math


def ss_mean(values):
    ret = None
    if len(values):
        ret = numpy.array(values).mean()
    return ret


def ss_stddev(values, ddof=1):
    ret = None
    if len(values):
        ret = numpy.array(values).std(ddof=ddof)
    return ret


def sharpe_ratio(returns, riskFreeRate, tradingPeriods, annualized=True):
    # :param returns: The returns.
    # :param riskFreeRate: The risk free rate per annum.
    # :param tradingPeriods: The number of trading periods per annum.
    # :param annualized: True if the sharpe ratio should be annualized.
    # * If using daily bars, tradingPeriods should be set to 252.
    # * If using hourly bars (with 6.5 trading hours a day) then tradingPeriods should be set to 252 * 6.5 = 1638.
    
    ret = 0.0

    # From http://en.wikipedia.org/wiki/Sharpe_ratio: if Rf is a constant risk-free return throughout the period,
    # then stddev(R - Rf) = stddev(R).
    volatility = ss_stddev(returns, 1)

    if volatility != 0:
        rfPerReturn = riskFreeRate / float(tradingPeriods)
        avgExcessReturns = ss_mean(returns) - rfPerReturn
        ret = avgExcessReturns / volatility

        if annualized:
            ret = ret * math.sqrt(tradingPeriods)
    return ret

def sharpe_ratiov1(df, label='Close',riskFreeRate=0.0049,tradingPeriods=252, annualized=True):

    returns=df[label].pct_change()
    returns=returns.dropna(how='any')
    ret = 0.0
    #if len(returns)>252:
    #    returns=returns[-252:]

    volatility = ss_stddev(returns, 1)

        

    if volatility != 0:
        rfPerReturn = riskFreeRate / float(tradingPeriods)
        avgExcessReturns = ss_mean(returns) - rfPerReturn
        ret = avgExcessReturns / volatility

        if annualized:
            ret = ret * math.sqrt(tradingPeriods)
    return ret
