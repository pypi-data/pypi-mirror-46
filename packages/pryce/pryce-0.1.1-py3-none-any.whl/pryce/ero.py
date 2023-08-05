import warnings
import psutil

import numpy as np
import numpy.random as rand
import scipy.optimize

from swutil.aux import split_integer
from swutil.hpc import EasyHPC
from swutil.np_tools import integral
from smolyak.applications.polynomials.polynomial_approximation import PolynomialSpace as PS

def _scale(G):
    try:
        return np.linalg.inv(scipy.linalg.cholesky(G))
    except Exception:
        w, v = [np.real(x) for x in scipy.linalg.eig(G)]
        return v@np.diag(1/np.sqrt(np.maximum(w, 1e-16)))

def simple_ero(model, k, M,**kwargs):
    '''
    Fully functioning implementation of ERO
    but uses a lot of memory
    '''
    poly_space = PS(n=1+model.d_eff, k=k)
    dt = model.T/(model.N-1)
    securities, times = model(M)
    payoffs = np.exp(-model.r * times)[:, None] *model.payoff(securities)
    arrays = [np.tile(times, M)[:, None], securities.reshape((model.N *M, -1), order='F')]
    polynomials = poly_space.evaluate_basis(np.concatenate(arrays, axis=1))
    scale = _scale(polynomials.T@polynomials/model.N/M)
    def psi(coeff):
        warnings.filterwarnings("ignore")
        intensities = np.exp(polynomials@(scale@coeff)).reshape((model.N, M), order='F')
        intensities[payoffs==0] = 0
        dintensities = intensities[..., None]*polynomials.reshape((model.N, M, -1), order='F')
        survivals = np.exp(np.concatenate([np.zeros((1, M)), -np.cumsum(intensities[:-1]*dt, axis=0)], axis=0))
        early = np.sum((survivals[:-1] - survivals[1:]) * payoffs[:-1])/M
        final = np.mean(survivals[-1] * payoffs[-1])
        dsurvivals = -survivals[..., None] * np.concatenate([np.zeros((1, M, poly_space.dimension)), np.cumsum(dintensities[:-1]*dt, axis=0)], axis=0)
        dsurvivals[np.isnan(dsurvivals)] = 0
        dearly = np.mean(np.sum((dsurvivals[:-1]-dsurvivals[1:])*payoffs[:-1, :, None], axis=0), axis=0)
        dfinal = np.mean(dsurvivals[-1]*payoffs[-1, :, None], axis=0)
        return -(early+final), -scale.T@(dearly+dfinal)
    return -scipy.optimize.minimize(
        psi,
        np.zeros(poly_space.dimension),
        method='L-BFGS-B',
        jac=True,
        options={'disp': False, 'gtol': 1e-60, 'ftol': 1e-60, 'maxfun': 20}
    ).fun, None, None, None

