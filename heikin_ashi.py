import config
import binance_futures
from datetime import datetime
from termcolor import colored
troubleshooting = config.troubleshooting

def initial_Open(klines)  : return (float(klines[-4][1]) + float(klines[-4][4])) / 2
def initial_Close(klines) : return (float(klines[-4][1]) + float(klines[-4][2]) + float(klines[-4][3]) + float(klines[-4][4])) / 4

def first_Open(klines)    : return (initial_Open(klines) + initial_Close(klines)) / 2
def first_Close(klines)   : return (float(klines[-3][1]) + float(klines[-3][2]) + float(klines[-3][3]) + float(klines[-3][4])) / 4
def first_High(klines)    : return max(float(klines[-3][2]), first_Open(klines), first_Close(klines))
def first_Low(klines)     : return min(float(klines[-3][3]), first_Open(klines), first_Close(klines))

def previous_Open(klines) : return (first_Open(klines) + first_Close(klines)) / 2
def previous_Close(klines): return (float(klines[-2][1]) + float(klines[-2][2]) + float(klines[-2][3]) + float(klines[-2][4])) / 4
def previous_High(klines) : return max(float(klines[-2][2]), previous_Open(klines), previous_Close(klines))
def previous_Low(klines)  : return min(float(klines[-2][3]), previous_Open(klines), previous_Close(klines))

def current_Open(klines)  : return (previous_Open(klines) + previous_Close(klines)) / 2
def current_Close(klines) : return (float(klines[-1][1]) + float(klines[-1][2]) + float(klines[-1][3]) + float(klines[-1][4])) / 4
def current_High(klines)  : return max(float(klines[-1][2]), current_Open(klines), current_Close(klines))
def current_Low(klines)   : return min(float(klines[-1][3]), current_Open(klines), current_Close(klines))

def first_candle(klines):
    if   (first_Open(klines) == first_High(klines)): return "RED"
    elif (first_Open(klines) == first_Low(klines)) : return "GREEN"
    elif (first_Open(klines) > first_Close(klines)): return "RED_INDECISIVE"
    elif (first_Close(klines) > first_Open(klines)): return "GREEN_INDECISIVE"
    else: return "NO_MOVEMENT"

def previous_candle(klines):
    if   (previous_Open(klines) == previous_High(klines)): return "RED"
    elif (previous_Open(klines) == previous_Low(klines)) : return "GREEN"
    elif (previous_Open(klines) > previous_Close(klines)): return "RED_INDECISIVE"
    elif (previous_Close(klines) > previous_Open(klines)): return "GREEN_INDECISIVE"
    else: return "NO_MOVEMENT"

def current_candle(klines):
    if   (current_Open(klines) == current_High(klines)): return "RED"
    elif (current_Open(klines) == current_Low(klines)) : return "GREEN"
    elif (current_Open(klines) > current_Close(klines)): return "RED_INDECISIVE"
    elif (current_Close(klines) > current_Open(klines)): return "GREEN_INDECISIVE"
    else: return "NO_MOVEMENT"

def get_hour(hour): # return GREEN // GREEN_INDECISIVE // RED // RED_INDECISIVE // NO_MOVEMENT
    title = str(hour) + " HOUR DIRECTION :   "
    if   hour == 1: klines = binance_futures.KLINE_INTERVAL_1HOUR()
    elif hour == 2: klines = binance_futures.KLINE_INTERVAL_2HOUR()
    elif hour == 4: klines = binance_futures.KLINE_INTERVAL_4HOUR()
    elif hour == 6: klines = binance_futures.KLINE_INTERVAL_6HOUR()

    if troubleshooting:
        print("The current_Open is  :   " + str(current_Open(klines)))
        print("The current_Close is :   " + str(current_Close(klines)))
        print("The current_High is  :   " + str(current_High(klines)))
        print("The current_Low is   :   " + str(current_Low(klines)))

    current = current_candle(klines)
    if   current == "GREEN"             : print(colored(title + current, "green"))
    elif current == "GREEN_INDECISIVE"  : print(colored(title + current, "green"))
    elif current == "RED"               : print(colored(title + current, "red"))
    elif current == "RED_INDECISIVE"    : print(colored(title + current, "red"))
    else                                : print(colored(title + current, "yellow"))
    return current

def get_current_minute(minute): # return GREEN // GREEN_INDECISIVE // RED // RED_INDECISIVE // NO_MOVEMENT
    title = "RECENT " + str(minute) + " MINUTE  :   "
    if   minute == 1: klines = binance_futures.KLINE_INTERVAL_1MINUTE()
    elif minute == 3: klines  = binance_futures.KLINE_INTERVAL_3MINUTE()
    elif minute == 5: klines  = binance_futures.KLINE_INTERVAL_5MINUTE()
    elif minute == 15: klines = binance_futures.KLINE_INTERVAL_15MINUTE()
    elif minute == 30: klines = binance_futures.KLINE_INTERVAL_30MINUTE()

    if troubleshooting:
        print("The current_Open is  :   " + str(current_Open(klines)))
        print("The current_Close is :   " + str(current_Close(klines)))
        print("The current_High is  :   " + str(current_High(klines)))
        print("The current_Low is   :   " + str(current_Low(klines)))

    minute_candle = current_candle(klines)
    if   minute_candle == "GREEN"            :   print(colored(title + minute_candle, "green"))
    elif minute_candle == "GREEN_INDECISIVE" :   print(colored(title + minute_candle, "green"))
    elif minute_candle == "RED"              :   print(colored(title + minute_candle, "red"))
    elif minute_candle == "RED_INDECISIVE"   :   print(colored(title + minute_candle, "red"))
    else                                     :   print(colored(title + minute_candle, "yellow"))
    return minute_candle

