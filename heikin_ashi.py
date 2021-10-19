from termcolor import colored
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
def current_open(klines)  : return float((previous_Open(klines) + previous_Close(klines)) / 2)
def current_close(klines) : return (float(klines[-1][1]) + float(klines[-1][2]) + float(klines[-1][3]) + float(klines[-1][4])) / 4
def current_high(klines)  : return max(float(klines[-1][2]), current_open(klines), current_close(klines))
def current_low(klines)   : return min(float(klines[-1][3]), current_open(klines), current_close(klines))
def candle_body(klines)   : return float(abs(current_open(klines) - current_close(klines)))
def candle_size(klines)   : return float(abs(candle_body(klines) / current_open(klines) * 100))

def upper_wick(klines):
    if candle(klines) == "GREEN" or candle(klines) == "GREEN_INDECISIVE": return float(current_high(klines) - current_close(klines))
    elif candle(klines) == "RED" or candle(klines) == "RED_INDECISIVE": return float(current_high(klines) - current_open(klines))

def lower_wick(klines):
    if candle(klines) == "GREEN" or candle(klines) == "GREEN_INDECISIVE": return float(current_open(klines) - current_low(klines))
    elif candle(klines) == "RED" or candle(klines) == "RED_INDECISIVE": return float(current_close(klines) - current_low(klines))

def absolute_indecisive(klines):
    return True if upper_wick(klines) > candle_body(klines) and lower_wick(klines) > candle_body(klines) else False

def candle(klines):
    if   (current_open(klines) == current_high(klines)): return "RED"
    elif (current_open(klines) == current_low(klines)) : return "GREEN"
    elif (current_open(klines) > current_close(klines)): return "RED_INDECISIVE"
    elif (current_close(klines) > current_open(klines)): return "GREEN_INDECISIVE"
    else: return "NO_MOVEMENT"

def color(klines):
    if not absolute_indecisive(klines):
        if candle(klines) == "GREEN" or candle(klines) == "GREEN_INDECISIVE": return "GREEN"
        elif candle(klines) == "RED" or candle(klines) == "RED": return "RED"
    else: return "INDECISIVE"

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

def VALID_CANDLE(klines):
    if not absolute_indecisive(klines):
        if (candle(klines) == "GREEN" or candle(klines) == "GREEN_INDECISIVE") and \
            current_close(klines) > previous_Close(klines) and current_close(klines) > previous_Open(klines): return "GREEN"
        elif (candle(klines) == "RED" or candle(klines) == "RED_INDECISIVE") and \
            current_close(klines) < previous_Close(klines) and current_close(klines) < previous_Open(klines): return "RED"

def war_formation(klines): # Pencil_Wick_Test
    if candle(klines) == "GREEN" or candle(klines) == "GREEN_INDECISIVE":
        if current_close(klines) > previous_Close(klines) and current_high(klines) > previous_High(klines): return True
    elif candle(klines) == "RED" or candle(klines) == "RED_INDECISIVE":
        if current_close(klines) < previous_Close(klines) and current_high(klines) < previous_High(klines): return True
