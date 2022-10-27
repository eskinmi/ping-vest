import numpy as np
import pytest
from mock import patch

from pingvest.api import assets


@pytest.fixture
def raw_data():
    return {
        "META_DATA": "STOCK INTRADAY",
        "data": {'2022-10-26': {'1. open': '475.9500', '2. high': '496.2000', '3. low': '474.2500', '4. close': '484.0900', '5. volume': '1880258'},
                 '2022-10-25': {'1. open': '478.4900', '2. high': '495.7499', '3. low': '478.3500', '4. close': '486.0100', '5. volume': '2047240'}
                 }
    }


class PseudoAsset(assets.AssetCollector):

    def __init__(self, query):
        self.query = query
        self.series = None
        self.raw = None

        params = {
            'function': 'PSEUDO_FUNCTION',
            'symbol': self.query
        }

        super().__init__(params, 'json')

    def _process(self, raw: dict):
        """
        Process raw json.
        :return:
            np.array
        """
        key = self._get_data_key(raw)
        raw = assets.asset_data_to_numpy(raw, key)
        return raw


@patch('pingvest.api.assets.get_api_key')
@patch('pingvest.api.assets.make_get_request_to_json')
def test_asset_process(mock_request_get, mock_get_api_key, raw_data):
    mock_get_api_key.return_value = None
    mock_request_get.return_value = raw_data
    asset = PseudoAsset('ANY_SYMBOL')
    asset.get()
    assert np.array_equal(asset.data, np.array([484.0900, 486.0100]))


def test_make_asset():
    with pytest.raises(ValueError):
        assets.make_asset(asset_name='nonexistent_asset')


@patch('pingvest.api.assets.make_asset')
@patch('pingvest.api.assets.get_api_key')
@patch('pingvest.api.assets.make_get_request_to_json')
def test_asset_loader_hash_key(mock_request_get, mock_get_api_key, mock_make_asset, raw_data):
    mock_get_api_key.return_value = None
    mock_request_get.return_value = raw_data
    mock_make_asset.return_value = PseudoAsset('FAKE_SYMBOL')
    hash_key = assets.AssetLoader._hash_asset_key(
        sym='FAKE_SYMBOL',
        asset_type='fake_asset',
        fake_param='fake_parameter'
    )
    assert hash_key == 'sym:fake_symbol-asset_type:fake_asset-fake_param:fake_parameter'

    asset = assets.AssetLoader.get(
        sym='FAKE_SYMBOL',
        asset_type='fake_asset',
        fake_param='fake_parameter'
    )

    assert type(asset) == PseudoAsset
    assert np.array_equal(asset.data, np.array([484.0900, 486.0100]))

