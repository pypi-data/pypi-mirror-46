import numpy as np
from ..signal.analysis import calculate_alternance


def calculate_alternance_map(data: np.ndarray,
                             t_start: int, t_end: int,
                             percentage: float = 80., apd_min: float = 10.) -> np.ndarray:
    """Calculate alternance of Action Potential map for ``percentage`` level repolarization
    of the signal in ``data`` along last axis.
    
    Parameters
    ----------
    ``data`` : np.ndarray, shape=(X, Y, T)
    ``t_start`` : int
    ``t_end`` : int
    ``percentage`` : float, optional
        level of signal to calculate duration (default is 80)
    ``APD_min`` : float, optional
        min action potential duration expected (default is 10)
        
    Returns
    -------
    np.ndarray, shape=(X, Y)
    """
    
    time = np.arange(t_start, t_end)
    alt_map = np.apply_along_axis(lambda x: calculate_alternance(time, x[t_start: t_end], percentage, apd_min), -1, data)
    return alt_map
