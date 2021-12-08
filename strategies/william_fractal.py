import pandas, os
import modules.EMA
import modules.MACD
import modules.candlestick
import modules.heikin_ashi

test_module = 1

def futures_hero(pair):
    # Fetch the raw klines data
    feda_klines = "feda_output.json"
    if os.path.isfile(feda_klines):
        default = pandas.read_json(feda_klines).rename({0: 'timestamp', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, axis=1) 
    else: default = modules.candlestick.get_klines(pair, '5m')

    # Process Heikin Ashi & Apply Technical Analysis
    dataset = modules.candlestick.candlestick(default)[["timestamp", "open", "high", "low", "close"]].copy()
    modules.EMA.apply_EMA(dataset, 20)[["timestamp", "20EMA"]].copy()
    modules.EMA.apply_EMA(dataset, 50)[["timestamp", "50EMA"]].copy()

    # William Fractal Processing
    dataset["close_pivot"] = dataset['close'].shift(3)
    dataset["high_s1"] = dataset['high'].shift(1)
    dataset["high_s2"] = dataset['high'].shift(2)
    dataset["high_s3"] = dataset['high'].shift(3)
    dataset["high_s4"] = dataset['high'].shift(4)
    dataset["high_s5"] = dataset['high'].shift(5)
    dataset["low_s1"] = dataset['low'].shift(1)
    dataset["low_s2"] = dataset['low'].shift(2)
    dataset["low_s3"] = dataset['low'].shift(3)
    dataset["low_s4"] = dataset['low'].shift(4)
    dataset["low_s5"] = dataset['low'].shift(5)

    # Apply Place Order Condition
    dataset["GO_LONG"] = dataset.apply(GO_LONG_CONDITION, axis=1)
    dataset["GO_SHORT"] = dataset.apply(GO_SHORT_CONDITION, axis=1)
    dataset["EXIT_LONG"] = dataset.apply(EXIT_LONG_CONDITION, axis=1)
    dataset["EXIT_SHORT"] = dataset.apply(EXIT_SHORT_CONDITION, axis=1)
    return dataset

def GO_LONG_CONDITION(dataset):
    if  dataset['high_s3'] > dataset['high_s1'] and \
        dataset['high_s3'] > dataset['high_s2'] and \
        dataset['high_s3'] > dataset['high_s4'] and \
        dataset['high_s3'] > dataset['high_s5'] and \
        dataset['close_pivot'] < dataset['20EMA'] and \
        dataset['close_pivot'] > dataset['50EMA'] and \
        dataset['20EMA'] > dataset['50EMA'] : return True
    else: return False

def GO_SHORT_CONDITION(dataset):
    if  dataset['low_s3'] < dataset['low_s1'] and \
        dataset['low_s3'] < dataset['low_s2'] and \
        dataset['low_s3'] < dataset['low_s4'] and \
        dataset['low_s3'] < dataset['low_s5'] and \
        dataset['close_pivot'] > dataset['20EMA'] and \
        dataset['close_pivot'] < dataset['50EMA'] and \
        dataset['20EMA'] < dataset['50EMA'] : return True
    else: return False

def EXIT_LONG_CONDITION(dataset):
    if dataset['low'] < dataset['50EMA']: return True
    else : return False

def EXIT_SHORT_CONDITION(dataset):
    if dataset['high'] > dataset['50EMA']: return True
    else : return False

if test_module:
    run = futures_hero("BTCUSDT")
    print(run)