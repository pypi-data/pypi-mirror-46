"""
Signal processing before analysis
=================================

filtration (module)
remove_baseline
baseline_als
transform_to_phase
normalize
autoscaling
ensemble_average
"""

__all__ = ['filtration', 
           
           'remove_baseline',
           'baseline_als',
           
           'transform_to_phase',
           'autoscaling',
           'ensemble_average']


from . import filtration

from .remove_baseline import remove_baseline, baseline_als
from .transform_to_phase import transform_to_phase
from .autoscaling import autoscaling
from .ensemble_average import ensemble_average
