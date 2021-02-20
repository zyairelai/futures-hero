import config
import binance_futures
from datetime import datetime
from termcolor import colored
troubleshooting = config.troubleshooting

def initial_Open(klines): return round(((float(klines[-4][1]) + float(klines[-4][4])) / 2), config.round_decimal)
def initial_Close(klines): return round(((float(klines[-4][1]) + float(klines[-4][2]) + float(klines[-4][3]) + float(klines[-4][4])) / 4), config.round_decimal)

def first_Open(klines): return round(((initial_Open(klines) + initial_Close(klines)) / 2), config.round_decimal)
def first_Close(klines): return round(((float(klines[-3][1]) + float(klines[-3][2]) + float(klines[-3][3]) + float(klines[-3][4])) / 4), config.round_decimal)
def first_High(klines): return max(float(klines[-3][2]), first_Open(klines), first_Close(klines))
def first_Low(klines): return min(float(klines[-3][3]), first_Open(klines), first_Close(klines))

def previous_Open(klines): return round(((first_Open(klines) + first_Close(klines)) / 2), config.round_decimal)
def previous_Close(klines): return round(((float(klines[-2][1]) + float(klines[-2][2]) + float(klines[-2][3]) + float(klines[-2][4])) / 4), config.round_decimal)
def previous_High(klines): return max(float(klines[-2][2]), previous_Open(klines), previous_Close(klines))
def previous_Low(klines): return min(float(klines[-2][3]), previous_Open(klines), previous_Close(klines))

def current_Open(klines): return round(((previous_Open(klines) + previous_Close(klines)) / 2), config.round_decimal)
def current_Close(klines): return round(((float(klines[-1][1]) + float(klines[-1][2]) + float(klines[-1][3]) + float(klines[-1][4])) / 4), config.round_decimal)
def current_High(klines): return max(float(klines[-1][2]), current_Open(klines), current_Close(klines))
def current_Low(klines): return min(float(klines[-1][3]), current_Open(klines), current_Close(klines))

def silent_candle(INTERVAL, TIME_TRAVEL): # return RED // GREEN // RED_INDECISIVE // GREEN_INDECISIVE // NO_MOVEMENT
    if INTERVAL == "1MINUTE": klines = binance_futures.KLINE_INTERVAL_1MINUTE(4)
    elif INTERVAL == "3MINUTE": klines = binance_futures.KLINE_INTERVAL_3MINUTE(4)
    elif INTERVAL == "5MINUTE": klines = binance_futures.KLINE_INTERVAL_5MINUTE(4)
    elif INTERVAL == "15MINUTE": klines = binance_futures.KLINE_INTERVAL_15MINUTE(4)
    elif INTERVAL == "30MINUTE": klines = binance_futures.KLINE_INTERVAL_30MINUTE(4)
    elif INTERVAL == "1HOUR": klines = binance_futures.KLINE_INTERVAL_1HOUR(4)
    elif INTERVAL == "2HOUR": klines = binance_futures.KLINE_INTERVAL_2HOUR(4)
    elif INTERVAL == "4HOUR": klines = binance_futures.KLINE_INTERVAL_4HOUR(4)
    elif INTERVAL == "6HOUR": klines = binance_futures.KLINE_INTERVAL_6HOUR(4)

    if TIME_TRAVEL == "FIRST":
        if (first_Open(klines) == first_High(klines)): return "RED"
        elif (first_Open(klines) == first_Low(klines)): return "GREEN"
        elif (first_Open(klines) > first_Close(klines)): return "RED_INDECISIVE"
        elif (first_Close(klines) > first_Open(klines)): return "GREEN_INDECISIVE"
        else: return "NO_MOVEMENT"

    elif TIME_TRAVEL == "PREVIOUS":
        if (previous_Open(klines) == previous_High(klines)): return "RED"
        elif (previous_Open(klines) == previous_Low(klines)): return "GREEN"
        elif (previous_Open(klines) > previous_Close(klines)): return "RED_INDECISIVE"
        elif (previous_Close(klines) > previous_Open(klines)): return "GREEN_INDECISIVE"
        else: return "NO_MOVEMENT"

    else:
        if (current_Open(klines) == current_High(klines)): return "RED"
        elif (current_Open(klines) == current_Low(klines)): return "GREEN"
        elif (current_Open(klines) > current_Close(klines)): return "RED_INDECISIVE"
        elif (current_Close(klines) > current_Open(klines)): return "GREEN_INDECISIVE"
        else: return "NO_MOVEMENT"

