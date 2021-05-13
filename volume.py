import binance_futures, heikin_ashi
from termcolor import colored

def volume_formation(klines):
    if  binance_futures.previous_volume(klines) > binance_futures.firstrun_volume(klines) and \
        binance_futures.current_volume(klines) > (binance_futures.previous_volume(klines) / 1.5): return True

def volume_breakout(klines):
    if binance_futures.current_volume(klines) > (binance_futures.previous_volume(klines) * 2) and heikin_ashi.current_candlebody(klines) > (heikin_ashi.previous_candlebody(klines) * 2): return True

def volume_weakening(klines):
    milliseconds = int(klines[-1][0]) - int(klines[-2][0])
    if milliseconds == 1 * 60 * 60000: interval = "1 HOUR"
    elif milliseconds == 6 * 60 * 60000: interval = "6 HOUR"

    if binance_futures.firstrun_volume(klines) > binance_futures.previous_volume(klines) and binance_futures.previous_volume(klines) > binance_futures.current_volume(klines):
        print("WEAKENING " + interval + " :   TRUE")
        return True
    else:
        print("WEAKENING " + interval + " :   FALSE")
        return False

def volume_declining(klines):
    milliseconds = int(klines[-1][0]) - int(klines[-2][0])
    if milliseconds == 1 * 60 * 60000: interval = "1 HOUR"
    elif milliseconds == 6 * 60 * 60000: interval = "6 HOUR"

    if binance_futures.initial_volume(klines) > binance_futures.firstrun_volume(klines) and \
       binance_futures.firstrun_volume(klines) > binance_futures.previous_volume(klines) and \
       binance_futures.previous_volume(klines) > binance_futures.current_volume(klines):
       print("🚫 " + interval + " VOLUME DECLINING 🚫")
       return True
