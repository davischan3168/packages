#!/usr/bin/env python3
# -*-coding:utf-8-*-

import math
import numpy as np
from time import time

def mcs_vector_numpy(S0, K, T, r, sigma, M, I):
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
    
    S = np.zeros((M + 1, I))
    S[0] = S0
    for t in range(1, M + 1):
        z = np.random.standard_normal(I) # pseudorandom numbers
        S[t] = S[t - 1] * np.exp((r - 0.5 * sigma ** 2) * dt
                                 + sigma * math.sqrt(dt) * z)
        # vectorized operation per time step over all paths
        
    # Calculating the Monte Carlo estimator
    C0 = math.exp(-r * T) * np.sum(np.maximum(S[-1] - K, 0)) / I

    # Results output
    tpy = time() - t0
    print("European Option Value %7.3f" % C0)
    print("Duration in Seconds %7.3f" % tpy)
    return C0
