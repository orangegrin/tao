import os
import sys
import time
import ccxt
import pandas as pd
import talib
import redis
import json

exchange = ccxt.bitmex()
r = redis.Redis(host='localhost', port=6379, db=0)


def get_ohlc(symbol, timeframe, resampleTimeframe):
    limit = 750
    params = {'reverse': True}
    # since = exchange.milliseconds() - limit * 60 * 1000
    since = None
    candles = exchange.fetch_ohlcv(symbol, timeframe, since, limit, params)
    df = pd.DataFrame(candles)
    df.columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    df.index = pd.to_datetime(df['timestamp'], unit='ms')
    df2 = df.resample(resampleTimeframe).agg(
        {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'})
    return df2


def get_MAs(df_ohlc, timeperiods):
    MAs = []
    for timeperiod in timeperiods:
        MAs.append(talib.MA(df_ohlc['close'], timeperiod=timeperiod, matype=0))
    return MAs


def get_stats(symbol):
    df_ohlc = get_ohlc(symbol, '5m', '30Min')
    stats = {'symbol': symbol}
    # 30M
    stats['30m'] = 'mix'
    MAs = get_MAs(df_ohlc, [5, 10, 30, 60])
    if MAs[0][-1] < MAs[1][-1] < MAs[2][-1] < MAs[3][-1]:
        stats['30m'] = 'down'
    if MAs[0][-1] > MAs[1][-1] > MAs[2][-1] > MAs[3][-1]:
        stats['30m'] = 'up'
    # 1H
    stats['1h'] = 'mix'
    df_ohlc = get_ohlc(symbol, '1h', '1H')
    MAs = get_MAs(df_ohlc, [5, 10, 30, 60])
    if MAs[0][-1] < MAs[1][-1] < MAs[2][-1] < MAs[3][-1]:
        stats['1h'] = 'down'
    if MAs[0][-1] > MAs[1][-1] > MAs[2][-1] > MAs[3][-1]:
        stats['1h'] = 'up'
    # 4H
    stats['4h'] = 'mix'
    df_ohlc = get_ohlc(symbol, '1h', '4H')
    MAs = get_MAs(df_ohlc, [5, 10, 30, 60])
    if MAs[0][-1] < MAs[1][-1] < MAs[2][-1] < MAs[3][-1]:
        stats['4h'] = 'down'
    if MAs[0][-1] > MAs[1][-1] > MAs[2][-1] > MAs[3][-1]:
        stats['4h'] = 'up'
    # 1D
    stats['1d'] = 'mix'
    df_ohlc = get_ohlc(symbol, '1d', '1D')
    MAs = get_MAs(df_ohlc, [5, 10, 30, 60])
    if MAs[0][-1] < MAs[1][-1] < MAs[2][-1] < MAs[3][-1]:
        stats['1d'] = 'down'
    if MAs[0][-1] > MAs[1][-1] > MAs[2][-1] > MAs[3][-1]:
        stats['1d'] = 'up'
    print(stats)
    return stats


last_stats_dict = {}


def save_to_redis(key, stats):
    j = json.dumps(stats)
    # if key not in last_stats_dict or last_stats_dict[key] != j:
    now = int(time.time() * 1000)
    r.hmset(key, {now: j})
    last_stats_dict[key] = j
    print('save changes')
    # else:
    #     print('no change %s' % key)


while True:
    try:
        # BTC/USD
        stats = get_stats('BTC/USD')
        save_to_redis('bitmex:BTC/USD', stats)
        # BCHZ18
        stats = get_stats('BCHZ18')
        save_to_redis('bitmex:BCHZ18', stats)
    except Exception as e:
        print(e)
    finally:
        interval = 10 * 60  # 15 minutes
        time.sleep(interval)
