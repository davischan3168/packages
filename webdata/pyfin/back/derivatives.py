#!/usr/bin/env python3
# -*-coding:utf-8-*-

from finance import *
import numpy as np

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
        discount_factor = self.discount_curve.get_discount_factors(
            (self.pricing_date, self.maturity))[0, 1]
        result = discount_factor * np.sum(cash_flow) / len(cash_flow)
        if full:
            return round(result, accuracy), discount_factor * cash_flow
        else:
            return round(result, accuracy)

if __name__=="__main__":
    me_gbm = market_environment('me_gbm', dt.datetime(2015, 1, 1))
    me_gbm.add_constant('initial_value', 36.)
    me_gbm.add_constant('volatility', 0.2)
    me_gbm.add_constant('final_date', dt.datetime(2015, 12, 31))
    me_gbm.add_constant('currency', 'EUR')
    me_gbm.add_constant('frequency', 'M')
    me_gbm.add_constant('paths', 10000)
    csr = constant_short_rate('csr', 0.06)
    gbm = geometric_brownian_motion('gbm', me_gbm)
    me_call = market_environment('me_call', me_gbm.pricing_date)
    me_call.add_constant('strike', 40.)
    me_call.add_constant('maturity', dt.datetime(2015, 12, 31))
    me_call.add_constant('currency', 'EUR')
    payoff_func = 'np.maximum(maturity_value - strike, 0)'
