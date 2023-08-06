import numpy as np


def calculate_activation_time(time: np.ndarray, signal: np.ndarray, percentage: float = 90.) -> float:
    """Calculate activation time for ``signal``.
    
    Parameters
    ----------
    ``time`` : np.array, shape(T)
    ``signal`` : np.ndarray, shape=(T)
    ``percentage`` : float, optional
        level of signal in percents that means activation (default is 90)
        
    Returns
    -------
    float or np.NaN in case of any problems
    """
        
    try:
        index_act = np.argmax(signal > signal.max() * percentage / 100.)
        t_act = time[index_act]
    except:
        t_act = np.NaN
    return t_act
