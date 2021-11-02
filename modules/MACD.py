test_module = False

def apply_default(dataset):
    dataset['12_EMA'] = dataset['close'].ewm(span=12).mean()
    dataset['26_EMA'] = dataset['close'].ewm(span=26).mean()
    dataset['MACD'] = dataset['12_EMA'] - dataset['26_EMA']
    dataset['Signal'] = dataset['MACD'].ewm(span=9).mean()
    dataset['Histogram'] = dataset['MACD'] - dataset['Signal']
    dataset['MACD_long'] = dataset.apply(long_condition, axis=1)
    dataset['MACD_short'] = dataset.apply(short_condition, axis=1)
    clean = dataset.drop(['open', 'high', 'low', 'close', 'volume', '12_EMA', '26_EMA', 'MACD', 'Signal', 'Histogram'], axis=1)
    return clean

def long_condition(dataset):
    if  dataset['Signal'] < 0 and \
        dataset['Signal'] < dataset['MACD'] and \
        dataset['Histogram'] > 0 : return True 
    else: return False

def short_condition(dataset):
    if  dataset['Signal'] > 0 and \
        dataset['Signal'] > dataset['MACD'] and \
        dataset['Histogram'] < 0 : return True  
    else: return False

if test_module:
    import candlestick, heikin_ashi
    klines = candlestick.KLINE_INTERVAL_1HOUR("BTCUSDT")
    heikin = heikin_ashi.heikin_ashi(klines)
    apply_MACD = apply_default(heikin)
    print("\nMACD.apply_default(heikin)")
    print(apply_MACD)