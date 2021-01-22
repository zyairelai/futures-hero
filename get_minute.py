output_minute = False

import config
from keys import client
from binance.client import Client
from termcolor import colored

# Return Type >>> "RED_CANDLE" // "GREEN_CANDLE" // "WEAK_RED" // "WEAK_GREEN" // "RED_INDECISIVE" // "GREEN_INDECISIVE" // "NO_MOVEMENT"

def get_current_minute(entry_exit): 
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_1MINUTE, limit=3)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if entry_exit == "ENTRY": threshold = config.entry_threshold
    elif entry_exit == "EXIT": threshold = config.exit_threshold
    else: threshold = 0.15

    title = "CURRENT MINUTE   :   "
    price_movement = (current_High - current_Low) / current_Open * 100

    if output_minute:
        print("The current_Open is  :   " + str(current_Open))
        print("The current_Close is :   " + str(current_Close))
        print("The current_High is  :   " + str(current_High))
        print("The current_Low is   :   " + str(current_Low))
        print("The price_movement is:   " + str(price_movement))

    if (current_Open == current_High):
        if (price_movement >= threshold):
            minute_candle = "RED_CANDLE"
            print(colored(title + "RED", "red"))
        else:
            minute_candle = "WEAK_RED"
            print(colored(title + "WEAK_RED", "red"))

    elif (current_Open == current_Low):
        if (price_movement >= threshold):
            minute_candle = "GREEN_CANDLE"
            print(colored(title + "GREEN", "green"))
        else:
            minute_candle = "WEAK_GREEN"
            print(colored(title + "WEAK_GREEN", "green"))
            
    else:
        if (current_Open > current_Close):
            print(colored(title + "RED_INDECISIVE", "red"))
            minute_candle = "RED_INDECISIVE"

        elif (current_Close > current_Open):
            print(colored(title + "GREEN_INDECISIVE", "green"))
            minute_candle = "GREEN_INDECISIVE"

        else:
            minute_candle = "NO_MOVEMENT"
            print(colored(title + "NO_MOVEMENT", "yellow"))
    return minute_candle

def recent_minute_count(minute): 
    if minute == 3: klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_3MINUTE, limit=3)
    elif minute == 5: klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_5MINUTE, limit=3)
    else:
        minute = 5
        klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_5MINUTE, limit=3)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    title           = "RECENT " + minute + " MINUTE  :   "
    threshold       = config.entry_threshold * 5
    price_movement  = (current_High - current_Low) / current_Open * 100

    if output_minute:
        print("The current_Open is  :   " + str(current_Open))
        print("The current_Close is :   " + str(current_Close))
        print("The current_High is  :   " + str(current_High))
        print("The current_Low is   :   " + str(current_Low))
        print("The price_movement is:   " + str(price_movement))

    if (current_Open == current_High):
        if (price_movement >= threshold):
            minute_candle = "RED_CANDLE"
            print(colored(title + "RED", "red"))
        else:
            minute_candle = "WEAK_RED"
            print(title + colored("WEAK_RED", "red"))

    elif (current_Open == current_Low):
        if (price_movement >= threshold):
            minute_candle = "GREEN_CANDLE"
            print(colored(title + "GREEN", "green"))
        else:
            minute_candle = "WEAK_GREEN"
            print(title + colored("WEAK_GREEN", "green"))
            
    else:
        if (current_Open > current_Close):
            print(title + colored("RED_INDECISIVE", "red"))
            minute_candle = "RED_INDECISIVE"

        elif (current_Close > current_Open):
            print(title + colored("GREEN_INDECISIVE", "green"))
            minute_candle = "GREEN_INDECISIVE"

        else:
            minute_candle = "NO_MOVEMENT"
            print(title + colored("NO_MOVEMENT", "white"))
    return minute_candle