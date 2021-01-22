import config
from keys import client
from binance.client import Client
from termcolor import colored

def get_current_trend(): # >>> "UP_TREND" // "DOWN_TREND" // "NO_TRADE_ZONE"
    main_direction = get_6_hour()
    recent_minute_count = get_5_minute()

    if (main_direction == "UP") and (recent_minute_count == "UP"):
        print(colored("CURRENT TREND    :   🥦 UP_TREND 🥦", "green"))
        trend = "UP_TREND"

    elif (main_direction == "DOWN") and (recent_minute_count == "DOWN"):
        print(colored("CURRENT TREND    :   🩸 DOWN_TREND 🩸", "red"))
        trend = "DOWN_TREND"

    else:
        trend = "NO_TRADE_ZONE"
        print(colored("CURRENT TREND    :   😴 NO_TRADE_ZONE 😴", "yellow"))
        
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

def get_5_minute(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_5MINUTE , limit=3)
    heikin_ashi_candle = heikin_ashi(klines)
    title = "RECENT 5 MINUTE  :   "
    if heikin_ashi_candle == "UP": print(title + "🥦🥦🥦")
    elif heikin_ashi_candle == "DOWN": print(title + "🩸🩸🩸")
    else: print(title + "😴😴😴")
    return heikin_ashi_candle

def get_4_hour(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_4HOUR, limit=3)
    heikin_ashi_candle = heikin_ashi(klines)
    title = "4 HOUR DIRECTION :   "
    if heikin_ashi_candle == "UP": print(title + "🥦🥦🥦")
    elif heikin_ashi_candle == "DOWN": print(title + "🩸🩸🩸")
    else: print(title + "😴😴😴")
    return heikin_ashi_candle

def get_6_hour(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_6HOUR, limit=3)
    heikin_ashi_candle = heikin_ashi(klines)
    title = "6 HOUR DIRECTION :   "
    if heikin_ashi_candle == "UP": print(title + "🥦🥦🥦")
    elif heikin_ashi_candle == "DOWN": print(title + "🩸🩸🩸")
    else: print(title + "😴😴😴")
    return heikin_ashi_candle
