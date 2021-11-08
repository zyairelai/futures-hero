import pandas, os
import modules.MACD
import modules.candlestick
import modules.heikin_ashi

test_module = False

def futures_hero(pair):
    # Process Heikin Ashi & Apply Technical Analysis
    main_raw    = modules.candlestick.get_klines(pair, '6h')
    support_raw = modules.candlestick.get_klines(pair, '4h')
    entry       = modules.candlestick.get_klines(pair, '1m')

    default, process = entry, entry
    main_candle    = modules.candlestick.candlestick(main_raw)[["timestamp", "color"]].copy()
    main_direction = modules.heikin_ashi.heikin_ashi(main_raw)[["timestamp", "color"]].copy()
    support_candle = modules.candlestick.candlestick(support_raw)[["timestamp", "color"]].copy()
    support_HA     = modules.heikin_ashi.heikin_ashi(support_raw)[["timestamp", "color"]].copy()

    # Backtest with FEDA json
    feda_klines = "feda_output.json"
    if os.path.isfile(feda_klines):
        feda_1min = pandas.read_json(feda_klines)
        feda_1min = feda_1min.rename({0: 'timestamp', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'volume'}, axis=1)
        default, process = feda_1min, feda_1min

    dataset   = modules.candlestick.candlestick(default)
    macd1MIN  = modules.MACD.apply_default(modules.heikin_ashi.heikin_ashi(process))

    main_candle    = main_candle.rename(columns={'color': 'main_candle'})
    main_direction = main_direction.rename(columns={'color': 'main_HA'})
    support_candle = support_candle.rename(columns={'color': 'support_candle'})
    support_HA     = support_HA.rename(columns={'color': 'support_HA'})

    # Merge all the necessarily data into one Dataframe
    dataset = pandas.merge_asof(dataset, main_candle, on='timestamp')
    dataset = pandas.merge_asof(dataset, main_direction, on='timestamp')
    dataset = pandas.merge_asof(dataset, support_candle, on='timestamp')
    dataset = pandas.merge_asof(dataset, support_HA, on='timestamp')
    dataset = pandas.merge_asof(dataset, macd1MIN, on='timestamp')

    # Apply Place Order Condition
    dataset["GO_LONG"] = dataset.apply(GO_LONG_CONDITION, axis=1)
    dataset["GO_SHORT"] = dataset.apply(GO_SHORT_CONDITION, axis=1)
    dataset["EXIT_LONG"] = dataset.apply(EXIT_LONG_CONDITION, axis=1)
    dataset["EXIT_SHORT"] = dataset.apply(EXIT_SHORT_CONDITION, axis=1)
    return dataset

def GO_LONG_CONDITION(dataset):
    color = "GREEN"
    if  dataset['main_candle'] == color and \
        dataset['main_HA']     == color and \
        dataset['support_candle'] == color and \
        dataset['support_HA']  == color and \
        dataset['MACD_long'] : return True
    else: return False

def GO_SHORT_CONDITION(dataset):
    color = "RED"
    if  dataset['main_candle'] == color and \
        dataset['main_HA']     == color and \
        dataset['support_candle'] == color and \
        dataset['support_HA']  == color and \
        dataset['MACD_short'] : return True
    else: return False

def EXIT_LONG_CONDITION(dataset):
    if dataset['MACD_short']: return True
    else : return False

def EXIT_SHORT_CONDITION(dataset):
    if dataset['MACD_long']: return True
    else : return False

if test_module:
    run = futures_hero("ETHUSDT")
    print(run)