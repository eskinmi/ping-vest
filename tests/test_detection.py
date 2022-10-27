import pytest
import datetime as dt
import numpy as np

from pingvest.detection.strategy.hit import price_hit_detector
from pingvest.detection.strategy.peakdip import peak_detector
from pingvest.detection.strategy.peakdip import dip_detector
from pingvest.detection.strategy.trend import naive_anomaly_detector
from pingvest.detection.detector import Detector


@pytest.fixture
def data():
    return np.array(
        [10.5, 10.4, 10.6, 10.7, 10.12, 11.0, 12.0, 13.0, 15.5, 14.0, 10.1]
    )


@pytest.fixture
def timestamps():
    return np.array(
        [dt.date.today() - dt.timedelta(d) for d in range(11)]
    )


def test_price_hit_detector(data, timestamps):

    # detection higher
    rb, prices, times = price_hit_detector(
        data,
        timestamps,
        target=14.0,
        detect_higher=True,
        max_lookback_units=20
    )
    req_prices, req_times = np.array([15.5, 14.0]), np.take(timestamps, np.array([8, 9]))
    assert rb
    assert np.array_equal(prices, req_prices)
    assert np.array_equal(times, req_times)

    # detection lower, with lookback units
    rb, prices, times = price_hit_detector(
        data,
        timestamps,
        target=10.5,
        detect_higher=False,
        max_lookback_units=5
    )
    req_prices, req_times = np.array([10.5, 10.4, 10.12]), np.take(timestamps, np.array([0, 1, 4]))
    assert rb
    assert np.array_equal(prices, req_prices)
    assert np.array_equal(times, req_times)


def test_peak_detector(data, timestamps):

    # detect peak normal
    rb, _, _ = peak_detector(
        data,
        timestamps,
        w=3,
        quant=0.1
    )
    assert not rb

    # detect peak array reversed
    data_reverse = np.flip(data)
    time_reverse = np.flip(timestamps)
    rb, prices, times = peak_detector(
        data_reverse,
        time_reverse,
        w=3,
        quant=0.1
    )
    req_prices, req_times = np.take(data_reverse, np.array([0, 1, 2])), np.take(time_reverse, np.array([0, 1, 2]))
    assert rb
    assert np.array_equal(prices, req_prices)
    assert np.array_equal(times, req_times)


def test_dip_detector(data, timestamps):

    # detect peak normal
    rb, prices, times = dip_detector(
        data,
        timestamps,
        w=3,
        quant=0.1
    )
    req_prices, req_times = np.take(data, np.array([0, 1, 2])), np.take(timestamps, np.array([0, 1, 2]))
    assert rb
    assert np.array_equal(prices, req_prices)
    assert np.array_equal(times, req_times)


def test_naive_anomaly_detector(data, timestamps):
    # detect outliers high limit
    rb, _, _ = naive_anomaly_detector(
        data,
        timestamps,
        abs_limit=3.0
    )
    assert not rb

    # detect outliers low limit
    rb, prices, times = naive_anomaly_detector(
        data,
        timestamps,
        abs_limit=1.5
    )
    req_prices, req_times = np.take(data, np.array([7, 9])), np.take(timestamps, np.array([7, 9]))
    assert rb
    assert np.array_equal(prices, req_prices)
    assert np.array_equal(times, req_times)


def test_detector(data, timestamps):
    detector = Detector('ASML', 'peak_detector')
    response = detector.detect(data, timestamps, w=3, quant=0.1)
    assert not response.rb
    assert not response.prices
    assert not response.timestamps
    assert response.sym == 'ASML'
    assert response.strategy == 'peak_detector'
