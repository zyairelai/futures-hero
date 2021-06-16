import config, HA_previous
from termcolor import colored
troubleshooting = config.troubleshooting

# ==========================================================================================================================================================================
#                                   IDENTIFY STRENGTH - Should add size of the candle 
# ==========================================================================================================================================================================

def benchmark(high, low):
    return (high + low) / 2

def candlebody_bigger_than_previous_candle(klines):
    return candlebody(klines) > HA_previous.candlebody(klines) / 2

def direction_wick(klines):
    if candle(klines) == "GREEN" or candle(klines) == "GREEN_INDECISIVE": return float(high(klines) - close(klines))
    elif candle(klines) == "RED" or candle(klines) == "RED_INDECISIVE": return float(close(klines) - low(klines))

def is_strong(mark_price, klines):
    if candle(klines) == "GREEN" or candle(klines) == "GREEN_INDECISIVE":
        lower_wick = open(klines) - low(klines)
        if candlebody(klines) > lower_wick and mark_price > benchmark(high(klines), low(klines)): return True

    elif candle(klines) == "RED" or candle(klines) == "RED_INDECISIVE":
        upper_wick = high(klines) - open(klines)
        if candlebody(klines) > upper_wick and mark_price < benchmark(high(klines), low(klines)): return True

def heikin_ashi(mark_price, klines):
    if (candle(klines) == "GREEN" or candle(klines) == "GREEN_INDECISIVE") and is_strong(mark_price, klines) and \
        candlebody_bigger_than_previous_candle(klines) : return "GREEN"

    elif (candle(klines) == "RED" or candle(klines) == "RED_INDECISIVE") and is_strong(mark_price, klines) and \
        candlebody_bigger_than_previous_candle(klines): return "RED"

    else: return "INDECISIVE"

def candlebody_bigger_than_previous_wick(klines):
    return candlebody(klines) > HA_previous.direction_wick(klines)

def candlebody_bigger_than_current_wick(klines):
    return candlebody(klines) > direction_wick(klines)

# ==========================================================================================================================================================================
#                                                 WAR FORMATION
# ==========================================================================================================================================================================

def war_formation(mark_price, klines): # Pencil_Wick_Test    
    if candle(klines) == "GREEN" or candle(klines) == "GREEN_INDECISIVE":
        if close(klines) > previous_Close(klines) and mark_price > previous_Close(klines): return True
    elif candle(klines) == "RED" or candle(klines) == "RED_INDECISIVE":
        if close(klines) < previous_Close(klines) and mark_price < previous_Close(klines): return True

def pattern_broken(klines): # return "BROKEN" // "NOT_BROKEN"
    current  = candle(klines)
    if ((current == "GREEN" or current == "GREEN_INDECISIVE") and (firstrun_High(klines) > previous_High(klines)) and (previous_High(klines) > high(klines))) or \
       ((current == "RED"   or current == "RED_INDECISIVE")   and (firstrun_Low(klines)  < previous_Low(klines))  and (previous_Low(klines)  < low(klines))) or \
       ((current == "GREEN" or current == "GREEN_INDECISIVE") and (previous_Close(klines) > close(klines))) or \
       ((current == "RED"   or current == "RED_INDECISIVE")   and (previous_Close(klines) < close(klines))): return "BROKEN"
    else: return "NOT_BROKEN"

# ==========================================================================================================================================================================
#                                         Heikin Ashi Calculations & Candle Types
# ==========================================================================================================================================================================

def initial_Open(klines)  : return (float(klines[-4][1]) + float(klines[-4][4])) / 2
def initial_Close(klines) : return (float(klines[-4][1]) + float(klines[-4][2]) + float(klines[-4][3]) + float(klines[-4][4])) / 4

def firstrun_Open(klines) : return float((initial_Open(klines) + initial_Close(klines)) / 2)
def firstrun_Close(klines): return (float(klines[-3][1]) + float(klines[-3][2]) + float(klines[-3][3]) + float(klines[-3][4])) / 4
def firstrun_High(klines) : return max(float(klines[-3][2]), firstrun_Open(klines), firstrun_Close(klines))
def firstrun_Low(klines)  : return min(float(klines[-3][3]), firstrun_Open(klines), firstrun_Close(klines))

def previous_Open(klines) : return float((firstrun_Open(klines) + firstrun_Close(klines)) / 2)
def previous_Close(klines): return (float(klines[-2][1]) + float(klines[-2][2]) + float(klines[-2][3]) + float(klines[-2][4])) / 4
def previous_High(klines) : return max(float(klines[-2][2]), previous_Open(klines), previous_Close(klines))
def previous_Low(klines)  : return min(float(klines[-2][3]), previous_Open(klines), previous_Close(klines))

def open(klines)  : return float((previous_Open(klines) + previous_Close(klines)) / 2)
def close(klines) : return (float(klines[-1][1]) + float(klines[-1][2]) + float(klines[-1][3]) + float(klines[-1][4])) / 4
def high(klines)  : return max(float(klines[-1][2]), open(klines), close(klines))
def low(klines)   : return min(float(klines[-1][3]), open(klines), close(klines))

def candle(klines):
    if   (open(klines) == high(klines)): return "RED"
    elif (open(klines) == low(klines)) : return "GREEN"
    elif (open(klines) > close(klines)): return "RED_INDECISIVE"
    elif (close(klines) > open(klines)): return "GREEN_INDECISIVE"
    else: return "NO_MOVEMENT"

def candlebody(klines) : return float(abs(open(klines) - close(klines)))
def candle_size(klines): return float(abs(candlebody(klines) / open(klines) * 100))

def output(mark_price, klines): # return GREEN // GREEN_INDECISIVE // RED // RED_INDECISIVE // NO_MOVEMENT
    if troubleshooting:
        print("The current_Open  is :   " + str(open(klines)))
        print("The current_Close is :   " + str(close(klines)))
        print("The current_High  is :   " + str(high(klines)))
        print("The current_Low   is :   " + str(low(klines)))

    milliseconds = int(klines[-1][0]) - int(klines[-2][0])
    if milliseconds == 1 * 60000: interval = "1 MINUTE  "
    elif milliseconds == 3 * 60000: interval = "3 MINUTE  "
    elif milliseconds == 5 * 60000: interval = "5 MINUTE  "
    elif milliseconds == 15 * 60000: interval = "15 MINUTE "
    elif milliseconds == 30 * 60000: interval = "30 MINUTE "
    elif milliseconds == 1 * 60 * 60000: interval = "1 HOUR    "
    elif milliseconds == 2 * 60 * 60000: interval = "2 HOUR    "
    elif milliseconds == 4 * 60 * 60000: interval = "4 HOUR    "
    elif milliseconds == 6 * 60 * 60000: interval = "6 HOUR    "
    elif milliseconds == 12 * 60 * 60000: interval = "12 HOUR   "

    current = candle(klines)
    if is_strong(mark_price, klines): strength = "STRONG"
    else: strength = "WEAK"
    if   current == "GREEN" or current == "GREEN_INDECISIVE": print(colored("RECENT " + interval + ":   " + strength + " " + current, "green"))
    elif current == "RED"   or current == "RED_INDECISIVE"  : print(colored("RECENT " + interval + ":   " + strength + " " + current, "red"))
    else: print(colored("RECENT " + interval + ":   " + strength + " " + current, "yellow"))
    return current

def closing_price_list(klines):
    closing_price_list = []
    for candle in range(len(klines)):
        closing_price_list.append(float(klines[candle][4]))
    return closing_price_list
