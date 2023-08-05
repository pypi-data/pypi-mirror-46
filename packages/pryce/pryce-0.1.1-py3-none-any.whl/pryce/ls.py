import numpy as np
from smolyak.applications.polynomials.polynomial_approximation import PolynomialSpace as PS
from smolyak.applications.polynomials.polynomial_approximation import PolynomialApproximation as PA


def ls(model, k, M, **kwargs):
    '''
    Compute American option prices using the Longstaff--Schwartz algorithm

    :param model: Market model
    :type model: Function that generates random market trajectories
    :param k: Polynomial degree
    :param M: Number of random market trajectories to be used in optimization
    '''
    poly_space = PS(n = model.d_eff, k = k)
    securities, times = model(M)
    N = model.N
    poly_continuation = lambda x: -np.inf*np.ones(M)
    coeff_payoff = 1
    coeff_poly = np.zeros(poly_space.dimension)
    coeffs = [(coeff_poly, coeff_payoff)]
    for i in range(N-2, -1, -1):
        print(f'{10+(N-2-i)/(N-2)*60:.0f}%',end='\r')
        payoffs = model.payoff(securities[i+1])
        y = np.exp(-model.r * (times[i+1]-times[i])) * np.maximum(payoffs, coeff_payoff*payoffs+poly_continuation(securities[i+1, ...]))
        x = securities[i, ...]
        coeff_poly, _, coeff_payoff = poly_space.weighted_least_squares(
            X=x,
            Y=y,
            basis_extension=lambda x: model.payoff(x).reshape(-1, 1)
        )
        poly_continuation = PA(poly_space, coeff_poly)
        coeffs.append([coeff_poly, coeff_payoff])
    init_payoff = model.payoff(securities[0, 0])
    v_train = np.maximum(init_payoff, np.mean(y))
    securities, times = model(M)
    stopped = np.zeros(M, dtype = bool)
    gain = np.nan*np.zeros(M)
    for i in range(N):
        print(f'{80+20*i/(N-1):.0f}%',end='\r')
        payoffs = model.payoff(securities[i])
        coeff_poly, coeff_payoff = coeffs[~i]
        continuation_value = coeff_payoff*payoffs+PA(poly_space, coeff_poly)(securities[i, ...])
        stop = (payoffs >= continuation_value)
        gain[~stopped & stop] = np.exp(-model.r*times[i])*payoffs[~stopped & stop]
        stopped |= stop
    return np.mean(gain), np.std(gain)/np.sqrt(M), v_train, np.exp(-model.r*model.T)*np.mean(payoffs)
