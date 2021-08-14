from termcolor import colored

def candle_body(klines)   : return float(abs(open(klines) - close(klines)))
def candle_size(klines)   : return float(abs(candle_body(klines) / open(klines) * 100))

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

def upper_wick(klines):
    if candle(klines) == "GREEN" or candle(klines) == "GREEN_INDECISIVE": return float(high(klines) - close(klines))
    elif candle(klines) == "RED" or candle(klines) == "RED_INDECISIVE": return float(high(klines) - open(klines))

def lower_wick(klines):
    if candle(klines) == "GREEN" or candle(klines) == "GREEN_INDECISIVE": return float(open(klines) - low(klines))
    elif candle(klines) == "RED" or candle(klines) == "RED_INDECISIVE": return float(close(klines) - low(klines))

def absolute_indecisive(klines):
    if candle_body(klines) < upper_wick(klines) and candle_body(klines) < lower_wick(klines) : return True

def candle(klines):
    if   (open(klines) == high(klines)): return "RED"
    elif (open(klines) == low(klines)) : return "GREEN"
    elif (open(klines) > close(klines)): return "RED_INDECISIVE"
    elif (close(klines) > open(klines)): return "GREEN_INDECISIVE"
    else: return "NO_MOVEMENT"

def VALID_CANDLE(klines):
    if (candle(klines) == "GREEN" or candle(klines) == "GREEN_INDECISIVE") and candle_body(klines) > lower_wick(klines): return "GREEN"
    elif (candle(klines) == "RED" or candle(klines) == "RED_INDECISIVE") and candle_body(klines) > upper_wick(klines): return "RED"

def output(klines): # return GREEN // GREEN_INDECISIVE // RED // RED_INDECISIVE // NO_MOVEMENT
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
    if   current == "GREEN" or current == "GREEN_INDECISIVE": print(colored("HEIKIN " + interval + ":   " + current, "green"))
    elif current == "RED"   or current == "RED_INDECISIVE"  : print(colored("HEIKIN " + interval + ":   " + current, "red"))
    else: print(colored("RECENT " + interval + ":   " + " " + current, "yellow"))
    return current

def war_formation(klines): # Pencil_Wick_Test    
    if candle(klines) == "GREEN" or candle(klines) == "GREEN_INDECISIVE":
        if close(klines) > previous_Close(klines) and high(klines) > previous_High(klines): return True
    elif candle(klines) == "RED" or candle(klines) == "RED_INDECISIVE":
        if close(klines) < previous_Close(klines) and high(klines) < previous_High(klines): return True
