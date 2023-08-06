import numpy as np
from ..routines import rescale as rescale_1d


def rescale(data: np.ndarray, v_min: float = 0., v_max: float = 1.) -> np.ndarray:
    """Rescale ``data`` to [``v_min``, ``v_max``] along last axis.
    
    Parameters
    ----------
    ``data`` : np.ndarray
    ``v_min`` : float, optional
        value minimum (default is 0)
    ``v_max`` : float, optional
        value maximum (default is 1)
        
    Returns
    -------
    numpy.ndarray
        rescaled ``data``
    """
    
    data_rescaled = np.apply_along_axis(rescale_1d, -1, data, v_min, v_max)
    return data_rescaled