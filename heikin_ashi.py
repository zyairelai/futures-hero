import pandas as pd
from termcolor import colored

def heikin_ashi(klines):
    heikin_ashi_df = pd.DataFrame(index=klines.index.values, columns=['open', 'high', 'low', 'close'])
    heikin_ashi_df['close'] = (klines['open'] + klines['high'] + klines['low'] + klines['close']) / 4

    for i in range(len(klines)):
        if i == 0: heikin_ashi_df.iat[0, 0] = klines['open'].iloc[0]
        else: heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i-1, 0] + heikin_ashi_df.iat[i-1, 3]) / 2

    heikin_ashi_df['high'] = heikin_ashi_df.loc[:, ['open', 'close']].join(klines['high']).max(axis=1)
    heikin_ashi_df['low'] = heikin_ashi_df.loc[:, ['open', 'close']].join(klines['low']).min(axis=1)

    # heikin_ashi_df['volume'] = klines['volume']
    heikin_ashi_df.insert(0,'timestamp', klines['timestamp'])
    heikin_ashi_df["candle_type"] = heikin_ashi_df.apply(candle_type, axis=1)
    heikin_ashi_df["color"]       = heikin_ashi_df.apply(color, axis=1)
    heikin_ashi_df["upper_wick"]  = heikin_ashi_df.apply(upper_wick, axis=1)
    heikin_ashi_df["lower_wick"]  = heikin_ashi_df.apply(lower_wick, axis=1)
    heikin_ashi_df["body_size"]   = abs(heikin_ashi_df['open'] - heikin_ashi_df['close'])
    heikin_ashi_df["pre_body"]    = heikin_ashi_df['body_size'].shift(1)
    heikin_ashi_df["indecisive"]  = heikin_ashi_df.apply(absolute_indecisive, axis=1)
    heikin_ashi_df["strong"]      = heikin_ashi_df.apply(super_strong, axis=1)
    heikin_ashi_df["VALID"]       = heikin_ashi_df.apply(valid_candle, axis=1)
    heikin_ashi_df = heikin_ashi_df.drop("pre_body", axis=1)

    return heikin_ashi_df

def output(HA):
    milliseconds = HA['timestamp'].iloc[-1] - HA['timestamp'].iloc[-2]
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

    current = HA['candle_type'].iloc[-1]
    if   current == "GREEN" or current == "GREEN_INDECISIVE": print(colored("HEIKIN " + interval + ":   " + current, "green"))
    elif current == "RED"   or current == "RED_INDECISIVE"  : print(colored("HEIKIN " + interval + ":   " + current, "red"))
    else: print(colored("RECENT " + interval + ":   " + current, "yellow"))

# ==========================================================================================================================================================================
#                                                           PANDAS CONDITIONS
# ==========================================================================================================================================================================

def candle_type(HA):
    if   (HA['open'] == HA['high']): return "RED"
    elif (HA['open'] == HA['low']) : return "GREEN"
    elif (HA['open'] > HA['close']): return "RED_INDECISIVE"
    elif (HA['open'] < HA['close']): return "GREEN_INDECISIVE"
    else: return "NO_MOVEMENT"

def color(HA):
    if HA['candle_type'] == "GREEN" or HA['candle_type'] == "GREEN_INDECISIVE": return "GREEN"
    if HA['candle_type'] == "RED"   or HA['candle_type'] == "RED_INDECISIVE"  : return "RED"
    else: return "INDECISIVE"

def upper_wick(HA):
    if HA['color'] == "GREEN": return HA['high'] - HA['close']
    elif HA['color'] == "RED": return HA['high'] - HA['open']
    else: return (HA['high'] - HA['open'] + HA['high'] - HA['close']) / 2

def lower_wick(HA):
    if HA['color'] == "GREEN": return HA['open'] - HA['low']
    elif HA['color'] == "RED": return HA['close'] - HA['low']
    else: return (HA['open'] - HA['low'] + HA['close'] - HA['low']) / 2

def super_strong(HA): return True if HA['indecisive'] == False and HA['body_size'] > HA['pre_body'] else False
def absolute_indecisive(HA): return True if HA['body_size'] * 2 < HA['upper_wick'] and HA['body_size'] * 2 < HA['lower_wick'] else False

def valid_candle(HA):
    if HA['strong']:
        if HA['color'] == "GREEN": return "GREEN"
        elif HA['color'] == "RED": return "RED"
    else: return "INDECISIVE"

# ==========================================================================================================================================================================
#                                                               TEST
# ==========================================================================================================================================================================

def test():
    import candlestick
    klines = candlestick.KLINE_INTERVAL_1HOUR(0)
    print("candlestick.KLINE_INTERVAL_1HOUR(0)")
    print(klines)
    print()

    processed_heikin_ashi = heikin_ashi(klines)
    print("heikin_ashi.heikin_ashi")
    print(processed_heikin_ashi)

# test()