def get_clear_direction(): # return RED // GREEN // INDECISIVE
    six_hour = binance_futures.KLINE_INTERVAL_6HOUR(4)

    if troubleshooting:
        print("The previous_Open is  :   " + str(previous_Open(six_hour)))
        print("The previous_Close is :   " + str(previous_Close(six_hour)))
        print("The previous_High is  :   " + str(previous_High(six_hour)))
        print("The previous_Low is   :   " + str(previous_Low(six_hour)))

    title = "PREVIOUS 6 HOUR  :   "
    if (previous_Open(six_hour) == previous_Low(six_hour)):
        previous = "GREEN"
        print(colored(title + previous, "green"))

    elif (previous_Close(six_hour) > previous_Open(six_hour)):
        previous = "GREEN_INDECISIVE"
        print(colored(title + previous, "green"))

    elif (previous_Open(six_hour) == previous_High(six_hour)):
        previous = "RED"
        print(colored(title + previous, "red"))

    elif (previous_Open(six_hour) > previous_Close(six_hour)):
        previous = "RED_INDECISIVE"
        print(colored(title + previous, "red"))

    else:
        previous = "NO_MOVEMENT"
        print(colored(title + previous, "yellow"))

    if troubleshooting:
        print("The current_Open is  :   " + str(current_Open(six_hour)))
        print("The current_Close is :   " + str(current_Close(six_hour)))
        print("The current_High is  :   " + str(current_High(six_hour)))
        print("The current_Low is   :   " + str(current_Low(six_hour)))

    title = "CURRENT 6 HOUR   :   "
    if (current_Open(six_hour) == current_Low(six_hour)):
        current = "GREEN"
        print(colored(title + current, "green"))

    elif (current_Close(six_hour) > current_Open(six_hour)):
        current = "GREEN_INDECISIVE"
        print(colored(title + current, "green"))

    elif (current_Open(six_hour) == current_High(six_hour)):
        current = "RED"
        print(colored(title + current, "red"))

    elif (current_Open(six_hour) > current_Close(six_hour)):
        current = "RED_INDECISIVE"
        print(colored(title + current, "red"))

    else:
        current = "NO_MOVEMENT"
        print(colored(title + current, "yellow"))

    if (previous == "GREEN") and (current == "GREEN"): trend = "GREEN"
    elif ((previous == "GREEN_INDECISIVE") and (previous_High(six_hour) > first_High(six_hour))) and (current == "GREEN"): trend = "GREEN"
    elif (previous == "RED") and (current == "RED"): trend = "RED"
    elif ((previous == "RED_INDECISIVE") and (previous_Low(six_hour) < first_Low(six_hour))) and (current == "RED"): trend = "RED"
    else: trend = "INDECISIVE"
    return trend

def get_hour(hour): # return RED // GREEN // INDECISIVE
    title = str(hour) + " HOUR DIRECTION :   "
    if hour == 1: klines = binance_futures.KLINE_INTERVAL_1HOUR(4)
    elif hour == 2: klines = binance_futures.KLINE_INTERVAL_2HOUR(4)
    elif hour == 4: klines = binance_futures.KLINE_INTERVAL_4HOUR(4)
    elif hour == 6: klines = binance_futures.KLINE_INTERVAL_6HOUR(4)

    if troubleshooting:
        print("The current_Open is  :   " + str(current_Open(klines)))
        print("The current_Close is :   " + str(current_Close(klines)))
        print("The current_High is  :   " + str(current_High(klines)))
        print("The current_Low is   :   " + str(current_Low(klines)))

    if (current_Open(klines) == current_Low(klines)):
        current = "GREEN"
        print(colored(title + current, "green"))

    elif (current_Close(klines) > current_Open(klines)):
        current = "GREEN_INDECISIVE"
        print(colored(title + current, "yellow"))

    elif (current_Open(klines) == current_High(klines)):
        current = "RED"
        print(colored(title + current, "red"))

    elif (current_Open(klines) > current_Close(klines)):
        current = "RED_INDECISIVE"
        print(colored(title + current, "yellow"))

    else:
        current = "NO_MOVEMENT"
        print(colored(title + current, "yellow"))

    return current

def get_current_minute(minute): # return RED // GREEN // RED_INDECISIVE // GREEN_INDECISIVE // NO_MOVEMENT
    if minute == 1: klines = klines = binance_futures.KLINE_INTERVAL_1MINUTE(4)
    elif minute == 3: klines = klines = binance_futures.KLINE_INTERVAL_3MINUTE(4)
    elif minute == 5: klines = klines = binance_futures.KLINE_INTERVAL_5MINUTE(4)
    elif minute == 15: klines = binance_futures.KLINE_INTERVAL_15MINUTE(4)
    elif minute == 30: klines = binance_futures.KLINE_INTERVAL_30MINUTE(4)

    if troubleshooting:
        print("The current_Open is  :   " + str(current_Open(klines)))
        print("The current_Close is :   " + str(current_Close(klines)))
        print("The current_High is  :   " + str(current_High(klines)))
        print("The current_Low is   :   " + str(current_Low(klines)))

    if (current_Open(klines) == current_High(klines)):
        minute_candle = "RED"
        print(colored("RECENT " + str(minute) + " MINUTE  :   " + minute_candle, "red"))

    elif (current_Open(klines) == current_Low(klines)):
        minute_candle = "GREEN"
        print(colored("RECENT " + str(minute) + " MINUTE  :   " + minute_candle, "green"))

    elif (current_Open(klines) > current_Close(klines)):
        minute_candle = "RED_INDECISIVE"
        print(colored("RECENT " + str(minute) + " MINUTE  :   " + minute_candle, "red"))

    elif (current_Close(klines) > current_Open(klines)):
        minute_candle = "GREEN_INDECISIVE"
        print(colored("RECENT " + str(minute) + " MINUTE  :   " + minute_candle, "green"))

    else:
        minute_candle = "NO_MOVEMENT"
        print(colored("RECENT " + str(minute) + " MINUTE  :   " + minute_candle, "white"))

    return minute_candle

