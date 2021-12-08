from pingvest.pipe import *
from pingvest.utils import stats


class NaiveDetector:

    def __init__(self, abs_limit=3):
        self.limit = abs_limit

    def detect(self, collector):
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


def get_asset(asset, query, interval):
    if asset == 'stock':
        return StockExchange(query=query, interval=interval)
    elif asset == 'forex':
        return ForeignExchange(query=query, interval=interval)
    else:
        raise ValueError('asset should be one of the following; stock, forex')


def get_detector(strategy):
    if strategy=='naive':
        return NaiveDetector(abs_limit=3)
    else:
        raise ValueError('strategy should be one of the following; naive')


def detect(asset, strategy, query, interval='30min'):
    det = get_detector(strategy)
    asset = get_asset(asset, query, interval)
    alerts = det.detect(asset)
    if alerts:
        notify(
            title=F"Stock Exchange Alert! {query}",
            text=F"high fluctuations in value at : {' '.join(str(exc.keys[i]) for i in alerts)}"
        )
