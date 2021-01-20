import config
from keys import client
from binance.client import Client

def main_direction(): return get_6_hour()   # get_4_hour() // get_6_hour()
def recent_minute(): return get_15_minute() # get_15_minute() // get_30_minute() // get_1_hour()

def get_current_trend(): # >>> "UP_TREND" // "DOWN_TREND" // "NO_TRADE_ZONE"
    direction  = main_direction()
    recent_min = recent_minute()
    cooldown   = cooldown_period()
    fakeout    = avoid_fakeout()

    if (direction == "UP") and (recent_min == "UP"):
        print("Current TREND    :   🥦 UP_TREND 🥦")
        if ((fakeout == "UP") and (cooldown == "UP")): trend = "UP_TREND"
        else: trend = "COOLDOWN"

    elif (direction == "DOWN") and (recent_min == "DOWN"):
        print("Current TREND    :   🩸 DOWN_TREND 🩸")
        if ((fakeout == "DOWN") and (cooldown == "DOWN")): trend = "DOWN_TREND"
        else: trend = "COOLDOWN"

    else:
        trend = "NO_TRADE_ZONE"
        print("Current TREND    :   😴 NO_TRADE_ZONE 😴")
    return trend

def cooldown_period():
    cooldown_period = get_3_minute()   
    if cooldown_period == "UP": print("Recent 3 minute  :   🥦 GREEN 🥦")
    elif cooldown_period == "DOWN": print("Recent 3 minute  :   🩸 RED 🩸")
    elif cooldown_period == "INDECISIVE": print("Recent 3 minute  :   😴 INDECISIVE 😴")
    else: print("SOMETHING_IS_BROKEN_IN_AVOIDING_FAKEOUT")
    return cooldown_period

def avoid_fakeout():
    avoid_fakeout = get_5_minute()   
    if avoid_fakeout == "UP": print("Recent 5 minute  :   🥦 GREEN 🥦")
    elif avoid_fakeout == "DOWN": print("Recent 5 minute  :   🩸 RED 🩸")
    elif avoid_fakeout == "INDECISIVE": print("Recent 5 minute  :   😴 INDECISIVE 😴")
    else: print("SOMETHING_IS_BROKEN_IN_AVOIDING_FAKEOUT")
    return avoid_fakeout

def get_3_minute(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_3MINUTE , limit=3)
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

def get_5_minute(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_5MINUTE , limit=3)
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

def get_15_minute(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_15MINUTE , limit=3)
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

def get_30_minute(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_30MINUTE , limit=3)
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

def get_1_hour(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_1HOUR, limit=3)
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

def get_4_hour(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_4HOUR, limit=3)
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

def get_6_hour(): # >>> "UP" // "DOWN" // "INDECISIVE"
    klines = client.futures_klines(symbol=config.pair, interval=Client.KLINE_INTERVAL_6HOUR, limit=3)
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