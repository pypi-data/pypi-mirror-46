import numpy as np
from swutil.time import Timer
from swutil.decorators import print_runtime
from pryce import pryce, BlackScholes, PutPayoff, CallPayoff, RoughBergomi, Heston

@print_runtime
def run_example(example, method, L, M, k, d, K, S0, J=0):
        T = 1
        r = 0.05
        if example.lower() == 'vanillaput':
            if d == 3:
                chol = np.linalg.cholesky(
                    [
                        [1, 0.8, 0.3],
                        [0.8, 1, 0.1],
                        [0.3, 0.1, 1]
                    ]
                )
                sigma = [[0.2], [0.15], [0.1]] * chol
                sigma = 0.3
            elif d==10:
                chol = np.linalg.cholesky([
                    [ 1.   ,  0.2  ,  0.2  ,  0.35 ,  0.2  ,  0.25 ,  0.2  ,  0.2  , 0.3  ,  0.2  ],
                    [ 0.2  ,  1.   ,  0.2  ,  0.2  ,  0.2  ,  0.125,  0.45 ,  0.2  , 0.2  ,  0.45 ],
                    [ 0.2  ,  0.2  ,  1.   ,  0.2  ,  0.2  ,  0.2  ,  0.2  ,  0.2  , 0.45 ,  0.2  ],
                    [ 0.35 ,  0.2  ,  0.2  ,  1.   ,  0.2  ,  0.2  ,  0.2  ,  0.2  , 0.425,  0.2  ],
                    [ 0.2  ,  0.2  ,  0.2  ,  0.2  ,  1.   ,  0.1  ,  0.2  ,  0.2  , 0.5  ,  0.2  ],
                    [ 0.25 ,  0.125,  0.2  ,  0.2  ,  0.1  ,  1.   ,  0.2  ,  0.2  , 0.35 ,  0.2  ],
                    [ 0.2  ,  0.45 ,  0.2  ,  0.2  ,  0.2  ,  0.2  ,  1.   ,  0.2  , 0.2  ,  0.2  ],
                    [ 0.2  ,  0.2  ,  0.2  ,  0.2  ,  0.2  ,  0.2  ,  0.2  ,  1.   , 0.2  , -0.1  ],
                    [ 0.3  ,  0.2  ,  0.45 ,  0.425,  0.5  ,  0.35 ,  0.2  ,  0.2  , 1.   ,  0.2  ],
                    [ 0.2  ,  0.45 ,  0.2  ,  0.2  ,  0.2  ,  0.2  ,  0.2  , -0.1  , 0.2  ,  1.   ]])
                diag = 0.3
                sigma = diag*chol
            else:
                sigma = 0.3
            model = BlackScholes(
                d=d,
                T=T,
                sigma=sigma,
                r=r,
                S0=S0*np.ones(d),
                L = L,
                payoff = PutPayoff(K,1/d*np.ones(d)),
            )
        elif example.lower()=='maxcall':
            payoff = CallPayoff(K, weight_function=lambda x: np.max(x, axis=-1))
            model = BlackScholes(
                d=d,
                T=3,
                sigma=0.2,
                r=0.05,
                S0= S0 * np.ones((d,)), 
                L=3,
                payoff=payoff,
                dividend = 0.1
            )
        elif example.lower() == 'heston':
            if d==10:
                rho = np.array([
                    [ 1.   ,  0.2  ,  0.2  ,  0.35 ,  0.2  ,  0.25 ,  0.2  ,  0.2  , 0.3  ,  0.2  , -0.5],
                    [ 0.2  ,  1.   ,  0.2  ,  0.2  ,  0.2  ,  0.125,  0.45 ,  0.2  , 0.2  ,  0.45 ,-0.5],
                    [ 0.2  ,  0.2  ,  1.   ,  0.2  ,  0.2  ,  0.2  ,  0.2  ,  0.2  , 0.45 ,  0.2  ,-0.5],
                    [ 0.35 ,  0.2  ,  0.2  ,  1.   ,  0.2  ,  0.2  ,  0.2  ,  0.2  , 0.425,  0.2  ,-0.5],
                    [ 0.2  ,  0.2  ,  0.2  ,  0.2  ,  1.   ,  0.1  ,  0.2  ,  0.2  , 0.5  ,  0.2  ,-0.5],
                    [ 0.25 ,  0.125,  0.2  ,  0.2  ,  0.1  ,  1.   ,  0.2  ,  0.2  , 0.35 ,  0.2  ,-0.5],
                    [ 0.2  ,  0.45 ,  0.2  ,  0.2  ,  0.2  ,  0.2  ,  1.   ,  0.2  , 0.2  ,  0.2  ,-0.5],
                    [ 0.2  ,  0.2  ,  0.2  ,  0.2  ,  0.2  ,  0.2  ,  0.2  ,  1.   , 0.2  , -0.1  ,-0.5],
                    [ 0.3  ,  0.2  ,  0.45 ,  0.425,  0.5  ,  0.35 ,  0.2  ,  0.2  , 1.   ,  0.2  ,-0.5],
                    [ 0.2  ,  0.45 ,  0.2  ,  0.2  ,  0.2  ,  0.2  ,  0.2  , -0.1  , 0.2  ,  1.   ,-0.5],
                    [-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,-0.5,1]
                ])
            elif d==1:
                rho =-0.5
            else:
                rho = np.eye(d+1)
            model = Heston(
                d=d,
                T=T,
                r=r,
                nu0=0.15,
                theta = 0.05,
                kappa = 3,
                xi = 0.5,
                rho = rho,
                S0=S0*np.ones(d),
                L = L,
                payoff = PutPayoff(K, 1/d*np.ones(d))
            )
        elif example.lower() == 'rbergomi':
            model = RoughBergomi(
                T=T,
                r=r,
                H=0.07,
                eta=1.9,
                xi = 0.3**2,
                rho = -0.9,
                S0=S0,
                L = L,
                payoff = PutPayoff(K),
                J = 3,
                memory = T/2,
            )
        return pryce(model=model,k=k,M=M, method=method,parallel = False, save_memory = True)

print(run_example(
    example='maxcall',
    method='ls',
    K=1,
    S0=1,
    L=2,
    d=1,
    k=2,
    M=200*2**8
)) 
