import numpy as np
from typing import Union

from pingvest.detection import stats


def naive_anomaly_detector(data: np.array,
                           timestamps: np.array,
                           abs_limit: Union[float, int]
                           ):
    data_stand = stats.standardize(
        stats.fod(data)
    )
    # find outliers
    outliers = stats.outliers(data_stand, abs_limit)
    return (
        any(outliers),
        np.take(data, outliers).tolist(),
        np.take(timestamps, outliers).tolist()
    )
