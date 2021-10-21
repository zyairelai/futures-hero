def apply_default(dataset):
    dataset['12_EMA'] = dataset['close'].ewm(span=12).mean()
    dataset['26_EMA'] = dataset['close'].ewm(span=26).mean()
    dataset['MACD'] = dataset['12_EMA'] - dataset['26_EMA']
    dataset['Signal'] = dataset['MACD'].ewm(span=9).mean()
    dataset['Histogram'] = dataset['MACD'] - dataset['Signal']
    dataset['long'] = dataset.apply(long_condition, axis=1)
    dataset['short'] = dataset.apply(short_condition, axis=1)
    clean = dataset.drop(['12_EMA', '26_EMA'], axis=1)
    return clean

def long_condition(dataset):
    return True if dataset['Histogram'] > 0 and dataset['MACD'] > dataset['Signal'] and dataset['Histogram'] > dataset['Signal'] else False

def short_condition(dataset):
    return True if dataset['Histogram'] < 0 and dataset['MACD'] < dataset['Signal'] and dataset['Histogram'] < dataset['Signal'] else False

# ==========================================================================================================================================================================
#                                                               TEST
# ==========================================================================================================================================================================

def test():
    import candlestick
    klines = candlestick.KLINE_INTERVAL_1HOUR(0)
    print("candlestick.KLINE_INTERVAL_1HOUR(0)")
    print(klines)
    print()

    apply_MACD = apply_default(klines)
    print("MACD.apply_default(klines)")
    print(apply_MACD)

# test()