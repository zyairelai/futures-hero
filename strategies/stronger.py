import pandas, os
import modules.MACD
import modules.candlestick
import modules.heikin_ashi

test_module = False

def futures_hero(pair):
    # Process Heikin Ashi & Apply Technical Analysis
    direction = modules.heikin_ashi.heikin_ashi(modules.candlestick.get_klines(pair, '1d'))[["timestamp", "candle"]].copy()
    support   = modules.heikin_ashi.heikin_ashi(modules.candlestick.get_klines(pair, '6h'))[["timestamp", "candle"]].copy()
    entry     = modules.candlestick.get_klines(pair, '1m')
    default, process = entry, entry

    # Backtest with FEDA json
    feda_klines = "feda_output.json"
    if os.path.isfile(feda_klines):
        feda_1min = pandas.read_json(feda_klines)
        feda_1min = feda_1min.rename({0: 'timestamp', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, axis=1)
        default, process = feda_1min, feda_1min

    dataset   = modules.candlestick.candlestick(default)
    macd1MIN  = modules.MACD.apply_default(modules.heikin_ashi.heikin_ashi(process))
    direction = direction.rename(columns={'candle': 'direction'})
    support   = support.rename(columns={'candle': 'support'})

    # Merge all the necessarily data into one Dataframe
    dataset = pandas.merge_asof(dataset, direction, on='timestamp')
    dataset = pandas.merge_asof(dataset, support, on='timestamp')
    dataset = pandas.merge_asof(dataset, macd1MIN, on='timestamp')

    # Apply Place Order Condition
    dataset["GO_LONG"] = dataset.apply(GO_LONG_CONDITION, axis=1)
    dataset["GO_SHORT"] = dataset.apply(GO_SHORT_CONDITION, axis=1)
    dataset["EXIT_LONG"] = dataset.apply(EXIT_LONG_CONDITION, axis=1)
    dataset["EXIT_SHORT"] = dataset.apply(EXIT_SHORT_CONDITION, axis=1)
    return dataset

def GO_LONG_CONDITION(dataset):
    if dataset['direction'] == "GREEN" and dataset['support'] == "GREEN" and dataset['MACD_long'] : return True
    else: return False

def GO_SHORT_CONDITION(dataset):
    if dataset['direction'] == "RED" and dataset['support'] == "RED" and dataset['MACD_short'] : return True
    else: return False

def EXIT_LONG_CONDITION(dataset):
    if dataset['MACD_short']: return True
    else : return False

def EXIT_SHORT_CONDITION(dataset):
    if dataset['MACD_long']: return True
    else : return False

if test_module:
    run = futures_hero("BTCUSDT")
    print(run)