import numpy as np
from ..signal.processing import ensemble_average as ensemble_average_1d


def ensemble_average(data: np.ndarray, cycle_length: int) -> np.ndarray:
    """
    Ensemble average of ``data`` along last axis.
    
    Parameters
    ``data``: np.ndarray, shape=(X, Y, T)
    ``cycle_length`` : int
        averaging interval
        
    Returns
    -------
    np.ndarray, shape=(X, Y, ``cycle_length``)
    """
    
    time = np.arange(data.shape[-1])
    return np.apply_along_axis(lambda signal: ensemble_average_1d(time, signal, cycle_length)[1], -1, data)