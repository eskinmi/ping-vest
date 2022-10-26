import numpy as np
from typing import List, Union


def ma(x, w) -> np.array:
    """ calculate moving averages """
    ma_ = (np.convolve(x, np.ones(w), 'valid') / w)
    return np.concatenate((x[:w-1], ma_))


def standardize(x) -> np.array:
    """ standardise """
    return (x-x.mean()) / x.std()


def min_max_scale(x) -> np.array:
    """ min max scaling """
    return (x-x.min()) / (x.max() - x.min())


def fod(x) -> np.array:
    """ first order differencing """
    return np.diff(x, 1)


def outliers(x: np.array, abs_limit: Union[float, int]) -> List[int]:
    """ detect outliers """
    return list(
        np.where(np.abs(x) >= abs_limit)[0]
    )


def trend(x) -> np.array:
    """ find linear trend with polyfit """
    return np.polyfit(np.arange(0, len(x)), x, 1)
