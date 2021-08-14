from termcolor import colored

def previous_open(klines) : return float(klines[-2][1])
def previous_high(klines) : return float(klines[-2][2])
def previous_low(klines)  : return float(klines[-2][3])
def previous_close(klines): return float(klines[-2][4])
def current_open(klines)  : return float(klines[-1][1])
def current_high(klines)  : return float(klines[-1][2])
def current_low(klines)   : return float(klines[-1][3])
def current_close(klines) : return float(klines[-1][4])
def candle_body(klines)   : return abs(current_open(klines) - current_close(klines))
def candle_wick(klines)   : return current_high(klines) - current_low(klines) - candle_body(klines)
def timestamp_of(kline): return kline[-1][0]

def closing_price_list(klines):
    closing_price_list = []
    for candle in range(len(klines)):
        closing_price_list.append(float(klines[candle][4]))
    return closing_price_list

def candle_color(klines):
    if current_close(klines) > current_open(klines): return "GREEN"
    elif current_close(klines) < current_open(klines): return "RED"
    else: return "INDECISIVE"

def upper_wick(klines):
    if candle_color(klines) == "GREEN": return current_high(klines) - current_close(klines)
    elif candle_color(klines) == "RED": return current_high(klines) - current_open(klines)
    else: return 0

def lower_wick(klines):
    if candle_color(klines) == "GREEN": return current_open(klines)  - current_low(klines)
    elif candle_color(klines) == "RED": return current_close(klines) - current_low(klines)
    else: return 0

def strong_candle(klines):
    if candle_body(klines) > candle_wick(klines): return True
    else:
        if candle_color(klines) == "GREEN" and current_close(klines) > previous_high(klines): return True
        elif candle_color(klines) == "RED" and current_close(klines) < previous_low(klines): return True

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
