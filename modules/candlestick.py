import ccxt
import pandas

test_module = False

query = 1000
ccxt_client = ccxt.binance()
tohlcv_colume = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
def KLINE_INTERVAL_1MIN(pair) : return pandas.DataFrame(ccxt_client.fetch_ohlcv(pair, '1m', limit=query), columns=tohlcv_colume)
def KLINE_INTERVAL_5MIN(pair) : return pandas.DataFrame(ccxt_client.fetch_ohlcv(pair, '5m', limit=query), columns=tohlcv_colume)
def KLINE_INTERVAL_30MIN(pair): return pandas.DataFrame(ccxt_client.fetch_ohlcv(pair, '30m',limit=query), columns=tohlcv_colume)
def KLINE_INTERVAL_1HOUR(pair): return pandas.DataFrame(ccxt_client.fetch_ohlcv(pair, '1h', limit=query), columns=tohlcv_colume)
def KLINE_INTERVAL_6HOUR(pair): return pandas.DataFrame(ccxt_client.fetch_ohlcv(pair, '6h', limit=query), columns=tohlcv_colume)

def candlestick(klines):
    candlestick_df = klines # make a new DataFrame called candlestick_df

    # Temporary previous column
    candlestick_df["high_s1"] = klines['high'].shift(1)
    candlestick_df["high_s2"] = klines['high'].shift(2)
    candlestick_df["low_s1"]  = klines['low'].shift(1)
    candlestick_df["low_s2"]  = klines['low'].shift(2)

    # Compute candlestick details
    candlestick_df["color"]  = candlestick_df.apply(candle_color, axis=1)
    candlestick_df["upper"]  = candlestick_df.apply(upper_wick, axis=1)
    candlestick_df["lower"]  = candlestick_df.apply(lower_wick, axis=1)
    candlestick_df["body"]   = abs(candlestick_df['open'] - candlestick_df['close'])
    candlestick_df["strong"] = candlestick_df.apply(strong_candle, axis=1)

    # Drop Temporarily Column
    dataset = candlestick_df.drop(["volume", "upper", "lower", "body", "high_s1", "low_s1", "low_s2", "high_s2"], axis=1)
    return dataset

# ==========================================================================================================================================================================
#                                                           PANDAS CONDITIONS
# ==========================================================================================================================================================================

def candle_color(candle):
    if candle['close'] > candle['open']: return "GREEN"
    elif candle['close'] < candle['open']: return "RED"
    else: return "INDECISIVE"

def upper_wick(candle):
    if candle['color'] == "GREEN": return candle['high'] - candle['close']
    elif candle['color'] == "RED": return candle['high'] - candle['open']
    else: return (candle['high'] - candle['open'] + candle['high'] - candle['close']) / 2

def lower_wick(candle):
    if candle['color'] == "GREEN": return candle['open'] - candle['low']
    elif candle['color'] == "RED": return candle['close'] - candle['low']
    else: return (candle['open'] - candle['low'] + candle['close'] - candle['low']) / 2

def strong_candle(candle):
    if candle["color"] == "GREEN": return True if candle['close'] > candle['high_s1'] and candle['close'] > candle['high_s2'] else False
    elif candle["color"] == "RED": return True if candle['close'] < candle['low_s1'] and candle['close'] < candle['low_s2'] else False
    else: return False

if test_module:
    klines = KLINE_INTERVAL_1HOUR("BTCUSDT")
    processed_candle = candlestick(klines)
    print("\ncandlestick.candlestick(klines)")
    print(processed_candle)