def entry_test(CANDLE, INTERVAL): # return "PASS" // "FAIL"
    if INTERVAL == "1MINUTE": klines = binance_futures.KLINE_INTERVAL_1MINUTE(4)
    elif INTERVAL == "3MINUTE": klines = binance_futures.KLINE_INTERVAL_3MINUTE(4)
    elif INTERVAL == "5MINUTE": klines = binance_futures.KLINE_INTERVAL_5MINUTE(4)
    elif INTERVAL == "15MINUTE": klines = binance_futures.KLINE_INTERVAL_15MINUTE(4)
    elif INTERVAL == "30MINUTE": klines = binance_futures.KLINE_INTERVAL_30MINUTE(4)
    elif INTERVAL == "1HOUR": klines = binance_futures.KLINE_INTERVAL_1HOUR(4)
    elif INTERVAL == "2HOUR": klines = binance_futures.KLINE_INTERVAL_2HOUR(4)
    elif INTERVAL == "4HOUR": klines = binance_futures.KLINE_INTERVAL_4HOUR(4)
    elif INTERVAL == "6HOUR": klines = binance_futures.KLINE_INTERVAL_6HOUR(4)

    if CANDLE == "GREEN":
        if (current_High(klines) > previous_High(klines)): return "PASS"
        else: return "FAIL"
    elif CANDLE == "RED":
        if (current_Low(klines) < previous_Low(klines)): return "PASS"
        else: return "FAIL"

def one_minute_exit_test(CANDLE): # return "PASS" // "FAIL"
    klines = binance_futures.KLINE_INTERVAL_1MINUTE(4)
    threshold = abs((previous_Open(klines) - previous_Close(klines)) / 4)

    if CANDLE == "GREEN":
        if (previous_High(klines) > current_High(klines)) and (current_Low(klines) < (previous_Low(klines) + threshold)): return "PASS"
        elif current_Low(klines) < previous_Low(klines): return "PASS"
        else: return "FAIL"
    elif CANDLE == "RED":
        if (current_Low(klines) > previous_Low(klines)) and (current_High(klines) > (previous_High(klines) - threshold)): return "PASS"
        elif current_High(klines) > previous_High(klines): return "PASS"
        else: return "FAIL"

def pattern_broken(INTERVAL): # return "BROKEN" // "NOT_BROKEN"
    if INTERVAL == "1MINUTE": klines = binance_futures.KLINE_INTERVAL_1MINUTE(4)
    elif INTERVAL == "3MINUTE": klines = binance_futures.KLINE_INTERVAL_3MINUTE(4)
    elif INTERVAL == "5MINUTE": klines = binance_futures.KLINE_INTERVAL_5MINUTE(4)
    elif INTERVAL == "15MINUTE": klines = binance_futures.KLINE_INTERVAL_15MINUTE(4)
    elif INTERVAL == "30MINUTE": klines = binance_futures.KLINE_INTERVAL_30MINUTE(4)
    elif INTERVAL == "1HOUR": klines = binance_futures.KLINE_INTERVAL_1HOUR(4)
    elif INTERVAL == "2HOUR": klines = binance_futures.KLINE_INTERVAL_2HOUR(4)
    elif INTERVAL == "4HOUR": klines = binance_futures.KLINE_INTERVAL_4HOUR(4)
    elif INTERVAL == "6HOUR": klines = binance_futures.KLINE_INTERVAL_6HOUR(4)

    if (first_Open(klines) == first_Low(klines)): first = "GREEN"
    elif (first_Open(klines) == first_High(klines)): first = "RED"
    else: first = "INDECISIVE"

    if (previous_Open(klines) == previous_Low(klines)): previous = "GREEN"
    elif (previous_Open(klines) == previous_High(klines)): previous = "RED"
    else: previous = "INDECISIVE"

    if (current_Open(klines) == current_Low(klines)): current = "GREEN"
    elif (current_Open(klines) == current_High(klines)): current = "RED"
    else: current = "INDECISIVE"

    if ((first == "INDECISIVE") and (previous == "INDECISIVE") and (current == "INDECISIVE")) or \
       ((first == "GREEN") and (previous == "GREEN") and (current == "INDECISIVE")) or \
       ((first == "RED") and (previous == "RED") and (current == "INDECISIVE")): return "BROKEN"
    else: return "NOT_BROKEN"
