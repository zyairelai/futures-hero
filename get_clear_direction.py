import config
import binance_futures
from datetime import datetime
from termcolor import colored

def clear_direction():
    klines = binance_futures.KLINE_INTERVAL_6HOUR()

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

    # print("The current_Open is  :   " + str(current_Open))
    # print("The current_Close is :   " + str(current_Close))
    # print("The current_High is  :   " + str(current_High))
    # print("The current_Low is   :   " + str(current_Low))
    # print("The Mark Price is    :   " + binance_futures.position_information()[0].get("markPrice"))

    title = "PREVIOUS 6 HOUR  :   "
    if (previous_Open == previous_Low):
        previous = "GREEN"
        print(colored(title + previous, "green"))
    elif (previous_Open == previous_High):
        previous = "RED"
        print(colored(title + previous, "red"))
    else:
        previous = "NO_TRADE_ZONE"
        print(colored(title + previous, "yellow"))

    title = "CURRENT 6 HOUR   :   "
    if (current_Open == current_Low):
        current = "GREEN"
        print(colored(title + current, "green"))
    elif (current_Open == current_High):
        current = "RED"
        print(colored(title + current, "red"))
    else:
        current = "NO_TRADE_ZONE"
        print(colored(title + current, "yellow"))

    if (previous == "GREEN") and (current == "GREEN"): trend = "UP_TREND"
    elif (previous == "RED") and (current == "RED"): trend = "DOWN_TREND"
    else: trend = "NO_TRADE_ZONE"
    return trend
