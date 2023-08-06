import numpy as np
from ...routines import phase_difference


def phase_singularity_detection_lasso(phase_array: np.ndarray, result: list,
                                      i_range: tuple = None, j_range: tuple = None):
    """Detects phase singularity points (PS) in ``phase_array`` with lasso method.
    
    Parameters
    ----------
    ``phase_array``: np.ndarray, shape=(X, Y)
    ``result`` : list
        list to append coordinates of PS
    ``i_range`` : tuple, optional
        range along first axis to process ``phase_array``
    ``j_range`` : tuple, optional
        range along seconf axis to process ``phase_array``
      
    Returns
    -------
    None
        use ``result`` to return PS coordinates 
    """
        
    if type(result) is not list:
        raise Exception("Invalid value of the argument: <result> must be a list!")
        
    if (i_range == None): # => j_range == None too
        i_range = (0, phase_array.shape[0])
        j_range = (0, phase_array.shape[1])
        
    i_min, i_max = i_range
    j_min, j_max = j_range
    i_middle, j_middle = (i_max + i_min) // 2, (j_max + j_min) // 2
    
    N, M = i_max - i_min, j_max - j_min # phase shape 
    
    diff = 0
    
    for i in range(i_min + 1, i_max):
        diff += phase_difference(phase_array[i-1, j_min], phase_array[i, j_min])
        diff -= phase_difference(phase_array[i-1, j_max-1], phase_array[i, j_max-1])
        
    for j in range(j_min + 1, j_max):
        diff -= phase_difference(phase_array[i_min, j-1], phase_array[i_min, j])
        diff += phase_difference(phase_array[i_max-1, j-1], phase_array[i_max-1, j])
        
    number_of_ps = np.round(abs(diff) / (2 * np.pi))
        
    if number_of_ps > 0:
        
        if ((N <= 3) and (M <= 3)):
            x = i_middle
            y = j_middle
            result.append([x, y])
        
        elif (N >= M):
            phase_singularity_detection_lasso(phase_array, result, (i_min, i_middle+1), (j_min, j_max))
            phase_singularity_detection_lasso(phase_array, result, (i_middle-1, i_max), (j_min, j_max))
            
        elif (M > N):
            phase_singularity_detection_lasso(phase_array, result, (i_min, i_max), (j_min, j_middle+1))
            phase_singularity_detection_lasso(phase_array, result, (i_min, i_max), (j_middle-1, j_max))      
    
    return number_of_ps


def phase_singularity_detection(phase_array: np.ndarray) -> np.ndarray:
    """Detects phase singularity points (PS) in ``phase_array``.
    
    Parameters
    ----------
    ``phase_array``: np.ndarray, shape=(X, Y)
    
    Returns
    -------
    np.ndarray, shape=(N, 2)
        x and y coordinates of PS 
    """
    
    i_list, j_list = [], []
    
    for i in range(1, phase_array.shape[0] - 1):
        for j in range(1, phase_array.shape[1] - 1):
            
            k11 = phase_difference(phase_array[i-1, j], phase_array[i-1, j-1])
            k21 = phase_difference(phase_array[i-1, j+1], phase_array[i-1, j])
            k31 = phase_difference(phase_array[i, j+1], phase_array[i-1, j+1])
            k32 = phase_difference(phase_array[i+1, j+1], phase_array[i, j+1])
            k33 = phase_difference(phase_array[i+1, j], phase_array[i+1, j+1])
            k23 = phase_difference(phase_array[i+1, j-1], phase_array[i+1, j])
            k13 = phase_difference(phase_array[i, j-1], phase_array[i+1, j-1])
            k12 = phase_difference(phase_array[i-1, j-1], phase_array[i, j-1])
            
            k = k11 + k21 + k32 + k33 + k23 + k13 + k12
            
            if np.abs(k) >= 3.0:
                i_list.append(i)
                j_list.append(j)
                
    result = np.array([i_list, j_list]).transpose()
                
    return result