class ParallelPsi:
    '''
    Computational content is mostly in local function psi in __call__
    Everything else is parallelization.
    See simple_implementation.simple_ero for the core logic
    '''
    def __init__(self, model, k, M, parallel=False, save_memory=True):
        self.poly_space = PS(n=1+model.d_eff, k=k)
        self.model = model
        self.M = M
        self.N = self.model.N
        self.B = self.poly_space.dimension
        self.parallel = parallel
        self.save_memory = save_memory
        self.new_samples()
        @EasyHPC(parallel=self.parallel)
        def gram(j):
            _, _, polynomials = self.path_slice(j)
            N, M = polynomials.shape[:2]
            X = polynomials.reshape(M*N, -1)
            return X.T@X/N
        G = np.sum(gram(range(self.nslices)), axis=0) / self.M
        self.scale = _scale(G)

    def new_samples(self):
        ncpus = psutil.cpu_count(logical=False) if self.parallel else 1
        memavail = psutil.virtual_memory()[1]
        min_nslices = int(8*self.M*self.N*5*self.B/(memavail/2))+1 if self.save_memory else 1
        self.slice_sizes = split_integer(self.M, length=ncpus*min_nslices)
        mempredicted = 8*self.N*5*self.B*sum(self.slice_sizes[:ncpus])
        if mempredicted > memavail:
            raise ValueError(f'Computation would require {mempredicted/2**30}GB memory but only {memavail/2**30}GB are available. Use save_memory=True')
        self.storage = {}
        self.rand_states = [(rand.seed(rand.randint(2**32 - 1)), rand.get_state())[1]
                            for j in self.slice_sizes]
        self.nslices = len(self.slice_sizes)

    def path_slice(self, j):
        if j not in self.storage:
            rand.set_state(self.rand_states[j])
            securities, times = self.model(self.slice_sizes[j])
            payoffs = np.exp(-self.model.r * times)[:, None] * self.model.payoff(securities)
            N, M = securities.shape[:2]
            arrays = [np.tile(times, M)[:, None], securities.reshape((N * M, -1), order='F')]
            polynomials = self.poly_space.evaluate_basis(np.concatenate(arrays, axis=1)).reshape((N, M, -1), order='F')
            if not self.save_memory:
                self.storage[j] = times, payoffs, polynomials
        else:
            times, payoffs, polynomials = self.storage[j]
        return times, payoffs, polynomials

    def __call__(self, coeff=None, for_optimization=False):
        @EasyHPC(parallel=self.parallel)
        def psi(j):
            times, payoffs, polynomials = self.path_slice(j)
            if coeff is None:
                intensities = np.zeros(polynomials.shape[:2])
            else:
                warnings.filterwarnings("ignore")
                intensities = np.exp(np.einsum('ijk,k->ij', polynomials, self.scale@coeff))
            intensities[payoffs == 0] = 0
            dintensities = intensities[..., None]*polynomials
            survivals = np.exp(-integral(A=intensities, F=times, cumulative=True))
            early = np.sum((survivals[:-1] - survivals[1:]) * payoffs[:-1], axis=0)
            final = survivals[-1] * payoffs[-1]
            y = early + final
            dsurvivals = -survivals[..., None] * integral(A=dintensities, F=times, cumulative=True)
            dsurvivals[np.isnan(dsurvivals)] = 0
            dearly = np.sum((dsurvivals[:-1]-dsurvivals[1:])*payoffs[:-1, :, None], axis=0)
            dfinal = dsurvivals[-1]*payoffs[-1, :, None]
            dy = dearly + dfinal
            return np.mean(y), np.std(y), self.scale.T@np.mean(dy, axis=0)
        values, stds, derivatives = zip(*psi(range(self.nslices)))
        value = np.average(values, axis=0, weights=self.slice_sizes)
        value_std = np.sqrt(np.average(np.array(stds)**2, axis=0, weights=self.slice_sizes)/self.M)
        derivative = np.average(derivatives, axis=0, weights=self.slice_sizes)
        if for_optimization:
            return -value, -derivative
        else:
            return value, value_std

def ero(model, k, M=None, parallel=False, tol=1e-60, maxfun=20, save_memory=False):
    '''
    Compute American option prices using exercise rate optimization

    :param model: Market model
    :type model: Function that generates random market trajectories
    :param k: Polynomial degree
    :param M: Number of random market trajectories to be used in optimization
    :param parallel: Run computations in parallel
    :param save_memory: If you run out of memory
    '''
    psi = ParallelPsi(model, k, M, parallel=parallel, save_memory=save_memory)
    def callback(_, state={'ncalls': 0}):
        state['ncalls'] += 1
        print(f"{100*state['ncalls']/(maxfun):.0f}%", end='\r')
    result = scipy.optimize.minimize(
        lambda x: psi(x, for_optimization=True),
        np.zeros(psi.B),
        method='L-BFGS-B',
        jac=True,
        callback=callback,
        options={'disp': False, 'gtol': tol, 'ftol': tol, 'maxfun': maxfun}
    )
    v_train, coeff = -result.fun, result.x
    psi.new_samples()
    v_test, std = psi(coeff)
    v_europ, _ = psi()
    return v_test, std, v_train, v_europ
