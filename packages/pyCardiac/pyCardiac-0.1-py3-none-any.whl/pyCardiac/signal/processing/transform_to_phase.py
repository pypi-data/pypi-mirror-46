import numpy as np
from scipy.signal import hilbert as hilbert_transform
from ...routines import rescale


def transform_to_phase(signal):
    """Transform ``signal`` to phase via Hilbert transform along last axis`.
    
    Parameters
    ----------
    ``signal`` : np.ndarray
    
    Returns
    -------
    np.ndarray
        phase array
    """
    
    signal_centered = np.apply_along_axis(lambda x: rescale(x) - 0.5, -1, signal)
    signal_hilbert = np.apply_along_axis(hilbert_transform, -1, signal_centered)
    phase = np.apply_along_axis(np.angle, -1, signal_hilbert)
    return phase
