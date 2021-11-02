test_module = False

def heikin_ashi(klines):
    import pandas
    heikin_ashi_df = pandas.DataFrame(index=klines.index.values, columns=['open', 'high', 'low', 'close'])
    heikin_ashi_df['close'] = (klines['open'] + klines['high'] + klines['low'] + klines['close']) / 4

    for i in range(len(klines)):
        if i == 0: heikin_ashi_df.iat[0, 0] = klines['open'].iloc[0]
        else: heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i-1, 0] + heikin_ashi_df.iat[i-1, 3]) / 2

    heikin_ashi_df['high'] = heikin_ashi_df.loc[:, ['open', 'close']].join(klines['high']).max(axis=1)
    heikin_ashi_df['low']  = heikin_ashi_df.loc[:, ['open', 'close']].join(klines['low']).min(axis=1)
    heikin_ashi_df["color"] = heikin_ashi_df.apply(color, axis=1)
    heikin_ashi_df.insert(0,'timestamp', klines['timestamp'])

    # Use Temporary Column to Identify Strength
    heikin_ashi_df["upper"] = heikin_ashi_df.apply(upper_wick, axis=1)
    heikin_ashi_df["lower"] = heikin_ashi_df.apply(lower_wick, axis=1)
    heikin_ashi_df["body"]  = abs(heikin_ashi_df['open'] - heikin_ashi_df['close'])
    heikin_ashi_df["body_s1"] = heikin_ashi_df['body'].shift(1)
    heikin_ashi_df["body_s2"] = heikin_ashi_df['body'].shift(2)
    heikin_ashi_df["indecisive"] = heikin_ashi_df.apply(absolute_indecisive, axis=1)
    heikin_ashi_df["strong"] = heikin_ashi_df.apply(super_strong, axis=1)
    
    # Reserve Useful Column
    heikin_ashi_df["candle"] = heikin_ashi_df.apply(valid_candle, axis=1)
    heikin_ashi_df = heikin_ashi_df.drop(["indecisive", "strong", "upper", "lower", "body", "body_s1", "body_s2"], axis=1)
    return heikin_ashi_df

# ==========================================================================================================================================================================
#                                                           PANDAS CONDITIONS
# ==========================================================================================================================================================================

def color(HA):
    if   HA['open'] < HA['close']: return "GREEN"
    elif HA['open'] > HA['close']: return "RED"
    else: return "INDECISIVE"

def upper_wick(HA):
    if HA['color'] == "GREEN": return HA['high'] - HA['close']
    elif HA['color'] == "RED": return HA['high'] - HA['open']
    else: return (HA['high'] - HA['open'] + HA['high'] - HA['close']) / 2

def lower_wick(HA):
    if HA['color'] == "GREEN": return  HA['open'] - HA['low']
    elif HA['color'] == "RED": return HA['close'] - HA['low']
    else: return (HA['open'] - HA['low'] + HA['close'] - HA['low']) / 2

def super_strong(HA):
    if  HA['indecisive'] == False and \
        HA['body'] > HA['body_s1'] and \
        HA['body'] > HA['body_s2'] : return True
    else: return False

def absolute_indecisive(HA):
    if HA['body'] * 2 < HA['upper'] and HA['body'] * 2 < HA['lower'] : return True
    else: return False

def valid_candle(HA):
    if HA['strong']:
        if HA['color'] == "GREEN": return "GREEN"
        elif HA['color'] == "RED": return "RED"
    else: return "INDECISIVE"

if test_module:
    import candlestick
    klines = candlestick.KLINE_INTERVAL_1HOUR("BTCUSDT")
    processed_heikin_ashi = heikin_ashi(klines)
    print("\nheikin_ashi.heikin_ashi")
    print(processed_heikin_ashi)