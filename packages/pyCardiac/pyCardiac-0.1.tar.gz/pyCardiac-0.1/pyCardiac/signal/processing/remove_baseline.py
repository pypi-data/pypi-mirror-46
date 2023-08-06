import numpy as np
from scipy import sparse
from scipy.sparse.linalg import spsolve
from scipy.signal import detrend as detrend


def remove_baseline(data: np.ndarray, method_name: str = "linear", **kwargs) -> np.ndarray:
    """Remove baseline from the ``data`` with given method along last axis.
    
    Parameters
    ----------
    ``data`` : np.ndarray, shape=(N)
    ``method_name`` : str, optional
        could be 'linear' or 'least_squares' (default is 'least_squares')
    ``**kwargs``
        arbitrary keyword arguments
    
    Returns
    -------
    np.ndarray, shape=(N)
        ``data`` without baseline  
    """
    
    if (method_name == "linear"):
        signal_detrended = np.apply_along_axis(detrend, -1, data, **kwargs)
    elif (method_name == "least_squares"):
        trend = np.apply_along_axis(baseline_als, -1, data, **kwargs)
        signal_detrended = data - trend
    else:
        raise Exception("method_name may be 'linear' or 'least_squares' but {} given".format(method_name))
    
    return signal_detrended
    

def baseline_als(signal: np.ndarray, lam: float = 1e6,
                 p: float = 0.01, niter: int = 10) -> np.ndarray:    
    """
    Extract baseline from the ``signal``.
    
    Parameters
    ----------
    ``signal`` : np.ndarray, shape=(N)
    ``lam`` : float, optional
        smoothness parameter (default is 1e6)
    ``p`` : float, optional
        asymmetry parameter (default is 0.01)
    ``niter``: int, optional
        number of iterations (default is 10)
        
    Returns
    -------
    np.ndarray, shape=(N)
        baseline of the ``signal``
        
    References
    ----------
    Baseline Correction with Asymmetric Least Squares Smoothing
    Paul H. C. EilersHans F.M. Boelens, October 21, 2005

    Note
    ----
    Explanation from the article:
        There are two parameters: p for asymmetry and lam for smoothness.
        Both have to be tuned to the data at hand.
        We found that generally 0.001 < p < 0.1 is a good choice (for a signal with positive peaks)
        and 10^2 < lam < 10^9, but exceptions may occur.
        In any case one should vary lam on a grid that is approximately linear for log(lam).
        Often visual inspection is sufficient to get good parameter values.
    """
    
    L = len(signal)
    D = sparse.diags([1, -2, 1],
                     [0, -1, -2],
                     shape = (L, L - 2))
    weights = np.ones(L)
    for i in range(niter):
        W = sparse.spdiags(weights, 0, L, L)
        Z = W + lam * D.dot(D.transpose())
        baseline = spsolve(Z, weights * signal)
        weights = p * (signal > baseline) + (1 - p) * (signal < baseline)
        
    return baseline
