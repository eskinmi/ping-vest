from .utils.helpers import *
import numpy as np
from typing import Dict, Tuple
import datetime as dt


class AssetCollector:

    def __init__(self, params: Dict[str, str]):
        self.api_key = get_api_key()
        self.save_loc = './data.json'
        self.api_path = 'https://www.alphavantage.co/query?'
        self.params = {**params, 'apikey': self.api_key}
        self.data = None

    def get(self):
        self.data = make_request(self.api_path, self.params)

    @property
    def data_key(self):
        if self.data:
            return list(self.data.keys())[1]
        else:
            return None

    @property
    def keys(self):
        if self.data:
            return [dt.datetime.strptime(i, '%Y-%m-%d %H:%M:%S') for i in self.data[self.data_key].keys()]

    def save(self, data=None):
        if data is None:
            data = self.data
        with open(self.save_loc, 'w') as f:
            json.dump(data, f)


class StockExchange(AssetCollector):
    """
    Collect stock exchange equity prices.
    Example usage:
         exc = StockExchange('IBM', '15min')
         exc.get()
         series = exc.process()
    """

    def __init__(self, query, interval):
        self.query = query
        self.interval = interval
        self.series = None
        self.raw = None

        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': self.query,
            'interval': self.interval
        }

        super().__init__(params)

    def process(self) -> np.array:
        """
        Process raw json.
        :return:
            np.array
        """
        self.raw = _data_to_numpy(self.data, self.data_key)
        return self.raw


class ForeignExchange(AssetCollector):
    """
    Foreign exchange equity prices.
    Example usage:
         exc = ForeignExchange('EUR-TRY', '15min')
         exc.get()
         series = exc.process()
    """

    def __init__(self, query, interval):
        self.query = query
        self.curs = self._query_to_curs(self.query)
        self.interval = interval
        self.series = None
        self.raw = None

        params = {
            'function': 'FX_INTRADAY',
            'from_symbol': self.curs[0],
            'to_symbol': self.curs[1],
            'interval': self.interval
        }

        super().__init__(params)

    @staticmethod
    def _query_to_curs(query:str) -> Tuple[str]:
        """
        Query is a string object that contains
        from currency and to currency with dash
        separation.
        Example : EUR-TRY
        :param query: str
        :return:
            Tuple[str, str]
        """
        return tuple(i.strip() for i in query.split('-'))

    def process(self) -> np.array:
        """
        Process raw json.
        :return:
            np.array
        """
        self.raw = _data_to_numpy(self.data, self.data_key)
        return self.raw


def interval_str_to_int(interval):
    return int(interval.replace('min', ''))


def _data_to_numpy(data, key):
    return np.array(
        [v.get('4. close', 0) for k, v in data[key].items()],
        dtype=np.float64
    )


def make(asset, query, interval):
    if asset == 'stock':
        return StockExchange(query=query, interval=interval)
    elif asset == 'forex':
        return ForeignExchange(query=query, interval=interval)
    else:
        raise ValueError('asset should be one of the following; stock, forex')