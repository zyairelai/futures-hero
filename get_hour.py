super_clear_direction = False

import config
import binance_futures
from datetime import datetime
from termcolor import colored
from get_position import get_position_info

def get_hour(hour):
    title = str(hour) + " HOUR DIRECTION :   "
    if hour == 1: klines = binance_futures.KLINE_INTERVAL_1HOUR()
    elif hour == 2: klines = binance_futures.KLINE_INTERVAL_2HOUR()
    elif hour == 4: klines = binance_futures.KLINE_INTERVAL_4HOUR()
    else:
        hour = 6
        klines = binance_futures.KLINE_INTERVAL_6HOUR()

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)
    previous_High   = max(float(klines[2][2]), previous_Open, previous_Close)
    previous_Low    = min(float(klines[2][3]), previous_Open, previous_Close)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if (current_Open == current_Low):
        current = "GREEN"
        trend = "UP_TREND"
        print(colored(title + current, "green"))
    elif (current_Open == current_High):
        current = "RED"
        trend = "DOWN_TREND"
        print(colored(title + current, "red"))
    else:
        current = "NO_TRADE_ZONE"
        trend = "NO_TRADE_ZONE"
        print(colored(title + current, "yellow"))

    if super_clear_direction:
        title = str(hour) + " HOUR DIRECTION :   "
        if (previous_Open == previous_Low):
            previous = "GREEN"
            print(colored(title + previous, "green"))
        elif (previous_Open == previous_High):
            previous = "RED"
            print(colored(title + previous, "red"))
        else:
            previous = "NO_TRADE_ZONE"
            print(colored(title + previous, "yellow"))

        if (previous == "GREEN") and (current == "GREEN"): trend = "UP_TREND"
        elif (previous == "RED") and (current == "RED"): trend = "DOWN_TREND"
        else: trend = "NO_TRADE_ZONE"
    return trend

