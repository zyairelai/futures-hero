import config, ccxt, pandas
from termcolor import colored
ccxt_client = ccxt.binance()

query = 55
tohlcv_colume = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
def KLINE_INTERVAL_1MIN(i) : return pandas.DataFrame(ccxt_client.fetch_ohlcv(config.pair[i], '1m', limit=query), columns=tohlcv_colume)
def KLINE_INTERVAL_5MIN(i) : return pandas.DataFrame(ccxt_client.fetch_ohlcv(config.pair[i], '5m', limit=query), columns=tohlcv_colume)
def KLINE_INTERVAL_30MIN(i): return pandas.DataFrame(ccxt_client.fetch_ohlcv(config.pair[i], '30m',limit=query), columns=tohlcv_colume)
def KLINE_INTERVAL_1HOUR(i): return pandas.DataFrame(ccxt_client.fetch_ohlcv(config.pair[i], '1h', limit=query), columns=tohlcv_colume)
def KLINE_INTERVAL_6HOUR(i): return pandas.DataFrame(ccxt_client.fetch_ohlcv(config.pair[i], '6h', limit=query), columns=tohlcv_colume)

def candlestick(klines):
    candlestick_df = klines # make a new DataFrame called candlestick_df

    # Temporary previous column
    candlestick_df["pre_high"]     = klines['high'].shift(1)
    candlestick_df["pre_low"]      = klines['low'].shift(1)
    candlestick_df["pre_pre_low"]  = klines['low'].shift(2)
    candlestick_df["pre_pre_high"] = klines['high'].shift(2)

    # Compute candlestick details
    candlestick_df["color"]  = candlestick_df.apply(candle_color, axis=1)
    candlestick_df["upper"]  = candlestick_df.apply(upper_wick, axis=1)
    candlestick_df["lower"]  = candlestick_df.apply(lower_wick, axis=1)
    candlestick_df["body"]   = abs(candlestick_df['open'] - candlestick_df['close'])
    candlestick_df["strong"] = candlestick_df.apply(strong_candle, axis=1)

    # Drop Previous Column
    dataset = candlestick_df.drop(["pre_high", "pre_low", "pre_pre_low", "pre_pre_high"], axis=1)
    return dataset

def output(candlestick):
    milliseconds = int(candlestick['timestamp'].iloc[1]) - int(candlestick['timestamp'].iloc[0])
    if milliseconds == 1 * 60000: interval = "1 MINUTE  "
    elif milliseconds == 3 * 60000: interval = "3 MINUTE  "
    elif milliseconds == 5 * 60000: interval = "5 MINUTE  "
    elif milliseconds == 15 * 60000: interval = "15 MINUTE "
    elif milliseconds == 30 * 60000: interval = "30 MINUTE "
    elif milliseconds == 1 * 60 * 60000: interval = "1 HOUR    "
    elif milliseconds == 2 * 60 * 60000: interval = "2 HOUR    "
    elif milliseconds == 4 * 60 * 60000: interval = "4 HOUR    "
    elif milliseconds == 6 * 60 * 60000: interval = "6 HOUR    "
    elif milliseconds == 12 * 60 * 60000: interval = "12 HOUR   "

    strength = "STRONG " if candlestick["strong"].iloc[-1] else "WEAK "
    if   candlestick['color'].iloc[-1] == "GREEN": print(colored("CANDLE " + interval + ":   " + strength + str(candlestick['color'].iloc[-1]), "green"))
    elif candlestick['color'].iloc[-1] == "RED"  : print(colored("CANDLE " + interval + ":   " + strength + str(candlestick['color'].iloc[-1]), "red"))
    else: print(colored("CANDLE " + interval + ":   " + str(candlestick['color'].iloc[-1]), "yellow"))

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
    if candle["color"] == "GREEN": return True if candle['close'] > candle['pre_high'] and candle['close'] > candle['pre_pre_high'] else False
    elif candle["color"] == "RED": return True if candle['close'] < candle['pre_low'] and candle['close'] < candle['pre_pre_low'] else False
    else: return False

# ==========================================================================================================================================================================
#                                                               TEST
# ==========================================================================================================================================================================

def test():
    klines = KLINE_INTERVAL_1HOUR(0)
    print("candlestick.KLINE_INTERVAL_1HOUR(0)")
    print(klines)
    print()

    processed_candle = candlestick(klines)
    print("candlestick.candlestick(klines)")
    print(processed_candle)
    print()

# test()