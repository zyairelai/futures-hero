import keys
import config
from binance.client import Client

def get_current_trend(): # >>> UP_TREND // DOWN_TREND // NO_TRADE_ZONE
    if (main_direction == "UP") and (recent_minute == "UP"):
        trend = "UP_TREND"
        print("Current TREND    :   🥦 UP_TREND 🥦")
    elif (main_direction == "DOWN") and (recent_minute == "DOWN"):
        trend = "DOWN_TREND"
        print("Current TREND    :   🩸 DOWN_TREND 🩸")
    else:
        trend = "NO_TRADE_ZONE"
        print("Current TREND    :   😴 NO_TRADE_ZONE 😴")
    return trend

def get_15_minute():
    klines = keys.client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_15MINUTE , limit=3)
    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)
    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)
    if      (current_Open == current_Low)   :   trend = "UP"
    elif    (current_Open == current_High)  :   trend = "DOWN"
    else                                    :   trend = "INDECISIVE"
    return trend

def get_30_minute():
    klines = keys.client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_30MINUTE , limit=3)
    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)
    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)
    if      (current_Open == current_Low)   :   trend = "UP"
    elif    (current_Open == current_High)  :   trend = "DOWN"
    else                                    :   trend = "INDECISIVE"
    return trend

def get_1_hour():
    klines = keys.client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_1HOUR, limit=3)
    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)
    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)
    if      (current_Open == current_Low)   :   trend = "UP"
    elif    (current_Open == current_High)  :   trend = "DOWN"
    else                                    :   trend = "INDECISIVE"
    return trend

def get_4_hour():
    klines = keys.client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_4HOUR, limit=3)
    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)
    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)
    if      (current_Open == current_Low)   :   trend = "UP"
    elif    (current_Open == current_High)  :   trend = "DOWN"
    else                                    :   trend = "INDECISIVE"
    return trend

def get_6_hour():
    klines = keys.client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_6HOUR, limit=3)
    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)
    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)
    if      (current_Open == current_Low)   :   trend = "UP"
    elif    (current_Open == current_High)  :   trend = "DOWN"
    else                                    :   trend = "INDECISIVE"
    return trend

main_direction  =  get_6_hour()         # get_4_hour    // get_6_hour
recent_minute   =  get_15_minute()      # get_15_minute // get_30_minute // get_1_hour