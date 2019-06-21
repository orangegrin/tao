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

    # 30M macd
    macd, macdsignal, macdhist = talib.MACD(
        df_ohlc['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    macd_key = "macd_30m"
    stats[macd_key] = 'mix'
    if(macdhist[-1] > 0):
        stats[macd_key] = 'up'
    if(macdhist[-1] < 0):
        stats[macd_key] = 'down'

    # 1H
    stats['1h'] = 'mix'
    df_ohlc = get_ohlc(symbol, '1h', '1H')
    MAs = get_MAs(df_ohlc, [5, 10, 30, 60])
    if MAs[0][-1] < MAs[1][-1] < MAs[2][-1] < MAs[3][-1]:
        stats['1h'] = 'down'
    if MAs[0][-1] > MAs[1][-1] > MAs[2][-1] > MAs[3][-1]:
        stats['1h'] = 'up'

    # 1h macd
    macd, macdsignal, macdhist = talib.MACD(
        df_ohlc['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    macd_key = "macd_1h"
    stats[macd_key] = 'mix'
    if(macdhist[-1] > 0):
        stats[macd_key] = 'up'
    if(macdhist[-1] < 0):
        stats[macd_key] = 'down'

    # 4H
    stats['4h'] = 'mix'
    df_ohlc = get_ohlc(symbol, '1h', '4H')
    MAs = get_MAs(df_ohlc, [5, 10, 30, 60])
    if MAs[0][-1] < MAs[1][-1] < MAs[2][-1] < MAs[3][-1]:
        stats['4h'] = 'down'
    if MAs[0][-1] > MAs[1][-1] > MAs[2][-1] > MAs[3][-1]:
        stats['4h'] = 'up'

    # 4h macd
    macd, macdsignal, macdhist = talib.MACD(
        df_ohlc['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    macd_key = "macd_4h"
    stats[macd_key] = 'mix'
    if(macdhist[-1] > 0):
        stats[macd_key] = 'up'
    if(macdhist[-1] < 0):
        stats[macd_key] = 'down'

    # 1D
    stats['1d'] = 'mix'
    df_ohlc = get_ohlc(symbol, '1d', '1D')
    MAs = get_MAs(df_ohlc, [5, 10, 30, 60])
    if MAs[0][-1] < MAs[1][-1] < MAs[2][-1] < MAs[3][-1]:
        stats['1d'] = 'down'
    if MAs[0][-1] > MAs[1][-1] > MAs[2][-1] > MAs[3][-1]:
        stats['1d'] = 'up'

    # 1d macd
    macd, macdsignal, macdhist = talib.MACD(
        df_ohlc['close'], fastperiod=12, slowperiod=26, signalperiod=9)
    macd_key = "macd_1d"
    stats[macd_key] = 'mix'
    if(macdhist[-1] > 0):
        stats[macd_key] = 'up'
    if(macdhist[-1] < 0):
        stats[macd_key] = 'down'
    return stats


last_stats_dict = {}


def save_to_redis(key, stats):
    val = json.dumps(stats)
    # if key not in last_stats_dict or last_stats_dict[key] != j:
    now = int(time.time() * 1000)
    r.hmset(key, {now: val})
    last_stats_dict[key] = val
    print('save to redis: %s' % (val))
    # else:
    #     print('no change %s' % key)


def bitmex_listen(symbol):
    stats = get_stats(symbol)
    save_to_redis('bitmex:%s' % (symbol), stats)


while True:
    try:
        bitmex_listen('BTC/USD')
        bitmex_listen('ETH/USD')
        bitmex_listen('LTCM19')
        bitmex_listen('EOSM19')
        bitmex_listen('XRPM19')
        bitmex_listen('BCHM19')
    except Exception as e:
        print(e)
    finally:
        interval = 10 * 60  # 15 minutes
        time.sleep(interval)
