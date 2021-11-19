import ccxt
import pandas

query = 1000
ccxt_client = ccxt.binance()
tohlcv_colume = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
def get_klines(pair, interval):
    return pandas.DataFrame(ccxt_client.fetch_ohlcv(pair, interval , limit=query), columns=tohlcv_colume)

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
    candlestick_df["volumeAvg"] = sum(klines["volume"]) / query / 3

    clean = candlestick_df[["timestamp", "open", "high", "low", "close", "volume", "volumeAvg", "color", "strong"]].copy()
    return clean

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

def test_module():
    klines = get_klines("BTCUSDT", "1h")
    processed_candle = candlestick(klines)
    print("\ncandlestick.candlestick(klines)")
    print(processed_candle)

# test_module()