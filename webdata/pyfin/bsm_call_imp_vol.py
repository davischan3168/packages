#!/usr/bin/env python3
# -*-coding:utf-8-*-
from time import time
from bsm_call_value import bsm_call_value
from bsm_vega import bsm_vega

def bsm_call_imp_vol(S0, K, T, r, C0, sigma_est, it=100):
    ''' Implied volatility of European call option in BSM model.
    Parameters
    ==========
    S0 : float
    initial stock/index level
    K : float
    strike price
    T : float
    maturity date (in year fractions)
    r : float
    constant risk-free short rate
    sigma_est : float
    estimate of impl. volatility
    it : integer
    number of iterations
    eturns
    =======
    simga_est : float
    numerically estimated implied volatility
    '''
    for i in range(it):
        sigma_est -= ((bsm_call_value(S0, K, T, r, sigma_est) - C0)
                      / bsm_vega(S0, K, T, r, sigma_est))
    return sigma_est
