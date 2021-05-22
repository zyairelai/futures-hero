import binance_futures_api

def get_out_zone(klines_30MIN, klines_6HOUR):
    future_direction = binance_futures_api.timestamp_of(klines_6HOUR) + return_interval(klines_6HOUR)
    get_out_zone = future_direction - return_interval(klines_30MIN)
    if binance_futures_api.get_timestamp() > get_out_zone: return True

def return_interval(klines):
    milliseconds = int(klines[-1][0]) - int(klines[-2][0])
    if milliseconds == 1 * 60000: interval = 1
    elif milliseconds == 3 * 60000: interval = 3
    elif milliseconds == 5 * 60000: interval = 5
    elif milliseconds == 15 * 60000: interval = 15
    elif milliseconds == 30 * 60000: interval = 30
    elif milliseconds == 1 * 60 * 60000: interval = 1 * 60
    elif milliseconds == 2 * 60 * 60000: interval = 2 * 60
    elif milliseconds == 4 * 60 * 60000: interval = 4 * 60
    elif milliseconds == 6 * 60 * 60000: interval = 6 * 60
    elif milliseconds == 12 * 60 * 60000: interval = 12 * 60
    return (interval * 60000)
