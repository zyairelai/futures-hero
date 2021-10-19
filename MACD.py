import pandas as pd
import candlestick
import binance_futures_api

lower_length = 12
higher_length = 26
signal_length = 9

def current(EMA_list):
    return round(float(EMA_list[-1]), 2)

def compute_EMA(digit, dataset):
    df = pd.DataFrame(dataset)
    ema = df.ewm(span=digit).mean()
    return ema[0].values.tolist()

def compute_MACD_list(dataset):
    MACD_list = []
    lower_EMA = compute_EMA(lower_length, dataset)
    higher_EMA = compute_EMA(higher_length, dataset)
    for i in range(len(higher_EMA)): MACD_list.append(lower_EMA[i] - higher_EMA[i])
    return MACD_list

def compute_Signal_list(dataset):
    return compute_EMA(signal_length, dataset)

def compute_histogram(MACD_list, Signal_list):
    histogram = []
    for i in range(len(MACD_list)): histogram.append(MACD_list[i] - Signal_list[i])
    return histogram

def long_condition(klines):
    closing = candlestick.closing_price_list(klines)
    MACD_list = compute_MACD_list(closing)
    Signal_list = compute_Signal_list(MACD_list)
    current_MACD = current(MACD_list)
    current_signal = current(Signal_list)
    current_histogram = current(compute_histogram(MACD_list, Signal_list))
    return True if current_histogram > 0 and current_MACD > current_signal else False

def short_condition(klines):
    closing = candlestick.closing_price_list(klines)
    MACD_list = compute_MACD_list(closing)
    Signal_list = compute_Signal_list(MACD_list)
    current_MACD = current(MACD_list)
    current_signal = current(Signal_list)
    current_histogram = current(compute_histogram(MACD_list, Signal_list))
    return True if current_histogram < 0 and current_MACD < current_signal else False

def test():
    klines_1MIN  = binance_futures_api.KLINE_INTERVAL_1MINUTE(0)
    closing = candlestick.closing_price_list(klines_1MIN)

    MACD_list = compute_MACD_list(closing)
    Signal_list = compute_Signal_list(MACD_list)

    current_MACD = current(MACD_list)
    current_signal = current(Signal_list)
    current_histogram = current(compute_histogram(MACD_list, Signal_list))

    print(current_histogram)
    print(current_MACD)
    print(current_signal)
