import pandas, os
import modules.EMA
import modules.MACD
import modules.candlestick
import modules.heikin_ashi

test_module = False

def futures_hero(pair):
    # Fetch the raw klines data
    main_raw = modules.candlestick.get_klines(pair, '6h')
    rSupport = modules.candlestick.get_klines(pair, '1h')
    entry    = modules.candlestick.get_klines(pair, '1m')

    # Backtest with FEDA json
    feda_klines = "feda_output.json"
    if os.path.isfile(feda_klines):
        default = pandas.read_json(feda_klines).rename({0: 'timestamp', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, axis=1) 
    else: default = entry

    # Process Heikin Ashi & Apply Technical Analysis
    dataset   = modules.candlestick.candlestick(default)[["timestamp", "open", "high", "low", "close"]].copy()
    volume    = modules.candlestick.candlestick(main_raw)[["timestamp", "volume", "volumeAvg"]].copy()
    direction = modules.heikin_ashi.heikin_ashi(main_raw)[["timestamp", "candle"]].copy()
    ema_trend = modules.EMA.apply_EMA(main_raw, 50)[["timestamp", "50EMA"]].copy()
    support   = modules.heikin_ashi.heikin_ashi(rSupport)[["timestamp", "candle"]].copy()
    entry     = modules.candlestick.get_klines(pair, '1m')
    macd1MIN  = modules.MACD.apply_MACD(modules.heikin_ashi.heikin_ashi(default))

    # Rename the column to avoid conflict
    direction = direction.rename(columns={'candle': 'direction'})
    support   = support.rename(columns={'candle': 'support'})

    # Merge all the necessarily data into one Dataframe
    dataset = pandas.merge_asof(dataset, volume, on='timestamp')
    dataset = pandas.merge_asof(dataset, direction, on='timestamp')
    dataset = pandas.merge_asof(dataset, ema_trend, on='timestamp')
    dataset = pandas.merge_asof(dataset, support, on='timestamp')
    dataset = pandas.merge_asof(dataset, macd1MIN, on='timestamp')

    # Apply Place Order Condition
    dataset["GO_LONG"] = dataset.apply(GO_LONG_CONDITION, axis=1)
    dataset["GO_SHORT"] = dataset.apply(GO_SHORT_CONDITION, axis=1)
    dataset["EXIT_LONG"] = dataset.apply(EXIT_LONG_CONDITION, axis=1)
    dataset["EXIT_SHORT"] = dataset.apply(EXIT_SHORT_CONDITION, axis=1)
    return dataset

def GO_LONG_CONDITION(dataset):
    color = "GREEN"
    volume_confirmation = dataset['volume'] > dataset['volumeAvg']

    if  dataset['direction'] == color and \
        dataset['support'] == color and \
        dataset['MACD_long'] and \
        volume_confirmation : return True
    else: return False

def GO_SHORT_CONDITION(dataset):
    color = "RED"
    volume_confirmation = dataset['volume'] > dataset['volumeAvg']

    if  dataset['direction'] == color and \
        dataset['support'] == color and \
        dataset['MACD_short'] and \
        volume_confirmation : return True
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