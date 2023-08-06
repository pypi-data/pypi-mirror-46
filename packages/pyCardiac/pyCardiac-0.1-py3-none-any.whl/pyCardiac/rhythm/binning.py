import numpy as np
from ..signal.processing.filtration import binning as binning_1d


def binning(data: np.ndarray, kernel_size: int = 3, kernel_name: str = 'uniform', mask: np.ndarray = None) -> np.ndarray:
    return binning_1d(data, kernel_size, kernel_name, mask)

binning.__doc__ = binning_1d.__doc__