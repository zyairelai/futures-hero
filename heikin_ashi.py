import config
import binance_futures
from datetime import datetime
from termcolor import colored
troubleshooting = config.troubleshooting

def get_clear_direction(): # return RED // GREEN // INDECISIVE
    klines = binance_futures.KLINE_INTERVAL_6HOUR()

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)

    first_Open      = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    first_Close     = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)
    first_High      = max(float(klines[1][2]), first_Open, first_Close)
    first_Low       = min(float(klines[1][3]), first_Open, first_Close)

    previous_Open   = round(((first_Open + first_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[1][3]) + float(klines[2][4])) / 4), config.round_decimal)
    previous_High   = max(float(klines[2][2]), previous_Open, previous_Close)
    previous_Low    = min(float(klines[2][3]), previous_Open, previous_Close)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[3][1]) + float(klines[3][2]) + float(klines[3][3]) + float(klines[3][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[3][2]), current_Open, current_Close)
    current_Low     = min(float(klines[3][3]), current_Open, current_Close)

    if troubleshooting:
        print("The previous_Open is  :   " + str(previous_Open))
        print("The previous_Close is :   " + str(previous_Close))
        print("The previous_High is  :   " + str(previous_High))
        print("The previous_Low is   :   " + str(previous_Low))

    title = "PREVIOUS 6 HOUR  :   "
    if (previous_Open == previous_Low):
        previous = "GREEN"
        print(colored(title + previous, "green"))

    elif (previous_Close > previous_Open):
        previous = "GREEN_INDECISIVE"
        print(colored(title + previous, "green"))

    elif (previous_Open == previous_High):
        previous = "RED"
        print(colored(title + previous, "red"))

    elif (previous_Open > previous_Close):
        previous = "RED_INDECISIVE"
        print(colored(title + previous, "yellow"))

    else:
        previous = "NO_MOVEMENT"
        print(colored(title + previous, "yellow"))

    if troubleshooting:
        print("The current_Open is  :   " + str(current_Open))
        print("The current_Close is :   " + str(current_Close))
        print("The current_High is  :   " + str(current_High))
        print("The current_Low is   :   " + str(current_Low))

    title = "CURRENT 6 HOUR   :   "
    if (current_Open == current_Low):
        current = "GREEN"
        print(colored(title + current, "green"))

    elif (current_Close > current_Open):
        current = "GREEN_INDECISIVE"
        print(colored(title + current, "yellow"))

    elif (current_Open == current_High):
        current = "RED"
        print(colored(title + current, "red"))

    elif (current_Open > current_Close):
        current = "RED_INDECISIVE"
        print(colored(title + current, "yellow"))

    else:
        current = "NO_MOVEMENT"
        print(colored(title + current, "yellow"))

    if (previous == "GREEN") and (current == "GREEN"): trend = "GREEN"
    elif ((previous == "GREEN_INDECISIVE") and (previous_High > first_High)) and (current == "GREEN"): trend = "GREEN"
    elif (previous == "RED") and (current == "RED"): trend = "RED"
    elif ((previous == "RED_INDECISIVE") and (previous_Low < first_Low)) and (current == "RED"): trend = "RED"
    else: trend = "INDECISIVE"
    return trend

def get_hour(hour): # return RED // GREEN // INDECISIVE
    title = str(hour) + " HOUR DIRECTION :   "
    if hour == 1: klines = binance_futures.KLINE_INTERVAL_1HOUR()
    elif hour == 2: klines = binance_futures.KLINE_INTERVAL_2HOUR()
    elif hour == 4: klines = binance_futures.KLINE_INTERVAL_4HOUR()
    elif hour == 6: klines = binance_futures.KLINE_INTERVAL_6HOUR()

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    first_Open      = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    first_Close     = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_Open + first_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[1][3]) + float(klines[2][4])) / 4), config.round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[3][1]) + float(klines[3][2]) + float(klines[3][3]) + float(klines[3][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[3][2]), current_Open, current_Close)
    current_Low     = min(float(klines[3][3]), current_Open, current_Close)

    if troubleshooting:
        print("The current_Open is  :   " + str(current_Open))
        print("The current_Close is :   " + str(current_Close))
        print("The current_High is  :   " + str(current_High))
        print("The current_Low is   :   " + str(current_Low))

    if (current_Open == current_Low):
        current = "GREEN"
        print(colored(title + current, "green"))

    elif (current_Close > current_Open):
        current = "GREEN_INDECISIVE"
        print(colored(title + current, "yellow"))

    elif (current_Open == current_High):
        current = "RED"
        print(colored(title + current, "red"))

    elif (current_Open > current_Close):
        current = "RED_INDECISIVE"
        print(colored(title + current, "yellow"))

    else:
        current = "NO_MOVEMENT"
        print(colored(title + current, "yellow"))

    return current

