import config
from termcolor import colored
troubleshooting = config.troubleshooting

# ==========================================================================================================================================================================
#                                                 IDENTIFY STRENGTH
# ==========================================================================================================================================================================

def direction_wick(klines):
    if candle(klines) == "GREEN" or candle(klines) == "GREEN_INDECISIVE": return float(high(klines) - close(klines))
    elif candle(klines) == "RED" or candle(klines) == "RED_INDECISIVE": return float(close(klines) - low(klines))

def is_strong(klines):
    if candle(klines) == "GREEN" or candle(klines) == "GREEN_INDECISIVE":
        lower_wick = open(klines) - low(klines)
        if candlebody(klines) > lower_wick: return True

    elif candle(klines) == "RED" or candle(klines) == "RED_INDECISIVE":
        upper_wick = high(klines) - open(klines)
        if candlebody(klines) > upper_wick: return True

# ==========================================================================================================================================================================
#                                              Heikin Ashi Calculations
# ==========================================================================================================================================================================

def initial_Open(klines)  : return (float(klines[-4][1]) + float(klines[-4][4])) / 2
def initial_Close(klines) : return (float(klines[-4][1]) + float(klines[-4][2]) + float(klines[-4][3]) + float(klines[-4][4])) / 4
def firstrun_Open(klines) : return float((initial_Open(klines) + initial_Close(klines)) / 2)
def firstrun_Close(klines): return (float(klines[-3][1]) + float(klines[-3][2]) + float(klines[-3][3]) + float(klines[-3][4])) / 4
def firstrun_High(klines) : return max(float(klines[-3][2]), firstrun_Open(klines), firstrun_Close(klines))
def firstrun_Low(klines)  : return min(float(klines[-3][3]), firstrun_Open(klines), firstrun_Close(klines))
def open(klines) : return float((firstrun_Open(klines) + firstrun_Close(klines)) / 2)
def close(klines): return (float(klines[-2][1]) + float(klines[-2][2]) + float(klines[-2][3]) + float(klines[-2][4])) / 4
def high(klines) : return max(float(klines[-2][2]), open(klines), close(klines))
def low(klines)  : return min(float(klines[-2][3]), open(klines), close(klines))
def candlebody(klines): return abs(open(klines) - close(klines))

def candle(klines):
    if   (open(klines) == high(klines)): return "RED"
    elif (open(klines) == low(klines)) : return "GREEN"
    elif (open(klines) > close(klines)): return "RED_INDECISIVE"
    elif (close(klines) > open(klines)): return "GREEN_INDECISIVE"
    else: return "NO_MOVEMENT"

def output(klines): # return GREEN // GREEN_INDECISIVE // RED // RED_INDECISIVE // NO_MOVEMENT
    if troubleshooting:
        print("The previous_Open  is :   " + str(open(klines)))
        print("The previous_Close is :   " + str(close(klines)))
        print("The previous_High  is :   " + str(high(klines)))
        print("The previous_Low   is :   " + str(low(klines)))

    milliseconds = int(klines[-1][0]) - int(klines[-2][0])
    if milliseconds == 1 * 60000: interval = "1 MINUTE"
    elif milliseconds == 3 * 60000: interval = "3 MINUTE"
    elif milliseconds == 5 * 60000: interval = "5 MINUTE"
    elif milliseconds == 15 * 60000: interval = "15 MIN  "
    elif milliseconds == 30 * 60000: interval = "30 MIN  "
    elif milliseconds == 1 * 60 * 60000: interval = "1 HOUR  "
    elif milliseconds == 2 * 60 * 60000: interval = "2 HOUR  "
    elif milliseconds == 4 * 60 * 60000: interval = "4 HOUR  "
    elif milliseconds == 6 * 60 * 60000: interval = "6 HOUR  "
    elif milliseconds == 12 * 60 * 60000: interval = "12 HOUR "

    previous = candle(klines)
    if is_strong(klines): strength = "STRONG"
    else: strength = "WEAK"
    if   previous == "GREEN" or previous == "GREEN_INDECISIVE": print(colored("PREVIOUS " + interval + ":   " + strength + " " + previous, "green"))
    elif previous == "RED"   or previous == "RED_INDECISIVE"  : print(colored("PREVIOUS " + interval + ":   " + strength + " " + previous, "red"))
    else: print(colored("RECENT " + interval + ":   " + strength + " " + previous, "yellow"))
    return previous
