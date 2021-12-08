import numpy as np
from typing import List


def ma(x, w) -> np.array:
    """
    moving averages with fill.
    :param x: np.array
    :param w: int
    """
    ma_ = (np.convolve(x, np.ones(w), 'valid') / w)
    return np.concatenate((x[:w-1], ma_))


def standardize(x) -> np.array:
    """
    standard scaling.
    :param x: np.array
    """
    return (x-x.mean()) / x.std()


def min_max_scale(x) -> np.array:
    """
    standard scaling.
    :param x: np.array
    """
    return (x-x.min()) / (x.max() - x.min())


def fod(x) -> np.array:
    """
    first order difference.
    :param x: np.array
    """
    return np.diff(x, 1)


def outliers(x, abs_limit) -> List[int]:
    """
    Find outliers
    :param x:
    """
    return list(
        np.where(np.abs(x) >= abs_limit)[0]
    )


def get_trend(x) -> np.array:
    """
    Find trend in series.
    :param x: np.array
    :return:
        np.array
    """
    return np.polyfit(np.arange(0, len(x)), x, 1)