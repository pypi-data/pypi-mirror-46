import numpy as np
from ...routines import rescale


def normalize(signal) -> np.ndarray:
    """Scaling ``signal`` to [0, 1].
    
    Parameters
    ----------
    ``signal`` : array-like object
    
    Returns
    -------
    np.ndarray, shape of signal
        normilized signal
    """    
        
    return rescale(signal)
