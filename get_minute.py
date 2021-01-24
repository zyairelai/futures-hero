import config
import binance_futures
from termcolor import colored

# Return Type >>> "RED" // "GREEN" // "WEAK_RED" // "WEAK_GREEN" // "RED_INDECISIVE" // "GREEN_INDECISIVE" // "NO_MOVEMENT"
threshold = 0

def get_current_minute():
    title = "CURRENT MINUTE   :   "
    klines = binance_futures.KLINE_INTERVAL_1MINUTE()

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    # threshold = config.threshold
    price_movement = (current_High - current_Low) / current_Open * 100

    if config.output:
        print("The current_Open is  :   " + str(current_Open))
        print("The current_Close is :   " + str(current_Close))
        print("The current_High is  :   " + str(current_High))
        print("The current_Low is   :   " + str(current_Low))
        print("The price_movement is:   " + str(price_movement))

    if (current_Open == current_High):
        if (price_movement >= threshold):
            minute_candle = "RED"
            print(colored(title + minute_candle, "red"))
        else:
            minute_candle = "WEAK_RED"
            print(colored(title + minute_candle, "red"))

    elif (current_Open == current_Low):
        if (price_movement >= threshold):
            minute_candle = "GREEN"
            print(colored(title + minute_candle, "green"))
        else:
            minute_candle = "WEAK_GREEN"
            print(colored(title + minute_candle, "green"))
            
    else:
        if (current_Open > current_Close):
            minute_candle = "RED_INDECISIVE"
            print(colored(title + minute_candle, "red"))

        elif (current_Close > current_Open):
            minute_candle = "GREEN_INDECISIVE"
            print(colored(title + minute_candle, "green"))

        else:
            minute_candle = "NO_MOVEMENT"
            print(colored(title + minute_candle, "yellow"))
    return minute_candle

def recent_minute_count(minute): 
    if   minute == 3: klines = binance_futures.KLINE_INTERVAL_3MINUTE()
    elif minute == 5: klines = binance_futures.KLINE_INTERVAL_5MINUTE()
    else:
        minute = 5
        klines = klines = binance_futures.KLINE_INTERVAL_5MINUTE()
    
    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    title           = "RECENT " + str(minute) + " MINUTE  :   "
    # threshold       = config.threshold * (minute - 1)
    price_movement  = (current_High - current_Low) / current_Open * 100

    if config.output:
        print("The current_Open is  :   " + str(current_Open))
        print("The current_Close is :   " + str(current_Close))
        print("The current_High is  :   " + str(current_High))
        print("The current_Low is   :   " + str(current_Low))
        print("The price_movement is:   " + str(price_movement))

    if (current_Open == current_High):
        if (price_movement >= threshold):
            minute_candle = "RED"
            print(colored(title + minute_candle, "red"))
        else:
            minute_candle = "WEAK_RED"
            print(colored(title + minute_candle, "red"))

    elif (current_Open == current_Low):
        if (price_movement >= threshold):
            minute_candle = "GREEN"
            print(colored(title + minute_candle, "green"))
        else:
            minute_candle = "WEAK_GREEN"
            print(colored(title + minute_candle, "green"))
            
    else:
        if (current_Open > current_Close):
            minute_candle = "RED_INDECISIVE"
            print(colored(title + minute_candle, "red"))

        elif (current_Close > current_Open):
            minute_candle = "GREEN_INDECISIVE"
            print(colored(title + minute_candle, "green"))

        else:
            minute_candle = "NO_MOVEMENT"
            print(colored(title + minute_candle, "white"))
    return minute_candle