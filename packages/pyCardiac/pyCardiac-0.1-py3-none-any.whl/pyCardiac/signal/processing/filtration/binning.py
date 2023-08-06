import numpy as np
from ....routines import kernel_gaussian, add_borders


def binning(data: np.ndarray, kernel_size: int = 3, kernel_name: str = 'uniform', mask: np.ndarray = None) -> np.ndarray:
    
    """Binning of ``data`` with given kernel and ``mask``.
    
    Parameters
    ----------
    ``data`` : np.ndarray, shape=(X, Y) or (X, Y, T)
        data to apply binning
    ``kernel_size`` : int, optional
        (default is 3)
    ``kernel_name`` : str, optional
        could be 'uniform' or 'gaussian' (default is gaussian)
    ``mask`` : np.ndarray, optional
        mask for data, shape=(X, Y)
        (default is None)
        
    Returns
    -------
    np.ndarray, shape of ``data``
        ``data`` binned
    """
    
    if kernel_name == 'uniform':
            kernel = np.ones((kernel_size, kernel_size)) / kernel_size**2
    elif kernel_name == 'gaussian':
            kernel = kernel_gaussian(kernel_size)
    else:
        raise Exception("kernel_name must be 'uniform' or 'gaussian' but '{}' was given".format(kernel_name))
   
    if len(data.shape) == 2:
        data_ = data.reshape(data.shape[0], data.shape[1], 1)
    elif len(data.shape) == 3:
        data_ = data
    else:
        msg = "data must have 2 or 3 dimentions but it has {}".format(len(data.shape))
        raise Exception(msg)

    N, M, T = data_.shape
            
    if mask is None:
        mask = np.ones_like(data_[:, :, 0])
    elif (mask.shape[0] != N) or (mask.shape[1] != M):
        msg = "mask must have shape ({0}, {1}) but has ({2}, {3})".format(N, M, mask.shape[0], mask.shape[1])
        raise Exception(msg)

    data_binned = np.zeros(data_.shape)

    kernel_size_half = kernel_size // 2

    
    for y in range(N):
        for x in range(M):

            if mask[y, x]:

                range_x = [x - kernel_size_half, x + kernel_size_half]
                range_y = [y - kernel_size_half, y + kernel_size_half]
                
                left_border_size = 0
                right_border_size = 0
                top_border_size = 0
                bottom_border_size = 0

                if range_x[0] < 0:
                    left_border_size = -range_x[0]
                if range_x[1] > M - 1:
                    right_border_size = range_x[1] - (M - 1)
                if range_y[0] < 0:
                    top_border_size = -range_y[0]
                if range_y[1] > N - 1:
                    bottom_border_size = range_y[1] - (N - 1)
                    
                mask_window = mask[range_y[0] + top_border_size : (range_y[1] + 1) - bottom_border_size,
                                   range_x[0] + left_border_size : (range_x[1] + 1) - right_border_size]
                
                mask_window = add_borders(mask_window,
                                                  left_border_size,
                                                  right_border_size,
                                                  top_border_size,
                                                  bottom_border_size)           

                kernel_current = kernel * mask_window
                kernel_current = kernel_current[top_border_size : kernel_size - bottom_border_size,
                                                left_border_size : kernel_size - right_border_size]  
                
                data_windows = data_[range_y[0] + top_border_size : (range_y[1] + 1) - bottom_border_size,
                                     range_x[0] + left_border_size : (range_x[1] + 1) - right_border_size,
                                     :]

                temp = np.rollaxis(data_windows, 2) * kernel_current
                data_binned[y, x, :] = np.sum(temp, axis = (1, 2))           

    if len(data.shape) == 2:
        return data_binned[:, :, 0]
    elif len(data.shape) == 3:
        return data_binned
