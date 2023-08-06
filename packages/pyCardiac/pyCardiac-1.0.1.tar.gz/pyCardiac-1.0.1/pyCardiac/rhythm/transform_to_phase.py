import numpy as np
from ..signal.processing import transform_to_phase as transform_to_phase_1d


def transform_to_phase(data: np.ndarray) -> np.ndarray:
    """Transform ``data`` to phase via Hilbert transform along last axis.
    
    Parameters
    ----------
    ``data`` : np.ndarray
    
    Returns
    -------
    np.ndarray
        phase array
    """
        
    return transform_to_phase_1d(data)
