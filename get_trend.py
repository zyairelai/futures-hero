import config
from keys import client
from binance.client import Client
from termcolor import colored

def get_current_trend(): # >>> "UP_TREND" // "DOWN_TREND" // "NO_TRADE_ZONE"
    main_direction  = get_4_hour()      # get_4_hour() // get_6_hour()
    recent_minute   = get_30_minute()   # get_15_minute() // get_30_minute() // get_1_hour()
    recent3min      = get_3_minute()
    recent5min      = get_5_minute()
    recent15min     = get_15_minute()

    if (main_direction == "UP") and (recent_minute == "UP"):
        print(colored("CURRENT TREND    :   UP_TREND", "green"))
        if (recent3min == "UP") and (recent5min == "UP") and (recent15min == "UP"): trend = "UP_TREND"
        else: trend = "COOLDOWN"
    elif (main_direction == "DOWN") and (recent_minute == "DOWN"):
        print(colored("CURRENT TREND    :   DOWN_TREND", "red"))
        if (recent3min == "DOWN") and (recent5min == "DOWN") and (recent15min == "DOWN"): trend = "DOWN_TREND"
        else: trend = "COOLDOWN"
    else:
        trend = "NO_TRADE_ZONE"
        print(colored("CURRENT TREND    :   NO_TRADE_ZONE", "yellow"))
    return trend

def heikin_ashi(klines):
    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)
    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)
    if (current_Open == current_Low): trend = "UP"
    elif (current_Open == current_High): trend = "DOWN"
    else: trend = "INDECISIVE"
    return trend

def get_3_minute(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_3MINUTE , limit=3)
    heikin_ashi_candle = heikin_ashi(klines)
    # if heikin_ashi_candle == "UP": print("recent 3 minute  :   🥦")
    # elif heikin_ashi_candle == "DOWN": print("recent 3 minute  :   🩸")
    # else: print("recent 3 minute  :   😴")
    return heikin_ashi_candle

def get_5_minute(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_5MINUTE , limit=3)
    heikin_ashi_candle = heikin_ashi(klines)
    if heikin_ashi_candle == "UP": print("recent 5 minute  :   🥦")
    elif heikin_ashi_candle == "DOWN": print("recent 5 minute  :   🩸")
    else: print("recent 5 minute  :   😴")
    return heikin_ashi_candle

def get_15_minute(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_15MINUTE , limit=3)
    heikin_ashi_candle = heikin_ashi(klines)
    if heikin_ashi_candle == "UP": print("recent 15 minute :   🥦")
    elif heikin_ashi_candle == "DOWN": print("recent 15 minute :   🩸")
    else: print("recent 15 minute :   😴")
    return heikin_ashi_candle

def get_30_minute(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_15MINUTE , limit=3)
    heikin_ashi_candle = heikin_ashi(klines)
    if heikin_ashi_candle == "UP": print("recent 30 minute :   🥦🥦")
    elif heikin_ashi_candle == "DOWN": print("recent 30 minute :   🩸🩸")
    else: print("recent 30 minute :   😴😴")
    return heikin_ashi_candle

def get_1_hour(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_1HOUR, limit=3)
    heikin_ashi_candle = heikin_ashi(klines)
    if heikin_ashi_candle == "UP": print("1 HOUR DIRECTION :   🥦🥦")
    elif heikin_ashi_candle == "DOWN": print("1 HOUR DIRECTION :   🩸🩸")
    else: print("1 HOUR DIRECTION :   😴😴")
    return heikin_ashi_candle

def get_4_hour(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_4HOUR, limit=3)
    heikin_ashi_candle = heikin_ashi(klines)
    if heikin_ashi_candle == "UP": print("4 HOUR DIRECTION :   🥦🥦🥦")
    elif heikin_ashi_candle == "DOWN": print("4 HOUR DIRECTION :   🩸🩸🩸")
    else: print("4 HOUR DIRECTION :   😴😴😴")
    return heikin_ashi_candle

def get_6_hour(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_6HOUR, limit=3)
    heikin_ashi_candle = heikin_ashi(klines)
    if heikin_ashi_candle == "UP": print("6 HOUR DIRECTION :   🥦🥦🥦")
    elif heikin_ashi_candle == "DOWN": print("6 HOUR DIRECTION :   🩸🩸🩸")
    else: print("6 HOUR DIRECTION :   😴😴😴")
    return heikin_ashi_candle
