#!/usr/bin/env python3
# -*-coding:utf-8-*-
from math import log, sqrt, exp
import math
import numpy as np
import pandas as pd
from scipy import stats
from time import time
from random import gauss,seed
import datetime as dt

def bsm_call_value(S0, K, T, r, sigma):
    ''' Valuation of European call option in BSM model.
    Analytical formula.
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
    value : float
    present value of the European call option
    '''

    S0 = float(S0)
    d1 = (log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    d2 = (log(S0 / K) + (r - 0.5 * sigma ** 2) * T) / (sigma * sqrt(T))
    value = (S0 * stats.norm.cdf(d1, 0.0, 1.0)
             - K * exp(-r * T) * stats.norm.cdf(d2, 0.0, 1.0))
    # stats.norm.cdf --> cumulative distribution function
    #    for normal distribution
    return value

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

# Implied volatility function
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

def mcs_pure_python(S0, K, T, r, sigma, M, I):
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
    # Simulating I paths with M time steps
    dt = T / M

    S = []
    for i in range(I):
        path = []
        for t in range(M + 1):
            if t == 0:
                path.append(S0)
            else:
                z = gauss(0.0, 1.0)
                St = path[t - 1] * exp((r - 0.5 * sigma ** 2) * dt
                                       + sigma * sqrt(dt) * z)
                path.append(St)
        S.append(path)
    # Calculating the Monte Carlo estimator
    C0 = exp(-r * T) * sum([max(path[-1] - K, 0) for path in S]) / I
    # Results output
    tpy = time() - t0
    print("European Option Value %7.3f" % C0)
    print("Duration in Seconds %7.3f" % tpy)
    return C0

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

def get_year_deltas(date_list, day_count=365.):
    """ Return vector of floats with day deltas in years.
    Initial value normalized to zero.
    Parameters
    ==========
    date_list : list or array
    collection of datetime objects
    day_count : float
    number of days for a year
    Results
    =======
    delta_list : array
    year fractions
    """
    
    start = date_list[0]
    delta_list = [(date - start).days / day_count for date in date_list]
    return np.array(delta_list)

class constant_short_rate(object):
    """
    Class for constant short rate discounting.
    Attributes
    ==========
    name : string
    name of the object
    short_rate : float (positive)
    constant rate for discounting
    Methods
    =======
    get_discount_factors :
    get discount factors given a list/array of datetime objects
    or year fractions
    """
    def __init__(self, name, short_rate):
        self.name = name
        self.short_rate = short_rate
        if short_rate < 0:
            raise ValueError('Short rate negative.')
    def get_discount_factors(self, date_list, dtobjects=True):
        if dtobjects is True:
            dlist = get_year_deltas(date_list)
        else:
            dlist = np.array(date_list)
            dflist = np.exp(self.short_rate * np.sort(-dlist))
            return np.array((date_list, dflist)).T

class market_environment(object):
    """
    Class to model a market environment relevant for valuation.
    Attributes
    ==========
    name: string
    name of the market environment
    pricing_date : datetime object
    date of the market environment
    Methods
    =======
    add_constant :
    adds a constant (e.g. model parameter)
    get_constant :
    gets a constant
    add_list :
    adds a list (e.g. underlyings)
    get_list :
    gets a list
    add_curve :
    adds a market curve (e.g. yield curve)
    get_curve :
    gets a market curve
    add_environment :
    adds and overwrites whole market environments
    with constants, lists, and curves
    """
    def __init__(self, name, pricing_date):
        self.name = name
        self.pricing_date = pricing_date
        self.constants = {}
        self.lists = {}
        self.curves = {}
    def add_constant(self, key, constant):
        self.constants[key] = constant
    def get_constant(self, key):
        return self.constants[key]
    def add_list(self, key, list_object):
        self.lists[key] = list_object
    def get_list(self, key):
        return self.lists[key]
    def add_curve(self, key, curve):
        self.curves[key] = curve
    def get_curve(self, key):
        return self.curves[key]
    def add_environment(self, env):
        # overwrites existing values, if they exist
        for key in env.constants:
            self.constants[key] = env.constants[key]
        for key in env.lists:
            self.lists[key] = env.lists[key]
        for key in env.curves:
            self.curves[key] = env.curves[key]

def sn_random_numbers(shape, antithetic=True, moment_matching=True,fixed_seed=False):
    """
    Returns an array of shape shape with (pseudo)random numbers
    that are standard normally distributed.
    Parameters
    ==========
    shape : tuple (o, n, m)
    generation of array with shape (o, n, m)
    antithetic : Boolean
    generation of antithetic variates
    moment_matching : Boolean
    matching of first and second moments
    fixed_seed : Boolean
    flag to fix the seed
    Results
    =======
    ran : (o, n, m) array of (pseudo)random numbers
    """
    if fixed_seed:
        np.random.seed(1000)
    if antithetic:
        ran = np.random.standard_normal((shape[0], shape[1], int(shape[2] / 2)))
        ran = np.concatenate((ran, -ran), axis=2)
    else:
        ran = np.random.standard_normal(shape)
    if moment_matching:
        ran = ran - np.mean(ran)
        ran = ran / np.std(ran)
    if shape[0] == 1:
        return ran[0]
    else:
        return ran

#
# DX Library Simulation
# simulation_class.py
#
class simulation_class(object):
    """
    Providing base methods for simulation classes.
    Attributes
    ==========
    name : string
    name of the object
    mar_env : instance of market_environment
    market environment data for simulation
    corr : Boolean
    True if correlated with other model object
    Methods
    =======
    generate_time_grid :
    returns time grid for simulation
    get_instrument_values :
    returns the current instrument values (array)
    """
    def __init__(self, name, mar_env, corr):
        try:
            self.name = name
            self.pricing_date = mar_env.pricing_date
            self.initial_value = mar_env.get_constant('initial_value')
            self.volatility = mar_env.get_constant('volatility')
            self.final_date = mar_env.get_constant('final_date')
            self.currency = mar_env.get_constant('currency')
            self.frequency = mar_env.get_constant('frequency')
            self.paths = mar_env.get_constant('paths')
            self.discount_curve = mar_env.get_curve('discount_curve')
            try:
                # if time_grid in mar_env take this
                # (for portfolio valuation)
                self.time_grid = mar_env.get_list('time_grid')
            except:
                self.time_grid = None
            try:
                # if there are special dates, then add these
                self.special_dates = mar_env.get_list('special_dates')
            except:
                self.special_dates = []
            self.instrument_values = None
            self.correlated = corr
            if corr is True:
                # only needed in a portfolio context when
                # risk factors are correlated
                self.cholesky_matrix = mar_env.get_list('cholesky_matrix')
                self.rn_set = mar_env.get_list('rn_set')[self.name]
                self.random_numbers = mar_env.get_list('random_numbers')
        except:
            print ("Error parsing market environment.")
            
    def generate_time_grid(self):
        start = self.pricing_date
        end = self.final_date
        # pandas date_range function
        # freq = e.g. 'B' for Business Day,
        # 'W' for Weekly, 'M' for Monthly
        time_grid = pd.date_range(start=start, end=end,
                                  freq=self.frequency).to_pydatetime()
        time_grid = list(time_grid)
        # enhance time_grid by start, end, and special_dates
        if start not in time_grid:
            time_grid.insert(0, start)
            # insert start date if not in list
        if end not in time_grid:
            time_grid.append(end)
            # insert end date if not in list
        if len(self.special_dates) > 0:
            # add all special dates
            time_grid.extend(self.special_dates)
            # delete duplicates
            time_grid = list(set(time_grid))
            # sort list
            time_grid.sort()
        self.time_grid = np.array(time_grid)
        
    def get_instrument_values(self, fixed_seed=True):
        if self.instrument_values is None:
            # only initiate simulation if there are no instrument values
            self.generate_paths(fixed_seed=fixed_seed, day_count=365.)
        elif fixed_seed is False:
            # also initiate resimulation when fixed_seed is False
            self.generate_paths(fixed_seed=fixed_seed, day_count=365.)
        return self.instrument_values

class geometric_brownian_motion(simulation_class):
    """
    Class to generate simulated paths based on
    the Black-Scholes-Merton geometric Brownian motion model.
    Attributes
    ==========
    name : string
    name of the object
    mar_env : instance of market_environment
    market environment data for simulation
    corr : Boolean
    True if correlated with other model simulation object
    Methods
    =======
    update :
    updates parameters
    generate_paths :
    returns Monte Carlo paths given the market environment
    """
    def __init__(self, name, mar_env, corr=False):
        super(geometric_brownian_motion, self).__init__(name, mar_env, corr)
        
    def update(self, initial_value=None, volatility=None, final_date=None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if final_date is not None:
            self.final_date = final_date
        self.instrument_values = None
        
    def generate_paths(self, fixed_seed=False, day_count=365.):
        if self.time_grid is None:
            self.generate_time_grid()
            # method from generic simulation class
        # number of dates for time grid
        M = len(self.time_grid)
        # number of paths
        I = self.paths
        # array initialization for path simulation
        paths = np.zeros((M, I))
        # initialize first date with initial_value
        paths[0] = self.initial_value
        if not self.correlated:
            # if not correlated, generate random numbers
            rand = sn_random_numbers((1, M, I),
                                     fixed_seed=fixed_seed)
        else:
            # if correlated, use random number object as provided
            # in market environment
            rand = self.random_numbers
        short_rate = self.discount_curve.short_rate
        # get short rate for drift of process
        for t in range(1, len(self.time_grid)):
            # select the right time slice from the relevant
            # random number set
            if not self.correlated:
                ran = rand[t]
            else:
                ran = np.dot(self.cholesky_matrix, rand[:, t, :])
                ran = ran[self.rn_set]
            dt = (self.time_grid[t] - self.time_grid[t - 1]).days / day_count
            # difference between two dates as year fraction
            paths[t] = paths[t - 1] * np.exp((short_rate - 0.5
                                              * self.volatility ** 2) * dt
                                             + self.volatility * np.sqrt(dt) * ran)
            # generate simulated values for the respective date
        self.instrument_values = paths

class jump_diffusion(simulation_class):
    """
    Class to generate simulated paths based on
    the Merton (1976) jump diffusion model.
    Attributes
    ==========
    name : string
    name of the object
    mar_env : instance of market_environment
    market environment data for simulation
    corr : Boolean
    True if correlated with other model object
    Methods
    =======
    update :
    updates parameters
    generate_paths :
    returns Monte Carlo paths given the market environment
    """
    def __init__(self, name, mar_env, corr=False):
        super(jump_diffusion, self).__init__(name, mar_env, corr)
        try:
            # additional parameters needed
            self.lamb = mar_env.get_constant('lambda')
            self.mu = mar_env.get_constant('mu')
            self.delt = mar_env.get_constant('delta')
        except:
            print("Error parsing market environment.")
            
    def update(self, initial_value=None, volatility=None, lamb=None,
               mu=None, delta=None, final_date=None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if lamb is not None:
            self.lamb = lamb
        if mu is not None:
            self.mu = mu
        if delta is not None:
            self.delt = delta
        if final_date is not None:
            self.final_date = final_date
        self.instrument_values = None
        
    def generate_paths(self, fixed_seed=False, day_count=365.):
        if self.time_grid is None:
            self.generate_time_grid()
            # method from generic simulation class
        # number of dates for time grid
        M = len(self.time_grid)
        # number of paths
        I = self.paths
        # array initialization for path simulation
        paths = np.zeros((M, I))
        # initialize first date with initial_value
        paths[0] = self.initial_value
        if self.correlated is False:
            # if not correlated, generate random numbers
            sn1 = sn_random_numbers((1, M, I),
                                    fixed_seed=fixed_seed)
            
        else:
            # if correlated, use random number object as provided
            # in market environment
            sn1 = self.random_numbers
            
        # standard normally distributed pseudorandom numbers
        # for the jump component
        sn2 = sn_random_numbers((1, M, I),
                                fixed_seed=fixed_seed)
        rj = self.lamb * (np.exp(self.mu + 0.5 * self.delt ** 2) - 1)
        
        short_rate = self.discount_curve.short_rate
        for t in range(1, len(self.time_grid)):
            # select the right time slice from the relevant
            # random number set
            if self.correlated is False:
                ran = sn1[t]
            else:
                # only with correlation in portfolio context
                ran = np.dot(self.cholesky_matrix, sn1[:, t, :])
                ran = ran[self.rn_set]
            dt = (self.time_grid[t] - self.time_grid[t - 1]).days / day_count
            # difference between two dates as year fraction
            poi = np.random.poisson(self.lamb * dt, I)
            # Poisson-distributed pseudorandom numbers for jump component
            paths[t] = paths[t - 1] * (np.exp((short_rate - rj
                                               - 0.5 * self.volatility ** 2) * dt
                                              + self.volatility * np.sqrt(dt) * ran)
                                       + (np.exp(self.mu + self.delt *
                                                 sn2[t]) - 1) * poi)
        self.instrument_values = paths


class square_root_diffusion(simulation_class):
    """
    Class to generate simulated paths based on
    the Cox-Ingersoll-Ross (1985) square-root diffusion model.
    Attributes
    ==========
    name : string
    name of the object
    mar_env : instance of market_environment
    market environment data for simulation
    corr : Boolean
    True if correlated with other model object
    Methods
    =======
    update :
    updates parameters
    generate_paths :
    returns Monte Carlo paths given the market environment
    """
    def __init__(self, name, mar_env, corr=False):
        super(square_root_diffusion, self).__init__(name, mar_env, corr)
        try:
            self.kappa = mar_env.get_constant('kappa')
            self.theta = mar_env.get_constant('theta')
        except:
            print ("Error parsing market environment.")
            
    def update(self, initial_value=None, volatility=None, kappa=None,
               theta=None, final_date=None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if kappa is not None:
            self.kappa = kappa
        if theta is not None:
            self.theta = theta
        if final_date is not None:
            self.final_date = final_date
        self.instrument_values = None
        
    def generate_paths(self, fixed_seed=True, day_count=365.):
        if self.time_grid is None:
            self.generate_time_grid()
        M = len(self.time_grid)
        I = self.paths
        paths = np.zeros((M, I))
        paths_ = np.zeros_like(paths)
        paths[0] = self.initial_value
        paths_[0] = self.initial_value
        if self.correlated is False:
            rand = sn_random_numbers((1, M, I),
                                     fixed_seed=fixed_seed)
        else:
            rand = self.random_numbers
            
        for t in range(1, len(self.time_grid)):
            dt = (self.time_grid[t] - self.time_grid[t - 1]).days / day_count
            if self.correlated is False:
                ran = rand[t]
            else:
                ran = np.dot(self.cholesky_matrix, rand[:, t, :])
                ran = ran[self.rn_set]
                
            # full truncation Euler discretization
            paths_[t] = (paths_[t - 1] + self.kappa
                         * (self.theta - np.maximum(0, paths_[t - 1, :])) * dt
                         + np.sqrt(np.maximum(0, paths_[t - 1, :]))
                         * self.volatility * np.sqrt(dt) * ran)
            paths[t] = np.maximum(0, paths_[t])
        self.instrument_values = paths

class valuation_class(object):
    """ Basic class for single-factor valuation.
    Attributes
    ==========
    name : string
    name of the object
    underlying :
    instance of simulation class
    mar_env : instance of market_environment
    market environment data for valuation
    payoff_func : string
    derivatives payoff in Python syntax
    Example: 'np.maximum(maturity_value - 100, 0)'
    where maturity_value is the NumPy vector with
    respective values of the underlying
    Example: 'np.maximum(instrument_values - 100, 0)'
    where instrument_values is the NumPy matrix with
    values of the underlying over the whole time/path gridMethods
    =======
    update:
    updates selected valuation parameters
    delta :
    returns the Delta of the derivative
    vega :
    returns the Vega of the derivative
    """
    
    def __init__(self, name, underlying, mar_env, payoff_func=''):
        try:
            self.name = name
            self.pricing_date = mar_env.pricing_date
            try:
                self.strike = mar_env.get_constant('strike')
                # strike is optional
            except:
                pass
            self.maturity = mar_env.get_constant('maturity')
            self.currency = mar_env.get_constant('currency')
            # simulation parameters and discount curve from simulation object
            self.frequency = underlying.frequency
            self.paths = underlying.paths
            self.discount_curve = underlying.discount_curve
            self.payoff_func = payoff_func
            self.underlying = underlying
            # provide pricing_date and maturity to underlying
            self.underlying.special_dates.extend([self.pricing_date,
                                                  self.maturity])
        except:
            print('Error parsing market environment.')
            
    def update(self, initial_value=None, volatility=None,
               strike=None, maturity=None):
        if initial_value is not None:
            self.underlying.update(initial_value=initial_value)
        if volatility is not None:
            self.underlying.update(volatility=volatility)
        if strike is not None:
            self.strike = strike
        if maturity is not None:
            self.maturity = maturity
            # add new maturity date if not in time_grid
            if not maturity in self.underlying.time_grid:
                self.underlying.special_dates.append(maturity)
                self.underlying.instrument_values = None
                
    def delta(self, interval=None, accuracy=4):
        if interval is None:
            interval = self.underlying.initial_value / 50.
        # forward-difference approximation
        # calculate left value for numerical Delta
        value_left = self.present_value(fixed_seed=True)
        # numerical underlying value for right value
        initial_del = self.underlying.initial_value + interval
        self.underlying.update(initial_value=initial_del)
        # calculate right value for numerical delta
        value_right = self.present_value(fixed_seed=True)
        # reset the initial_value of the simulation object
        self.underlying.update(initial_value=initial_del - interval)
        delta = (value_right - value_left) / interval
        # correct for potential numerical errors
        if delta < -1.0:
            return -1.0
        elif delta > 1.0:
            return 1.0
        else:
            return round(delta, accuracy)
        
    def vega(self, interval=0.01, accuracy=4):
        if interval < self.underlying.volatility / 50.:
            interval = self.underlying.volatility / 50.
        # forward-difference approximation
        # calculate the left value for numerical Vega
        value_left = self.present_value(fixed_seed=True)
        # numerical volatility value for right value
        vola_del = self.underlying.volatility + interval
        # update the simulation object
        self.underlying.update(volatility=vola_del)
        # calculate the right value for numerical Vega
        value_right = self.present_value(fixed_seed=True)
        # reset volatility value of simulation object
        self.underlying.update(volatility=vola_del - interval)
        vega = (value_right - value_left) / interval
        return round(vega, accuracy)

class valuation_mcs_european(valuation_class):
    """
    Class to value European options with arbitrary payoff
    by single-factor Monte Carlo simulation.
    Methods
    =======
    generate_payoff :
         returns payoffs given the paths and the payoff function
    present_value :
         returns present value (Monte Carlo estimator)
    """
    
    def generate_payoff(self, fixed_seed=False):
        """
        Parameters
        ==========
        fixed_seed : Boolean
        use same/fixed seed for valuation
        """
        try:
            # strike defined?
            strike = self.strike
        except:
            pass
        paths = self.underlying.get_instrument_values(fixed_seed=fixed_seed)
        time_grid = self.underlying.time_grid
        try:
            time_index = np.where(time_grid == self.maturity)[0]
            time_index = int(time_index)
        except:
            print("Maturity date not in time grid of underlying.")
        maturity_value = paths[time_index]
        # average value over whole path
        mean_value = np.mean(paths[:time_index], axis=1)
        # maximum value over whole path
        max_value = np.amax(paths[:time_index], axis=1)[-1]
        # minimum value over whole path
        min_value = np.amin(paths[:time_index], axis=1)[-1]
        try:
            payoff = eval(self.payoff_func)
            return payoff
        except:
            print("Error evaluating payoff function.")
            
    def present_value(self, accuracy=6, fixed_seed=False, full=False):
        """
        Parameters
        ==========
        accuracy : int
            number of decimals in returned result
        fixed_seed : Boolean
            use same/fixed seed for valuation
        full : Boolean
            return also full 1d array of present values
        """
        cash_flow = self.generate_payoff(fixed_seed=fixed_seed)
        discount_factor = self.discount_curve.get_discount_factors((self.pricing_date, self.maturity))[0, 1]
        result = discount_factor * np.sum(cash_flow) / len(cash_flow)
        if full:
            return round(result, accuracy), discount_factor * cash_flow
        else:
            return round(result, accuracy)

if __name__=="__main__":
    """
    me_gbm = market_environment('me_gbm', dt.datetime(2015, 1, 1))
    me_gbm.add_constant('initial_value', 36.)
    me_gbm.add_constant('volatility', 0.2)
    me_gbm.add_constant('final_date', dt.datetime(2015, 12, 31))
    me_gbm.add_constant('paths', 10000)
    csr=constant_short_rate('csr',0.05)
    me_gbm.add_curve('discount_curve',csr)
    me_gbm.add_constant('currency', 'EUR')
    me_gbm.add_constant('frequency', 'M')
    gbm = geometric_brownian_motion('gbm', me_gbm)
    gbm.generate_time_grid()
    gbm.time_grid
    """
    me_gbm = market_environment('me_gbm', dt.datetime(2015, 1, 1))
    me_gbm.add_constant('initial_value', 36.)
    me_gbm.add_constant('volatility', 0.2)
    me_gbm.add_constant('final_date', dt.datetime(2015, 12, 31))
    me_gbm.add_constant('currency', 'EUR')
    me_gbm.add_constant('frequency', 'M')
    me_gbm.add_constant('paths', 10000)
    csr = constant_short_rate('csr', 0.06)
    me_gbm.add_curve('discount_curve',csr)
    gbm = geometric_brownian_motion('gbm', me_gbm)
    me_call = market_environment('me_call', me_gbm.pricing_date)
    me_call.add_constant('strike', 40.)
    me_call.add_constant('maturity', dt.datetime(2015, 12, 31))
    me_call.add_constant('currency', 'EUR')
    payoff_func = 'np.maximum(maturity_value - strike, 0)'
    eur_call = valuation_mcs_european('eur_call', underlying=gbm,
                                      mar_env=me_call, payoff_func=payoff_func)
    
    #"""
