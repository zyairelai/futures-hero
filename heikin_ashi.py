import config
import binance_futures
from datetime import datetime
from termcolor import colored
troubleshooting = config.troubleshooting

# ==========================================================================================================================================================================
#                                              Heikin Ashi Calculations & Candle Types
# ==========================================================================================================================================================================
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
# ==========================================================================================================================================================================
#                                                        Retrieve HOUR and MINUTE
# ==========================================================================================================================================================================
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
    else: print(colored(title + current, "yellow"))
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
    else: print(colored(title + minute_candle, "yellow"))
    return minute_candle
# ==========================================================================================================================================================================
#                                                             WAR FORMATION
# ==========================================================================================================================================================================
def pencil_wick_test(CANDLE):
    klines = binance_futures.KLINE_INTERVAL_1MINUTE()
    previous_volume = binance_futures.get_volume("PREVIOUS", "1MINUTE")
    current_volume  = binance_futures.get_volume("CURRENT",  "1MINUTE")
    volume_confirmation = (current_volume > (previous_volume / 2))

    if CANDLE == "GREEN":
        if  current_High(klines)  > previous_High(klines)  and \
            current_Close(klines) > previous_Close(klines) and \
            volume_confirmation: 
            return True
    elif CANDLE == "RED":
        if  current_Low(klines)   < previous_Low(klines)   and \
            current_Close(klines) < previous_Close(klines) and \
            volume_confirmation:
                return True

def one_minute_exit_test(POSITION):
    klines = binance_futures.KLINE_INTERVAL_1MINUTE()
    if POSITION == "LONG":
        if (previous_Close(klines) > current_High(klines)) or (previous_Close(klines) > current_Close(klines)): return True
    elif POSITION == "SHORT":
        if (previous_Close(klines) < current_Low(klines)) or (previous_Close(klines) < current_Close(klines)): return True
# ==========================================================================================================================================================================
#                                                          IDENTIFY STRENGTH
# ==========================================================================================================================================================================
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

    current  = current_candle(klines)
    if ((current == "GREEN" or current == "GREEN_INDECISIVE") and (first_High(klines) > previous_High(klines)) and (previous_High(klines) > current_High(klines))) or \
       ((current == "RED"   or current == "RED_INDECISIVE")   and (first_Low(klines)  < previous_Low(klines))  and (previous_Low(klines)  < current_Low(klines))) or \
       ((current == "GREEN" or current == "GREEN_INDECISIVE") and (previous_Close(klines) > current_Close(klines))) or \
       ((current == "RED"   or current == "RED_INDECISIVE")   and (previous_Close(klines) < current_Close(klines))): return "BROKEN"
    else: return "NOT_BROKEN"

def strength_of(INTERVAL):
    if   INTERVAL == "1MINUTE" : klines = binance_futures.KLINE_INTERVAL_1MINUTE()
    elif INTERVAL == "1HOUR"   : klines = binance_futures.KLINE_INTERVAL_1HOUR()
    elif INTERVAL == "6HOUR"   : klines = binance_futures.KLINE_INTERVAL_6HOUR()

    previous = previous_candle(klines)
    current = current_candle(klines)

    open  = current_Open(klines)
    close = current_Close(klines)
    high  = current_High(klines)
    low   = current_Low(klines)

    if current == "GREEN": 
        upper_wick = high - close
        candlebody = close - open
        if upper_wick > candlebody: strength = "WEAK"
        else: strength = "STRONG"

    elif current == "RED":
        lower_wick = close - low
        candlebody = open - close
        if lower_wick > candlebody: strength = "WEAK"
        else: strength = "STRONG"
    
    elif current == "GREEN_INDECISIVE":
        upper_wick = high - close
        lower_wick = open - low
        candlebody = close - open
        if candlebody > lower_wick:
            if previous == "GREEN": strength = "WEAK"
            else: strength = "STRONG"
        else:
            if  high  > previous_High(klines)  and \
                close > previous_Close(klines) and \
                open  > previous_Open(klines)  and \
                low   > previous_Low(klines): strength = "STRONG"
            else: strength = "WEAK"

    elif current == "RED_INDECISIVE":
        upper_wick = high - open
        lower_wick = close - low
        candlebody = open - close
        if candlebody > upper_wick:
            if previous == "RED": strength = "WEAK"
            else: strength = "STRONG"
        else:
            if  high  < previous_High(klines)  and \
                close < previous_Close(klines) and \
                open  < previous_Open(klines)  and \
                low   < previous_Low(klines): strength = "STRONG"
            else: strength = "WEAK"
    return strength
