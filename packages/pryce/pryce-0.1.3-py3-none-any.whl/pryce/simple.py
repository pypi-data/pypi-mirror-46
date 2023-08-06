import numpy as np
import scipy 
from smolyak.applications.polynomials.polynomial_approximation import PolynomialSpace as PS

def simple_ero(model,k,M):
    poly_space = PS(n=1+model.d_eff, k=k)
    dt = model.T/(model.N-1)
    securities,times = model(M)
    payoffs = np.exp(-model.r * times)[:,None] *model.payoff(securities[...,:model.d])
    arrays = [np.tile(times,M)[:,None], securities.reshape((model.N *M, -1),order='F')]
    polynomials = poly_space.evaluate_basis(np.concatenate(arrays,axis=1))
    try:
        return np.linalg.inv(scipy.linalg.cholesky(G))
    except:
        w,v = [np.real(x) for x in scipy.linalg.eig(G)]
        return v@np.diag(1/np.sqrt(np.maximum(w,1e-16)))
    def psi(coeff):
        warnings.filterwarnings("ignore")
        intensities = np.exp(polynomials@(scale@coeff)).reshape((model.N,M),order='F')
        intensities[payoffs==0] = 0
        dintensities = intensities[...,None]*polynomials.reshape((model.N,M,-1),order='F')
        survivals = np.exp(np.concatenate([np.zeros((1,M)),-np.cumsum(intensities[:-1]*dt,axis=0)],axis=0))
        early = np.sum((survivals[:-1] - survivals[1:]) * payoffs[:-1])/M
        final = np.mean(survivals[-1] * payoffs[-1])
        dsurvivals = -survivals[..., None] * np.concatenate([np.zeros((1,M,len(poly_space.basis))),np.cumsum(dintensities[:-1]*dt,axis=0)],axis=0)
        dsurvivals[np.isnan(dsurvivals)] = 0
        dearly = np.mean(np.sum((dsurvivals[:-1]-dsurvivals[1:])*payoffs[:-1,:,None],axis=0),axis=0)
        dfinal = np.mean(dsurvivals[-1]*payoffs[-1, :, None],axis=0)
        return early+final,scale.T@(dearly+dfinal)
    return -scipy.optimize.minimize(
        lambda x: -psi(x),
        np.zeros(len(poly_space.basis)),
        method='L-BFGS-B',
        jac=True,
        options={'disp': False, 'gtol': 1e-60, 'ftol': 1e-60, 'maxfun': 20}
    ).fun
