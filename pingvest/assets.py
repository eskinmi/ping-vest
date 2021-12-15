from .utils.helpers import *
import numpy as np
from typing import Dict, Tuple
import datetime as dt
import csv
import pandas as pd


class AssetCollector:

    def __init__(self, params: Dict[str, str], parse_type='json'):
        self.api_key = get_api_key()
        self.save_loc = './data.json'
        self.api_path = 'https://www.alphavantage.co/query?'
        self.parse_type = parse_type
        self.params = {**params, 'apikey': self.api_key}
        self.data = None

    @property
    def parse_type(self):
        return self._parse_type

    @parse_type.setter
    def parse_type(self, value):
        can_be = ['json', 'csv']
        if value in can_be:
            self._parse_type = value
        else:
            raise ValueError(F'parse type can be one of the following : {can_be}')

    def get(self):
        if self.parse_type == 'json':
            self.data = make_request_to_json(self.api_path, self.params)
        elif self.parse_type == 'csv':
            self.data = make_request_to_csv(self.api_path, self.params)
        else:
            pass

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

        super().__init__(params, 'json')

    def process(self) -> np.array:
        """
        Process raw json.
        :return:
            np.array
        """
        self.raw = _data_to_numpy(self.data, self.data_key)
        return self.raw


class StockExchangeExtended(AssetCollector):
    """
    Collect stock exchange equity prices.
    Example usage:
         exc = StockExchange('IBM', '15min')
         exc.get()
         series = exc.process()
    """

    def __init__(self, query, interval, for_slice):
        self.query = query
        self.interval = interval
        self.slice = for_slice
        self.series = None
        self.raw = None

        params = {
            'function': 'TIME_SERIES_INTRADAY_EXTENDED',
            'symbol': self.query,
            'interval': self.interval,
            'slice': self.slice
        }

        super().__init__(params, 'csv')

    def process(self) -> np.array:
        """
        Process raw json.
        :return:
            np.array
        """
        cr = csv.reader(self.data.splitlines(), delimiter=',')
        arr = list(cr)
        df = pd.DataFrame(arr)
        headers = df.iloc[0]
        df = df[1:]
        df.columns = headers
        df_open = df[['time', 'close']]
        self.series = df_open
        return df_open


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

        super().__init__(params, 'json')

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