def one_minute_exit_test(CANDLE): # return "PASS" // "FAIL"
    klines = binance_futures.KLINE_INTERVAL_1MINUTE()
    threshold = abs((previous_Open(klines) - previous_Close(klines)) / 4)

    if CANDLE == "GREEN":
        if (previous_Close(klines) > current_High(klines)) or \
          ((previous_High(klines) > current_High(klines)) and (current_Low(klines) < (previous_Low(klines) + threshold))): return True
    elif CANDLE == "RED":
        if (previous_Close(klines) < current_Low(klines)) or \
          ((current_Low(klines) > previous_Low(klines)) and (current_High(klines) > (previous_High(klines) - threshold))): return True

def pencil_wick_test(CANDLE, INTERVAL): # return "PASS" // "FAIL"
    if   INTERVAL == "1MINUTE" : klines = binance_futures.KLINE_INTERVAL_1MINUTE()
    elif INTERVAL == "3MINUTE" : klines = binance_futures.KLINE_INTERVAL_3MINUTE()
    elif INTERVAL == "5MINUTE" : klines = binance_futures.KLINE_INTERVAL_5MINUTE()
    elif INTERVAL == "15MINUTE": klines = binance_futures.KLINE_INTERVAL_15MINUTE()
    elif INTERVAL == "30MINUTE": klines = binance_futures.KLINE_INTERVAL_30MINUTE()
    elif INTERVAL == "1HOUR"   : klines = binance_futures.KLINE_INTERVAL_1HOUR()
    elif INTERVAL == "2HOUR"   : klines = binance_futures.KLINE_INTERVAL_2HOUR()
    elif INTERVAL == "4HOUR"   : klines = binance_futures.KLINE_INTERVAL_4HOUR()
    elif INTERVAL == "6HOUR"   : klines = binance_futures.KLINE_INTERVAL_6HOUR()

    if CANDLE == "GREEN":
        # if (current_Close(klines) > previous_Close(klines)): return "PASS"
        if (current_Close(klines) > previous_High(klines)): return "PASS"
        else: return "FAIL"
    elif CANDLE == "RED":
        # if (current_Close(klines) < previous_Close(klines)): return "PASS"
        if (current_Low(klines) < previous_Low(klines)): return "PASS"
        else: return "FAIL"

def pattern_broken(INTERVAL): # return "BROKEN" // "NOT_BROKEN"
    if   INTERVAL == "1MINUTE" : klines = binance_futures.KLINE_INTERVAL_1MINUTE()
    elif INTERVAL == "3MINUTE" : klines = binance_futures.KLINE_INTERVAL_3MINUTE()
    elif INTERVAL == "5MINUTE" : klines = binance_futures.KLINE_INTERVAL_5MINUTE()
    elif INTERVAL == "15MINUTE": klines = binance_futures.KLINE_INTERVAL_15MINUTE()
    elif INTERVAL == "30MINUTE": klines = binance_futures.KLINE_INTERVAL_30MINUTE()
    elif INTERVAL == "1HOUR"   : klines = binance_futures.KLINE_INTERVAL_1HOUR()
    elif INTERVAL == "2HOUR"   : klines = binance_futures.KLINE_INTERVAL_2HOUR()
    elif INTERVAL == "4HOUR"   : klines = binance_futures.KLINE_INTERVAL_4HOUR()
    elif INTERVAL == "6HOUR"   : klines = binance_futures.KLINE_INTERVAL_6HOUR()

    if   (first_Open(klines) == first_Low(klines)) : first = "GREEN"
    elif (first_Open(klines) == first_High(klines)): first = "RED"
    else: first = "INDECISIVE"

    if   (previous_Open(klines) == previous_Low(klines)) : previous = "GREEN"
    elif (previous_Open(klines) == previous_High(klines)): previous = "RED"
    else: previous = "INDECISIVE"

    if   (current_Open(klines) == current_Low(klines)) : current = "GREEN"
    elif (current_Open(klines) == current_High(klines)): current = "RED"
    else: current = "INDECISIVE"

    if ((first == "INDECISIVE") and (previous == "INDECISIVE") and (current == "INDECISIVE")) or \
       ((first == "GREEN")      and (previous == "GREEN")      and (current == "INDECISIVE")) or \
       ((first == "RED")        and (previous == "RED")        and (current == "INDECISIVE")) or \
       ((current == "GREEN")    and (first_High(klines) > previous_High(klines)) and (previous_High(klines) < current_Close(klines))) or \
       ((current == "RED")      and (first_Low(klines) < previous_Low(klines))   and (previous_Low(klines) > current_Close(klines))) or \
       ((current == "GREEN")    and (current_Close(klines) < previous_Close(klines))) or \
       ((current == "RED")      and (current_Close(klines) > previous_Close(klines))): return "BROKEN"
    else: return "NOT_BROKEN"
