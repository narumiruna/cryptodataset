import pandas as pd
import pytest

from cryptodataset import MAXData


@pytest.fixture
def max_data() -> MAXData:
    return MAXData()


def test_max_ohlcv_get_ohlcv(max_data: MAXData) -> None:
    symbol = 'BTCUSDT'
    timeframe = '1d'

    df = max_data.get_ohlcv(symbol, timeframe)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0


def test_max_ohlcv_get_ohlcv_limit(max_data: MAXData) -> None:
    symbol = 'BTCUSDT'
    timeframe = '1d'
    limit = 30

    df = max_data.get_ohlcv(symbol, timeframe, limit)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == limit
