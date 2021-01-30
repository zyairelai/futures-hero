import config
import binance_futures
from termcolor import colored

def recent_minute():
    klines = klines = binance_futures.KLINE_INTERVAL_5MINUTE()

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if (current_Open == current_High):
        minute_candle = "RED"
        print(colored("RECENT 5 MINUTE  :   " + minute_candle, "red"))
    elif (current_Open == current_Low):
        minute_candle = "GREEN"
        print(colored("RECENT 5 MINUTE  :   " + minute_candle, "green"))

    else:
        if (current_Open > current_Close):
            minute_candle = "RED_INDECISIVE"
            print(colored("RECENT 5 MINUTE  :   " + minute_candle, "red"))
        elif (current_Close > current_Open):
            minute_candle = "GREEN_INDECISIVE"
            print(colored("RECENT 5 MINUTE  :   " + minute_candle, "green"))
        else:
            minute_candle = "NO_MOVEMENT"
            print(colored("RECENT 5 MINUTE  :   " + minute_candle, "white"))
    return minute_candle

def emergency_minute():
    klines = klines = binance_futures.KLINE_INTERVAL_1MINUTE()

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    threshold = 0.3
    emergency = "INDECISIVE"
    price_movement  = (current_High - current_Low) / current_Open * 100

    if (current_Open == current_High): 
        if (price_movement >= threshold): 
            emergency = "RED"

    elif (current_Open == current_Low): 
        if (price_movement >= threshold): 
            emergency = "GREEN"

    return emergency
