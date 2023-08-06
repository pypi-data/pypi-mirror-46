"""
Basic routines for other modules and functions
==============================================

rescale
moving_average
add_borders
phase_difference
char_to_float
float_to_char
scalar_multiplications
kernel_gaussian
awgn
"""


__all__ = ['rescale',
           'moving_average',
           'add_borders',
           'phase_difference',
           'char_to_float',
           'float_to_char',
           'scalar_multiplications',
           'kernel_gaussian',
           'awgn']

from .routines import rescale, moving_average, add_borders, phase_difference, char_to_float, float_to_char, scalar_multiplications
from .kernel_gaussian import kernel_gaussian
from .awgn import awgn
