#!/usr/bin/env python3
# -*-coding:utf-8-*-

import math
from math import log, sqrt, exp
from scipy import stats
def bsm_vega(S0, K, T, r, sigma):
    ''' Vega of European option in BSM model.
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
    sigma : float
    volatility factor in diffusion term
    Returns
    =======
    vega : float
    partial derivative of BSM formula with respect
    to sigma, i.e. Vega
    '''
    S0 = float(S0)
    d1 = (log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    vega = S0 * stats.norm.cdf(d1, 0.0, 1.0) * sqrt(T)
    return vega
