import config
import get_minute
from keys import client
from binance.client import Client
from termcolor import colored

def get_current_trend(): # >>> "UP_TREND" // "DOWN_TREND" // "NO_TRADE_ZONE"
    main_direction = get_hour(6)
    recent_minute_count = get_minute.recent_minute_count(5)
    if (main_direction == "UP") and (recent_minute_count == "GREEN_CANDLE"): trend = "UP_TREND"
    elif (main_direction == "DOWN") and (recent_minute_count == "RED_CANDLE"): trend = "DOWN_TREND"
    else: trend = "NO_TRADE_ZONE"
    return trend

def get_hour(hour): # >>> "UP" // "DOWN" // "INDECISIVE"
    if hour == 1: klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_1HOUR, limit=3)
    elif hour == 2: klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_2HOUR, limit=3)
    elif hour == 4: klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_4HOUR, limit=3)
    elif hour == 6: klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_6HOUR, limit=3)
    else: 
        hour = 6
        klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_6HOUR, limit=3)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)
    
    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    title = hour + " HOUR DIRECTION :   "

    if (current_Open == current_Low) == "UP":
        print(colored(title + "UP_TREND", "green"))
        trend = "UP"

    elif (current_Open == current_High) == "DOWN":
        print(colored(title + "DOWN_TREND", "red"))
        trend = "DOWN"

    else:
        print(colored(title + "NO_TRADE_ZONE", "yellow"))
        trend = "INDECISIVE"

    return trend
