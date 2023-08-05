import warnings
import psutil
from collections import namedtuple

import numpy as np

from .models import BlackScholes, Heston, RoughBergomi
from .ero import ero, simple_ero
from .ls import ls


class BasketPayoff:
    def __init__(self,f=lambda x:x,weights=None,weight_function=None):
        self.f = f
        self.weights=weights
        self.weight_function=weight_function
        self.d = None
    def __call__(self,log_securities):
        if self.d:
            log_securities = log_securities[...,:self.d]
        basket = np.exp(log_securities)
        if self.weight_function:
            weighted = self.weight_function(basket)
        else:
            weighted = np.sum(basket, axis=-1) if self.weights is None else basket@self.weights
        return self.f(weighted)
    def __repr__(self):
        return f'BasketPayoff(f={self.f},weights={self.weights},weight_function={self.weight_function})'

class CallPayoff(BasketPayoff):
    def __init__(self,K, weights=None, weight_function=None):
        self.K = K
        super().__init__(lambda x: np.clip(x-K,0,None), weights,weight_function)
    def __repr__(self):
        return f'CallPayoff(K={self.K},weights={self.weights},weight_function={self.weight_function})'

class PutPayoff(BasketPayoff):
    def __init__(self,K, weights=None, weight_function=None):
        self.K = K
        super().__init__(lambda x: np.clip(K-x,0,None), weights, weight_function)
    def __repr__(self):
        return f'PutPayoff(K={self.K},weights={self.weights},weight_function={self.weight_function})'

Valuation = namedtuple('Valuation','v_test std v_train v_europ method k M kwargs model')

def pryce(model, k, M, method='ero', **kwargs):
    result = {'ero':ero,'ls':ls,'simple_ero':simple_ero}[method](model,k,M,**kwargs)
    return Valuation(*result, method, k, M, kwargs, model)

