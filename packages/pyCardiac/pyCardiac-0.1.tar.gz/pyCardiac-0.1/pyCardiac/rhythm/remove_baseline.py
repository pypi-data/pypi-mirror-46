from ..signal.processing import remove_baseline as remove_baseline_1d


def remove_baseline(data, method_name = "linear", **kwargs):
    data_detrended = remove_baseline_1d(data, method_name, **kwargs)
    return data_detrended

remove_baseline.__doc__ = remove_baseline_1d.__doc__