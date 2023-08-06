import numpy as np

def kernel_gaussian(kernel_size: int, sigma: float = None) -> np.ndarray:
    """Square gaussian kernel with given ``kernel_size`` and ``sigma``
    
    Parameters
    ----------
    ``kernel_size`` : int
        size of the kernel, must be 1, 3, 5, etc.
    ``sigma`` : float, optional
        standard deviation (default is None)
        
    Returns
    -------
    np.ndarray, shape=(``kernel_size``, ``kernel_size``)
    """
    
    if (kernel_size % 2 != 1) or (kernel_size < 1):
        msg = "kernel_size must be odd positive integer but '{}' was given".format(kernel_size)
        raise Exception(msg)
        
    if (sigma is None):
        sigma = kernel_size / (3. * 2)
    elif sigma <= 0:
        msg = "sigma must be positive value but '{}' was given".format(sigma)
        raise Exception(msg)

    kernel = np.zeros((kernel_size, kernel_size))

    i_center = kernel_size / 2
    j_center = i_center

    i_center_int = kernel_size // 2
    j_center_int = kernel_size // 2

    for i in range(i_center_int, kernel_size):
        for j in range(j_center_int, kernel_size):
            
            r = np.array([i - i_center, j - j_center])
            r_norm = np.linalg.norm(r)
            
            kernel_element = np.exp(-r_norm**2 / (2. * sigma**2))
            
            kernel[i, j] = kernel_element
            kernel[(kernel_size - 1) - i, j] = kernel_element
            kernel[i, (kernel_size - 1) - j] = kernel_element
            kernel[(kernel_size - 1) - i, (kernel_size - 1) - j] = kernel_element

    kernel = kernel / kernel.sum()
    
    return kernel