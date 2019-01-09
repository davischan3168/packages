#!/usr/bin/env python3
# -*-coding:utf-8-*-

import math
import numpy as np
from time import time

def mcs_full_vector_numpy(S0, K, T, r, sigma, M, I):
    seed(20000)
    t0 = time()
    """
    # Parameters
    S0 = 100. # initial value
    K = 105. # strike price
    T = 1.0 # maturity
    r = 0.05 # riskless short rate
    sigma = 0.2 # volatility
    M = 50 # number of time steps
    dt = T / M # length of time interval
    I = 250000 # number of paths
    """
    dt = T / M
    # Simulating I paths with M time steps
    S = S0 * np.exp(np.cumsum((r - 0.5 * sigma ** 2) * dt
                        + sigma * math.sqrt(dt)
                        * np.random.standard_normal((M + 1, I)), axis=0))
    # sum instead of cumsum would also do
    # if only the final values are of interest
    S[0] = S0
    
    # Calculating the Monte Carlo estimator
    C0 = math.exp(-r * T) * np.sum(np.maximum(S[-1] - K, 0)) / I


    # Results output
    tpy = time() - t0
    print("European Option Value %7.3f" % C0)
    print("Duration in Seconds %7.3f" % tpy)
    return C0
