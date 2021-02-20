import config
import binance_futures
from termcolor import colored

def entry_test(CANDLE, INTERVAL):
    if INTERVAL == "1MINUTE": klines = binance_futures.KLINE_INTERVAL_1MINUTE(4)
    elif INTERVAL == "3MINUTE": klines = binance_futures.KLINE_INTERVAL_3MINUTE(4)
    elif INTERVAL == "5MINUTE": klines = binance_futures.KLINE_INTERVAL_5MINUTE(4)
    elif INTERVAL == "15MINUTE": klines = binance_futures.KLINE_INTERVAL_15MINUTE(4)
    elif INTERVAL == "30MINUTE": klines = binance_futures.KLINE_INTERVAL_30MINUTE(4)
    elif INTERVAL == "1HOUR": klines = binance_futures.KLINE_INTERVAL_1HOUR(4)
    elif INTERVAL == "2HOUR": klines = binance_futures.KLINE_INTERVAL_2HOUR(4)
    elif INTERVAL == "4HOUR": klines = binance_futures.KLINE_INTERVAL_4HOUR(4)
    elif INTERVAL == "6HOUR": klines = binance_futures.KLINE_INTERVAL_6HOUR(4)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    first_Open      = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    first_Close     = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)

    previous_Open   = round(((first_Open + first_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[1][3]) + float(klines[2][4])) / 4), config.round_decimal)
    previous_High   = max(float(klines[2][2]), previous_Open, previous_Close)
    previous_Low    = min(float(klines[2][3]), previous_Open, previous_Close)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[3][1]) + float(klines[3][2]) + float(klines[3][3]) + float(klines[3][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[3][2]), current_Open, current_Close)
    current_Low     = min(float(klines[3][3]), current_Open, current_Close)

    if CANDLE == "GREEN":
        if (current_High > previous_High): return "PASS"
        else: return "FAIL"
    elif CANDLE == "RED":
        if (current_Low < previous_Low): return "PASS"
        else: return "FAIL"

def one_minute_exit_test(CANDLE):
    klines = binance_futures.KLINE_INTERVAL_1MINUTE(4)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    first_Open      = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    first_Close     = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)

    previous_Open   = round(((first_Open + first_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[1][3]) + float(klines[2][4])) / 4), config.round_decimal)
    previous_High   = max(float(klines[2][2]), previous_Open, previous_Close)
    previous_Low    = min(float(klines[2][3]), previous_Open, previous_Close)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[3][1]) + float(klines[3][2]) + float(klines[3][3]) + float(klines[3][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[3][2]), current_Open, current_Close)
    current_Low     = min(float(klines[3][3]), current_Open, current_Close)

    threshold = abs((previous_Open - previous_Close) / 4)

    if CANDLE == "GREEN":
        if (previous_High > current_High) and (current_Low < (previous_Low + threshold)): return "PASS"
        elif current_Low < previous_Low: return "PASS"
        else: return "FAIL"
    elif CANDLE == "RED":
        if (current_Low > previous_Low) and (current_High > (previous_High - threshold)): return "PASS"
        elif current_High > previous_High: return "PASS"
        else: return "FAIL"
