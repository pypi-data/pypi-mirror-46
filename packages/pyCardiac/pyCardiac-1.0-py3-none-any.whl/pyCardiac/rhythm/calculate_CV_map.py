import numpy as np
from . import calculate_activation_map


def calculate_CV_map(data: np.ndarray, t_start: int, t_end: int,
                     percentage: float = 90., dx: float = 1., dy: float = 1.) -> np.ndarray:
    """Calculate Conduction Velocity map from ``data`` in given time region.
    Uses activation mapping.
    
    Parameters
    ----------
    ``data`` : np.ndarray, shape=(X, Y, T)
    ``t_start`` : int
    ``t_end`` : int
    ``percentage`` : float, optional
        level of signal in percents that means activation (default is 90)
    ``dx`` : float, optional
        constant sample distance for X dimension (default is 1)
    ``dy`` : float, optional
        constant sample distance for Y dimension (default is 1)
        
    Returns
    -------
    np.ndarray, shape=(X, Y)
        x-velocities
    np.ndarray, shape=(X, Y)
        y-velocities
        
    """
        
    act_map = calculate_activation_map(data, t_start, t_end, percentage)
    CV_map = np.gradient(act_map, dx, dy)
    return CV_map