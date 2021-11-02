import pandas
import modules.MACD
import modules.candlestick
import modules.heikin_ashi

test_module = False

def futures_hero(pair):
    # Process Heikin Ashi & Apply Technical Analysis
    dataset  = modules.candlestick.candlestick(modules.candlestick.KLINE_INTERVAL_1MIN(pair))
    ha_6HOUR = modules.heikin_ashi.heikin_ashi(modules.candlestick.KLINE_INTERVAL_6HOUR(pair))[["timestamp", "candle"]].copy()
    ha_1HOUR = modules.heikin_ashi.heikin_ashi(modules.candlestick.KLINE_INTERVAL_1HOUR(pair))[["timestamp", "candle"]].copy()
    macd1MIN = modules.MACD.apply_default(modules.candlestick.KLINE_INTERVAL_1MIN(pair))
    ha_6HOUR = ha_6HOUR.rename(columns={'candle': '6_HOUR'})
    ha_1HOUR = ha_1HOUR.rename(columns={'candle': '1_HOUR'})

    # Merge all the necessarily data into one Dataframe
    dataset = pandas.merge_asof(dataset, ha_6HOUR, on='timestamp')
    dataset = pandas.merge_asof(dataset, ha_1HOUR, on='timestamp')
    dataset = pandas.merge_asof(dataset, macd1MIN, on='timestamp')

    # Apply Place Order Condition
    dataset["GO_LONG"] = dataset.apply(GO_LONG_CONDITION, axis=1)
    dataset["GO_SHORT"] = dataset.apply(GO_SHORT_CONDITION, axis=1)
    dataset["EXIT_LONG"] = dataset.apply(EXIT_LONG_CONDITION, axis=1)
    dataset["EXIT_SHORT"] = dataset.apply(EXIT_SHORT_CONDITION, axis=1)
    return dataset

def GO_LONG_CONDITION(dataset):
    if dataset['6_HOUR'] == "GREEN" and dataset['1_HOUR'] == "GREEN" and dataset['MACD_long'] : return True
    else: return False

def GO_SHORT_CONDITION(dataset):
    if dataset['6_HOUR'] == "RED" and dataset['1_HOUR'] == "RED" and dataset['MACD_short'] : return True
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