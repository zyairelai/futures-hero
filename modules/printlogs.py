from termcolor import colored

def candlestick(candlestick):
    milliseconds = int(candlestick['timestamp'].iloc[1]) - int(candlestick['timestamp'].iloc[0])
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

    strength = "STRONG " if candlestick["strong"].iloc[-1] else "WEAK "
    if   candlestick['color'].iloc[-1] == "GREEN": print(colored("CANDLE " + interval + ":   " + strength + str(candlestick['color'].iloc[-1]), "green"))
    elif candlestick['color'].iloc[-1] == "RED"  : print(colored("CANDLE " + interval + ":   " + strength + str(candlestick['color'].iloc[-1]), "red"))
    else: print(colored("CANDLE " + interval + ":   " + str(candlestick['color'].iloc[-1]), "yellow"))

def heikin_ashi(HA):
    milliseconds = HA['timestamp'].iloc[-1] - HA['timestamp'].iloc[-2]
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

    current = HA['candle_type'].iloc[-1]
    if   current == "GREEN" or current == "GREEN_INDECISIVE": print(colored("HEIKIN " + interval + ":   " + current, "green"))
    elif current == "RED"   or current == "RED_INDECISIVE"  : print(colored("HEIKIN " + interval + ":   " + current, "red"))
    else: print(colored("RECENT " + interval + ":   " + current, "yellow"))
