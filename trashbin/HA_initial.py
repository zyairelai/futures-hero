import config
from termcolor import colored
troubleshooting = config.troubleshooting

# ==========================================================================================================================================================================
#                                         Heikin Ashi Calculations & Candle Types
# ==========================================================================================================================================================================

def initial_Open(klines)  : return (float(klines[-4][1]) + float(klines[-4][4])) / 2
def initial_Close(klines) : return (float(klines[-4][1]) + float(klines[-4][2]) + float(klines[-4][3]) + float(klines[-4][4])) / 4
def Open(klines)          : return float((initial_Open(klines) + initial_Close(klines)) / 2)
def Close(klines)         : return (float(klines[-3][1]) + float(klines[-3][2]) + float(klines[-3][3]) + float(klines[-3][4])) / 4
def High(klines)          : return max(float(klines[-3][2]), Open(klines), Close(klines))
def Low(klines)           : return min(float(klines[-3][3]), Open(klines), Close(klines))
def candlebody(klines)    : return abs(Open(klines) - Close(klines))

def firstrun_candle(klines):
    if   (Open(klines) == High(klines)): return "RED"
    elif (Open(klines) == Low(klines)) : return "GREEN"
    elif (Open(klines) > Close(klines)): return "RED_INDECISIVE"
    elif (Close(klines) > Open(klines)): return "GREEN_INDECISIVE"
    else: return "NO_MOVEMENT"

def output(klines): # return GREEN // GREEN_INDECISIVE // RED // RED_INDECISIVE // NO_MOVEMENT
    if troubleshooting:
        print("The firstrun_Open  is :   " + str(Open(klines)))
        print("The firstrun_Close is :   " + str(Close(klines)))
        print("The firstrun_High  is :   " + str(High(klines)))
        print("The firstrun_Low   is :   " + str(Low(klines)))

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

    firstrun = firstrun_candle(klines)
    if   firstrun == "GREEN" or firstrun == "GREEN_INDECISIVE": print(colored("FIRSTRUN " + interval + ":   " + firstrun, "green"))
    elif firstrun == "RED"   or firstrun == "RED_INDECISIVE"  : print(colored("FIRSTRUN " + interval + ":   " + firstrun, "red"))
    else: print(colored("RECENT " + interval + ":   " + firstrun, "yellow"))
    return firstrun
