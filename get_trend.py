import config
import get_minute
import binance_futures
from termcolor import colored

def get_current_trend(): # >>> "UP_TREND" // "DOWN_TREND" // "NO_TRADE_ZONE"
    main_direction = get_hour(config.main_hour)
    support_direction = get_hour(config.support_dir)
    recent_minute_count = get_minute.recent_minute_count(config.recent_min)
    if (main_direction == "GREEN") and (support_direction == "GREEN") and (recent_minute_count == "GREEN"): trend = "UP_TREND"
    elif (main_direction == "RED") and (support_direction == "RED") and (recent_minute_count == "RED"): trend = "DOWN_TREND"
    else: trend = "NO_TRADE_ZONE"
    return trend

def get_hour(hour): # >>> "UP" // "DOWN" // "INDECISIVE"
    title = str(hour) + " HOUR DIRECTION :   "
    threshold = config.threshold * 10

    if hour == 15:
        klines = binance_futures.KLINE_INTERVAL_15MINUTE()
        title = str(hour) + " MIN DIRECTION :   "
    elif hour == 30:
        klines = binance_futures.KLINE_INTERVAL_30MINUTE()
        title = str(hour) + " MIN DIRECTION :   "
    elif hour == 1: klines = binance_futures.KLINE_INTERVAL_1HOUR()
    elif hour == 2: klines = binance_futures.KLINE_INTERVAL_2HOUR()
    elif hour == 4: klines = binance_futures.KLINE_INTERVAL_4HOUR()
    else:
        hour = 6
        klines = binance_futures.KLINE_INTERVAL_6HOUR()
        threshold = config.threshold * 30

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    price_movement = abs((current_Open - current_Close) / current_Open * 100)

    if config.output:
        print("The current_Open is  :   " + str(current_Open))
        print("The current_Close is :   " + str(current_Close))
        print("The current_High is  :   " + str(current_High))
        print("The current_Low is   :   " + str(current_Low))
        print("The price_movement is:   " + str(price_movement))

    if (current_Open == current_Low):
        if (price_movement >= threshold):
            trend = "GREEN"
            print(colored(title + trend, "green"))
        else:
            trend = "INDECISIVE" # "WEAK_RED"
            print(colored(title + trend, "green"))

    elif (current_Open == current_High):
        if (price_movement >= threshold):
            trend = "RED"
            print(colored(title + trend, "red"))
        else:
            trend = "INDECISIVE" # "WEAK_GREEN"
            print(colored(title + trend, "red"))

    else:
        trend = "NO_TRADE_ZONE"
        print(colored(title + trend, "yellow"))

    return trend
