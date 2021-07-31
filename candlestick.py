import heikin_ashi
from termcolor import colored

def open(klines)  : return float(klines[-1][1])
def high(klines)  : return float(klines[-1][2])
def low(klines)   : return float(klines[-1][3])
def close(klines) : return float(klines[-1][4])
def timestamp_of(kline): return kline[-1][0]
def candle_body(klines): return abs(open(klines) - close(klines))

def candle_color(klines):
    if close(klines) > open(klines): return "GREEN"
    elif close(klines) < open(klines): return "RED"
    else: return "INDECISIVE"

def upper_wick(klines):
    if candle_color(klines) == "GREEN": return high(klines) - close(klines)
    elif candle_color(klines) == "RED": return high(klines) - open(klines)
    else: return 0

def lower_wick(klines):
    if candle_color(klines) == "GREEN": return open(klines) - low(klines)
    elif candle_color(klines) == "RED": return close(klines) - low(klines)
    else: return 0

def strong_candle(klines):
    if candle_body(klines) > upper_wick(klines) + lower_wick(klines): return True

def output(klines):
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

    candle = candle_color(klines)
    if strong_candle(klines): strength = "STRONG "
    else: strength = "WEAK "

    if   candle == "GREEN" or candle == "GREEN_INDECISIVE": print(colored("CANDLE " + interval + ":   " + strength + candle, "green"))
    elif candle == "RED"   or candle == "RED_INDECISIVE"  : print(colored("CANDLE " + interval + ":   " + strength + candle, "red"))
    else: print(colored("CANDLE " + interval + ":   " + candle, "yellow"))
    return candle

def hybrid(klines):
    if candle_color(klines) == "GREEN" and strong_candle(klines) and heikin_ashi.VALID_CANDLE(klines) == "GREEN": return "GREEN"
    elif candle_color(klines) == "RED" and strong_candle(klines) and heikin_ashi.VALID_CANDLE(klines) == "RED" : return "RED"

def both_candle(klines):
    if candle_color(klines) == "GREEN" and heikin_ashi.VALID_CANDLE(klines) == "GREEN": return "GREEN"
    elif candle_color(klines) == "RED" and heikin_ashi.VALID_CANDLE(klines) == "RED" : return "RED"
