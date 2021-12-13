import pandas, os
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
        default = pandas.read_json(feda_klines).rename({0: 'timestamp', 1: 'open', 2: 'high', 3: 'low', 4: 'close', 5: 'vol'}, axis=1) 
    else: default = entry

    # Process Heikin Ashi & Apply Technical Analysis
    dataset  = modules.candlestick.candlestick(default)
    main_can = modules.candlestick.candlestick(main_raw)[["timestamp", "color"]].copy()
    main_dir = modules.heikin_ashi.heikin_ashi(main_raw)[["timestamp", "color"]].copy()
    supp_can = modules.candlestick.candlestick(rSupport)[["timestamp", "color"]].copy()
    supp_dir = modules.heikin_ashi.heikin_ashi(rSupport)[["timestamp", "color"]].copy()
    macd1MIN = modules.MACD.apply_MACD(modules.heikin_ashi.heikin_ashi(default))

    # Rename the column to avoid conflict
    main_can = main_can.rename(columns={'color': 'main_candle'})
    main_dir = main_dir.rename(columns={'color': 'main_HA'})
    supp_can = supp_can.rename(columns={'color': 'support_candle'})
    supp_dir = supp_dir.rename(columns={'color': 'support_HA'})

    # Merge all the necessarily data into one Dataframe
    dataset = pandas.merge_asof(dataset, main_can, on='timestamp')
    dataset = pandas.merge_asof(dataset, main_dir, on='timestamp')
    dataset = pandas.merge_asof(dataset, supp_can, on='timestamp')
    dataset = pandas.merge_asof(dataset, supp_dir, on='timestamp')
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