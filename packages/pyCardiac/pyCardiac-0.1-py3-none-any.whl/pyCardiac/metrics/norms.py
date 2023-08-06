"""
Metrics below may be used to compare goodness of fit between Action Potentials via Genetic Algorithm.
"""

import numpy as np

def ssd(a, b):
    """ Sum Of Squared Differences (SSD) calculation.
        
        Parameters
        ----------
        ``a`` : array-like object
            first signal
        ``b`` : array-like object
            second signal
        
        Returns
        -------
        float
            SSD value
    """
    A = np.array(a)
    B = np.array(b)
    return np.sum((A - B) * (A - B))


def sd(a, b):
    """ Standard deviation (SD) calculation.
            
        Parameters
        ----------
        ``a`` : array-like object
            first signal
        ``b`` : array-like object
            second signal
            
        Returns
        -------
        float
            SD value
    """
    
    A = np.array(a)
    B = np.array(b)
    summation = np.sum((A - B) * (A - B)) / A.size
    return np.sqrt(summation)

