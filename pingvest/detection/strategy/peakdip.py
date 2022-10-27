import numpy as np

from pingvest.detection import stats


def dip_detector(data: np.array,
                 timestamps: np.array,
                 w: int = 3,
                 quant: float = 0.05
                 ):
    data_ma = stats.ma(data, w)
    data_scaled = stats.min_max_scale(data_ma)
    if any(data_scaled[:3] <= quant):
        return (
            True,
            data[:w].tolist(),
            timestamps[:w].tolist()
        )
    else:
        return False, [], []


def peak_detector(data: np.array,
                  timestamps: np.array,
                  w: int = 3,
                  quant: float = 0.05
                  ):
    data_ma = stats.ma(data, w)
    data_scaled = stats.min_max_scale(data_ma)
    if any(data_scaled[:w] >= 1 - quant):
        return (
            True,
            data[:w].tolist(),
            timestamps[:w].tolist()
        )
    else:
        return False, [], []


def post_peak_drop_detector(data: np.array, w: int = 3, quant: float = 0.05):
    raise NotImplementedError


def post_dip_spike_detector(data: np.array, w: int = 3, quant: float = 0.05):
    raise NotImplementedError
