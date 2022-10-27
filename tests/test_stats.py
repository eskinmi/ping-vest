import pytest
import numpy as np

from pingvest.detection import stats


@pytest.fixture
def x():
    return np.linspace(10, 20, 3)


@pytest.fixture
def x_standardized():
    return np.array([-3.5, -2, -1, 0, 1, 2, 3.5])


def test_ma(x):
    res = stats.ma(x, 2)
    req = np.array([10.0, 12.5, 17.5])
    assert np.array_equal(res, req)


def test_standardize(x):
    pass


def test_min_max_scale(x):
    res = stats.min_max_scale(x)
    req = np.array([0.0, 0.5, 1.0])
    assert np.array_equal(res, req)


def test_fod(x):
    res = stats.fod(x)
    req = np.array([5.0, 5.0])
    assert np.array_equal(res, req)


def test_outliers(x_standardized):
    res = stats.ix_outliers(x_standardized, abs_limit=3.0)
    req = np.array([0, 6])
    assert np.array_equal(np.array(res), req)


def test_trend(x):
    res = stats.trend(x)
    req = np.array([5.0, 10.0])
    assert np.allclose(res, req)
