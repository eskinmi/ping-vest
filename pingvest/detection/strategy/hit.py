import numpy as np


def price_hit_detector(prices: np.array,
                       timestamps: np.array,
                       target: float,
                       detect_higher: bool,
                       max_lookback_units: int = 10
                       ):
    data_sliced = prices[:1 * max_lookback_units]
    if detect_higher:
        passed = np.argwhere(data_sliced >= target)
    else:
        passed = np.argwhere(data_sliced <= target)
    return (
        any(passed),
        np.take(data_sliced, passed).flatten().tolist(),
        np.take(timestamps, passed).flatten().tolist()
    )
