import os
import pytest

from src.data_grab import DataGrab
from src.arb_finder import ArbFinder


@pytest.fixture
def data_grab():
    return DataGrab(os.getenv('API_KEY'), sport='basketball_nba', mkt='h2h')

@pytest.fixture
def arb_find():
    return ArbFinder()


def test_data_grab(data_grab):
    re = data_grab.request_odds()
    assert re.status_code == 200, 'Fail: non-200 response'

def test_data_construction(data_grab):
    data = data_grab.data_construction()
    assert data.shape[0] > 0, 'Fail: empty dataframe'


def test_best_odds(arb_find):
    odds_data = arb_find.best_odds()
    assert odds_data.shape[0] > 0, 'Fail: empty dataframe'

def test_redis_loader(arb_find):
    response = arb_find.redis_loader()
    assert response == 'Success', 'Fail: data not loaded to redis'

