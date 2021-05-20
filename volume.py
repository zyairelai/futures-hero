import binance_futures_api, HA_current, HA_previous

def volume_formation(klines):
    if  binance_futures_api.previous_volume(klines) > binance_futures_api.firstrun_volume(klines) and \
        binance_futures_api.current_volume(klines) > (binance_futures_api.previous_volume(klines) / 1.5): return True

def volume_breakout(klines):
    if binance_futures_api.current_volume(klines) > (binance_futures_api.previous_volume(klines) * 2) and HA_current.candlebody(klines) > (HA_previous.candlebody(klines) * 2): return True

def volume_weakening(klines):
    milliseconds = int(klines[-1][0]) - int(klines[-2][0])
    if milliseconds == 1 * 60 * 60000: interval = "1 HOUR"
    elif milliseconds == 6 * 60 * 60000: interval = "6 HOUR"

    if binance_futures_api.firstrun_volume(klines) > binance_futures_api.previous_volume(klines) and binance_futures_api.previous_volume(klines) > binance_futures_api.current_volume(klines):
        print("WEAKENING " + interval + " :   TRUE")
        return True
    else:
        print("WEAKENING " + interval + " :   FALSE")
        return False

def volume_declining(klines):
    milliseconds = int(klines[-1][0]) - int(klines[-2][0])
    if milliseconds == 1 * 60 * 60000: interval = "1 HOUR"
    elif milliseconds == 6 * 60 * 60000: interval = "6 HOUR"

    if binance_futures_api.initial_volume(klines) > binance_futures_api.firstrun_volume(klines) and \
       binance_futures_api.firstrun_volume(klines) > binance_futures_api.previous_volume(klines) and \
       binance_futures_api.previous_volume(klines) > binance_futures_api.current_volume(klines):
       print("🚫 " + interval + " VOLUME DECLINING 🚫")
       return True
