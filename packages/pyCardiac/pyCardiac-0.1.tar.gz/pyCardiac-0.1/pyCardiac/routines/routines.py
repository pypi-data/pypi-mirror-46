import numpy as np

def rescale(signal, v_min: float = 0., v_max: float = 1.) -> np.ndarray:
    """Rescale ``signal`` to [``v_min``, ``v_max``].
    
    Parameters
    ----------
    ``signal`` : array-like object, shape=(X)
        signal to rescale
    ``v_min`` : float, optional
        value minimum (default is 0)
    ``v_max`` : float, optional
        value maximum (default is 1)
        
    Returns
    -------
    numpy.ndarray, shape=(X)
        rescaled ``signal``
    """

    # rescaling to [0, 1]
    result = np.array(signal, dtype = float)
    result -= np.nanmin(result)
    result /= np.nanmax(result)

    # rescaling to [v_min, v_max] 
    v_ptp = v_max - v_min
    result *= v_ptp
    result += v_min

    return result
    

def moving_average(signal: np.ndarray, n: int = 3) -> np.ndarray:
    """Moving average of the signal with given window size.
    Source: https://stackoverflow.com/a/14314054
    
    Parameters
    ----------
    ``signal``: numpy.ndarray, shape=(X)
        signal to average
    ``n``: int, optional
        window size (default is 3)
    
    Returns
    -------
    numpy.ndarray, shape=(X - (n - 1))
    """

    signal_ = np.cumsum(signal, dtype = float)
    signal_[n:] = signal_[n:] - signal_[:-n]
    signal_averaged = signal_[n - 1:] / n
    return signal_averaged


def add_borders(matrix: np.ndarray,
                left_border_size: int,
                right_border_size: int,
                top_border_size: int,
                bottom_border_size: int,
                value: float = 0.) -> np.ndarray:
    """Adds borders with given sizes and filled with given ``value`` to ``matrix``.
    
    Parameters
    ----------
    ``matrix`` : numpy.ndarray, shape=(N, M)
        square matrix
    ``left_border_size`` : int
        size fo the left border to add
    ``right_border_size`` : int
        size fo the right border to add
    ``top_border_size`` : int
        size fo the top border to add
    ``bottom_border_size`` : int
        size fo the bottom border to add
    ``value`` : float, optional
        value to fill added borders (default is 0)
        
    Returns
    -------
    numpy.ndarray, shape=(X, Y)
        matrix with new borders
    """
    
    if (len(matrix.shape) != 2):
        msg = "matrix must be square"
        raise Exception(msg)
    
    n, m = matrix.shape

    A = np.full((n + top_border_size + bottom_border_size,
                 m + left_border_size + right_border_size),
                fill_value = value)

    top = top_border_size
    bottom = top_border_size + n
    left = left_border_size
    right = left_border_size + m

    A[top : bottom, left : right] = matrix  

    return A


def phase_difference(a: float, b: float) -> float:
    """Calculating phase difference of two values.
    
    Parameters
    ----------
    ``a`` : float
    ``b`` : float
    
    Returns
    -------
    float
        phase difference
    """
    
    if np.abs(a - b) <= np.pi:
        return a - b
    
    elif (a - b) > 0:
        return a - b - 2 * np.pi
    
    else:
        return a - b + 2 * np.pi
    

def char_to_float(c: int, f_min: float = -100., f_max: float = 50.) -> float:
    """Translates char number ``c`` from -128 to 127 to float from ``f_min`` to ``f_max``.
    
    Parameters
    ----------
    ``c`` : int
        value to translate
    ``f_min`` : float, optional
        (default is -100)
    ``f_max`` : float, optional
        (default is 50)
        
    Returns
    -------
    float
    """
    
    f = f_min + (f_max - f_min) * (c + 128.) / 255.
    return f


def float_to_char(f: float, f_min: float = -100., f_max: float = 50.) -> int:
    """Translates float number ``f`` from ``f_min`` to ``f_max`` to char from -128 to 127.
    
    Parameters
    ----------
    ``f`` : float
        value to translate
    ``f_min`` : float, optional
        (default is -100)
    ``f_max`` : float, optional
        (default is 50)
        
    Returns
    -------
    int
    """
    
    c = -128. + 255. * (f - f_min) / (f_max - f_min)
    c = int(c)
    return c

def scalar_multiplications(a, b):
    """ Scalar multiplications calculations (for autoscaling.py).
    Parameters
    ----------
    ``a`` : array-like object
    signal to scale
    ``b`` : array-like object
    reference signal
        
    Returns
    -------
    numpy.ndarray, shape=(5)
    """
    a, b = map(np.array, (a, b))
    coefficients = np.array([0., 0., 0., 0., 0.])
    coefficients[0] = np.sum(a * b)
    coefficients[1] = sum(a)
    coefficients[2] = sum(b)
    coefficients[3] = np.sum(a * a)
    coefficients[4] = sum(np.ones(len(a)))
    return coefficients

