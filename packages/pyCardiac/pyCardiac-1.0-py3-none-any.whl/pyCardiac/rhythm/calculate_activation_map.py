import numpy as np
from ..signal.analysis import calculate_activation_time


def calculate_activation_map(data: np.ndarray, t_start: int, t_end: int, percentage: float = 90.) -> np.ndarray:
    """Calculate activation map from ``data`` in given time region along last axis.
    
    Parameters
    ----------
    ``data`` : np.ndarray, shape=(X, Y, T)
    ``t_start`` : int
    ``t_end`` : int
    ``percentage`` : float, optional
        level of signal in percents that means activation (default is 90)
        
    Returns
    -------
    np.ndarray, shape=(X, Y)
    """
    
    time = np.arange(t_start, t_end)
    act_map = np.apply_along_axis(lambda x: calculate_activation_time(time, x[t_start: t_end], percentage), -1, data)
    return act_map
