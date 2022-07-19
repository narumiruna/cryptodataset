import ccxt
import pandas as pd
from loguru import logger


def to_milliseconds(timeframe: str) -> int:
    return {'1m': 1000 * 60, '1h': 1000 * 60 * 60, '1d': 1000 * 60 * 60 * 24}[timeframe]


def fetch_all_ohlcv(exchange: ccxt.Exchange, symbol: str, timeframe: str) -> pd.DataFrame:
    logger.info('fetching {} ohlcv form {} with timeframe {}', symbol, exchange.name, timeframe)

    since = None
    limit = None

    all_ohlcv = []
    while True:
        ohlcv = exchange.fetch_ohlcv(symbol=symbol, timeframe=timeframe, since=since)
        ohlcv.sort(key=lambda k: k[0])

        if limit is None:
            limit = len(ohlcv)

        if all_ohlcv and ohlcv[0][0] == all_ohlcv[0][0]:
            break

        all_ohlcv = ohlcv + all_ohlcv

        # a small amount of overlap to make sure the final data is continuous
        since = ohlcv[0][0] - to_milliseconds(timeframe) * (limit - 1)

    df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df = df.drop_duplicates('timestamp')
    df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')

    return df
