from pingvest.utils import stats
from pingvest.assets import AssetCollector
from typing import List


def make(strategy, **kwargs):
    if strategy == 'naive':
        return NaiveDetector(**kwargs)
    else:
        raise ValueError('strategy should be one of the following; naive')


class NaiveDetector:

    def __init__(self, abs_limit=3):
        self.limit = abs_limit

    def detect(self, collector: AssetCollector) -> List[int]:
        # collect data
        collector.get()
        # process
        collector.process()
        # standardize fod
        arr = stats.standardize(
            stats.fod(
                collector.raw
            )
        )
        # find outliers
        return stats.outliers(arr, self.limit)