def get_current_minute(minute): # return RED // GREEN // RED_INDECISIVE // GREEN_INDECISIVE // NO_MOVEMENT
    if minute == 1: klines = klines = binance_futures.KLINE_INTERVAL_1MINUTE()
    elif minute == 3: klines = klines = binance_futures.KLINE_INTERVAL_3MINUTE()
    elif minute == 5: klines = klines = binance_futures.KLINE_INTERVAL_5MINUTE()
    elif minute == 15: klines = binance_futures.KLINE_INTERVAL_15MINUTE()
    elif minute == 30: klines = binance_futures.KLINE_INTERVAL_30MINUTE()

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    first_Open      = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    first_Close     = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_Open + first_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[1][3]) + float(klines[2][4])) / 4), config.round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[3][1]) + float(klines[3][2]) + float(klines[3][3]) + float(klines[3][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[3][2]), current_Open, current_Close)
    current_Low     = min(float(klines[3][3]), current_Open, current_Close)

    if troubleshooting:
        print("The current_Open is  :   " + str(current_Open))
        print("The current_Close is :   " + str(current_Close))
        print("The current_High is  :   " + str(current_High))
        print("The current_Low is   :   " + str(current_Low))

    if (current_Open == current_High):
        minute_candle = "RED"
        print(colored("RECENT " + str(minute) + " MINUTE  :   " + minute_candle, "red"))

    elif (current_Open == current_Low):
        minute_candle = "GREEN"
        print(colored("RECENT " + str(minute) + " MINUTE  :   " + minute_candle, "green"))

    elif (current_Open > current_Close):
        minute_candle = "RED_INDECISIVE"
        print(colored("RECENT " + str(minute) + " MINUTE  :   " + minute_candle, "red"))

    elif (current_Close > current_Open):
        minute_candle = "GREEN_INDECISIVE"
        print(colored("RECENT " + str(minute) + " MINUTE  :   " + minute_candle, "green"))

    else:
        minute_candle = "NO_MOVEMENT"
        print(colored("RECENT " + str(minute) + " MINUTE  :   " + minute_candle, "white"))
    return minute_candle

def silent_candle(INTERVAL):
    if INTERVAL == "1MINUTE": klines = binance_futures.KLINE_INTERVAL_1MINUTE()
    elif INTERVAL == "3MINUTE": klines = binance_futures.KLINE_INTERVAL_3MINUTE()
    elif INTERVAL == "5MINUTE": klines = binance_futures.KLINE_INTERVAL_5MINUTE()
    elif INTERVAL == "15MINUTE": klines = binance_futures.KLINE_INTERVAL_15MINUTE()
    elif INTERVAL == "30MINUTE": klines = binance_futures.KLINE_INTERVAL_30MINUTE()
    elif INTERVAL == "1HOUR": klines = binance_futures.KLINE_INTERVAL_1HOUR()
    elif INTERVAL == "2HOUR": klines = binance_futures.KLINE_INTERVAL_2HOUR()
    elif INTERVAL == "4HOUR": klines = binance_futures.KLINE_INTERVAL_4HOUR()
    elif INTERVAL == "6HOUR": klines = binance_futures.KLINE_INTERVAL_6HOUR()

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    first_Open      = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    first_Close     = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)

    previous_Open   = round(((first_Open + first_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[1][3]) + float(klines[2][4])) / 4), config.round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[3][1]) + float(klines[3][2]) + float(klines[3][3]) + float(klines[3][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[3][2]), current_Open, current_Close)
    current_Low     = min(float(klines[3][3]), current_Open, current_Close)

    if (current_Open == current_High): silent_candle = "RED"
    elif (current_Open == current_Low): silent_candle = "GREEN"
    elif (current_Open > current_Close): silent_candle = "RED_INDECISIVE"
    elif (current_Close > current_Open): silent_candle = "GREEN_INDECISIVE"
    else: silent_candle = "NO_MOVEMENT"
    return silent_candle
