import config
import binance_futures
from termcolor import colored

def pencil_wick_test(CANDLE):
    title  = "PENCIL WICK TEST :   "
    klines = binance_futures.KLINE_INTERVAL_1MINUTE()

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)

    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)
    previous_High   = max(float(klines[1][2]), previous_Open, previous_Close)
    previous_Low    = min(float(klines[1][3]), previous_Open, previous_Close)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    threshold = 0.05

    if CANDLE == "GREEN":
        if current_High < previous_High:
            if ((current_High - previous_High) / current_High * 100) < threshold:
                result = "PASS"
            else: result = "FAIL"
        else: result = "PASS"

    elif CANDLE == "RED":
        if current_Low > previous_Low:
            if ((previous_Low - current_Low) / previous_Low * 100) < threshold:
                result = "PASS"
            else: result = "FAIL"
        else: result = "PASS"

    if result == "PASS": print(colored(title + result, "green"))
    else: print(colored(title + result, "red"))

    return result
