from abc import ABC, abstractmethod
import dateutil.parser
import csv
import time
import numpy as np
import pandas as pd
from typing import Dict, Tuple
import json
import logging

from pingvest.utils import get_api_key
from pingvest.utils import make_get_request_to_csv
from pingvest.utils import make_get_request_to_json


logger = logging.getLogger('app.assets')


class AssetCollectionException(Exception):
    def __init__(self, message=None):
        if message:
            self.message = message
        else:
            self.message = "Asset Collection Failure."
        super().__init__(self.message)


class AssetCollector(ABC):

    def __init__(self, params: Dict[str, str], parse_type='json'):
        self.api_key = get_api_key()
        self.save_loc = './data.json'
        self.api_path = 'https://www.alphavantage.co/query?'
        self.parse_type = parse_type
        self.params = {**params, 'apikey': self.api_key}
        self.raw_data = None
        self.raw_key = None
        self.data = None
        self.data_keys = None

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

    @abstractmethod
    def _process(self, *args, **kwargs):
        pass

    def get(self):
        if self.parse_type == 'json':
            raw_data = make_get_request_to_json(
                self.api_path,
                self.params
            )
        elif self.parse_type == 'csv':
            raw_data = make_get_request_to_csv(
                self.api_path,
                self.params
            )
        else:
            raise ValueError(F'parse type {self.parse_type} is invalid.')
        self.raw_data = raw_data
        self.raw_key = self._get_data_key(raw_data)
        self.data_keys = self._process_keys()
        self.data = self._process(raw_data)
        return self.data

    def _process_keys(self):
        logger.debug('processing date keys in data.')
        return np.array([dateutil.parser.parse(i) for i in self.raw_data[self.raw_key].keys()])

    @staticmethod
    def _get_data_key(raw: dict):
        if keys := list(raw.keys()):
            logger.debug(F'data keys: {keys}')
            if len(keys) > 1:
                return keys[1]
            else:
                logger.error(raw[keys[0]])
                raise AssetCollectionException(
                    """
                    asset collection failed!
                    info: {raw[keys[0]]}
                    """
                )
        else:
            logger.error('keys do not exists in data.')

    def write(self):
        with open(self.save_loc, 'w') as f:
            json.dump(self.data, f)


class StockExchangeIntraDay(AssetCollector):
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

    def _process(self, raw: dict) -> np.array:
        """
        Process raw json.
        :return:
            np.array
        """
        key = self._get_data_key(raw)
        raw = asset_data_to_numpy(raw, key)
        return raw


class StockExchangeDaily(AssetCollector):
    """
    Collect stock exchange equity prices.
    Example usage:
         exc = StockExchange('IBM', '15min')
         exc.get()
         series = exc.process()
    """

    def __init__(self, query):
        self.query = query
        self.series = None
        self.raw = None

        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': self.query
        }

        super().__init__(params, 'json')

    def _process(self, raw: dict) -> np.array:
        """
        Process raw json.
        :return:
            np.array
        """
        key = self._get_data_key(raw)
        raw = asset_data_to_numpy(raw, key)
        return raw


class StockExchangeIntraDayExtended(AssetCollector):
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

    def _process(self, raw: dict) -> np.array:
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


class ForeignExchangeIntraDay(AssetCollector):
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
    def _query_to_curs(query: str) -> Tuple[str]:
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

    def _process(self, raw: dict) -> np.array:
        """
        Process raw json.
        :return:
            np.array
        """
        key = self._get_data_key(raw)
        raw = asset_data_to_numpy(raw, key)
        return raw


def interval_str_to_int(interval):
    return int(interval.replace('min', ''))


def asset_data_to_numpy(data, key):
    logger.debug('processing raw data to numpy array.')
    return np.array(
        [v.get('4. close', 0) for k, v in data[key].items()],
        dtype=np.float64
    )


def make_asset(asset_name, **asset_params):
    valid_names = ['stock-intraday', 'forex-intraday', 'stock-daily']
    if asset_name not in valid_names:
        raise ValueError(F'asset should be one of the following; {valid_names}')
    else:
        if asset_name == 'stock-intraday':
            return StockExchangeIntraDay(**asset_params)
        if asset_name == 'forex-intraday':
            return ForeignExchangeIntraDay(**asset_params)
        if asset_name == 'stock-daily':
            return StockExchangeDaily(**asset_params)


class AssetLoader:
    assets = {}

    @staticmethod
    def _hash_asset_key(sym, asset_type, **kwargs):
        return '-'.join(
            F'{k.lower()}:{v.lower()}' for k, v in {'sym': sym, 'asset_type': asset_type, **kwargs}.items()
        )

    @staticmethod
    def _get_with_reties(asset):
        for attempt in range(3):
            try:
                asset.get()
            except AssetCollectionException as e:
                logger.error(f'attempt {attempt} : {e.message}')
                time.sleep(60)
            else:
                break
        else:
            raise AssetCollectionException('failed after 3 attempts. check logs!')
        return asset

    @classmethod
    def get(cls, sym, asset_type, **kwargs):
        key = cls._hash_asset_key(sym, asset_type, **kwargs)
        logger.debug(F'asset hash key: {key}')
        if key not in cls.assets:
            logger.debug('creating new asset with')
            logger.debug(F'asset type: {asset_type}, query: {sym}')
            asset = make_asset(asset_type, query=sym, **kwargs)
            asset = cls._get_with_reties(asset)
            cls.assets[key] = asset
            return asset
        else:
            logger.debug('asset is already loaded. returning the loaded asset.')
            return cls.assets[key]
