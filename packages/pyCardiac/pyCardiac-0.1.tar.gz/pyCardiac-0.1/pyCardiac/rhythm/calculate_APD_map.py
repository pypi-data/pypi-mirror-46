import numpy as np
from ..signal.analysis import calculate_APD


def calculate_APD_map(data: np.ndarray, t_start: int, t_end: int, percentage: float = 80.) -> np.ndarray:
    """ Calculate Action Potential Duration map for ``percentage`` level repolarization
    of the signal in ``data`` along last axis.
    
    Parameters
    ``data`` : np.ndarray, shape=(X, Y, T)
    ``t_start`` : int
    ``t_end`` : int
    ``percentage`` : float, optional
        level of signal to calculate duration (default is 80)
        
    Returns
    -------
    np.ndarray, shape=(X, Y)
    """
        
    time = np.arange(t_start, t_end)
    apd_map = np.apply_along_axis(lambda x: calculate_APD(time, x[t_start: t_end], percentage), -1, data)
    return apd_map