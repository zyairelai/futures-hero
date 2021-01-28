import config
import binance_futures
from datetime import datetime
from termcolor import colored
from get_position import get_position_info

def get_clear_direction():
    klines = binance_futures.KLINE_INTERVAL_6HOUR()

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)
    previous_High   = max(float(klines[2][2]), previous_Open, previous_Close)
    previous_Low    = min(float(klines[2][3]), previous_Open, previous_Close)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if (previous_Open == previous_Low):
        previous = "GREEN"
        print(colored("PREVIOUS 6 HOUR  :   " + previous, "green"))
    elif (previous_Open == previous_High):
        previous = "RED"
        print(colored("PREVIOUS 6 HOUR  :   " + previous, "red"))
    else:
        previous = "NO_TRADE_ZONE"
        print(colored("PREVIOUS 6 HOUR  :   " + previous, "yellow"))

    if (current_Open == current_Low):
        current = "GREEN"
        trend = "UP_TREND"
        print(colored("CURRENT 6 HOUR   :   " + current, "green"))
    elif (current_Open == current_High):
        current = "RED"
        trend = "DOWN_TREND"
        print(colored("CURRENT 6 HOUR   :   " + current, "red"))
    else:
        current = "NO_TRADE_ZONE"
        trend = "NO_TRADE_ZONE"
        print(colored("CURRENT 6 HOUR   :   " + current, "yellow"))

    # if (previous == "GREEN") and (current == "GREEN"): trend = "UP_TREND"
    # elif (previous == "RED") and (current == "RED"): trend = "DOWN_TREND"
    # else: trend = "NO_TRADE_ZONE"
    return trend

def recent_minute():
    klines = klines = binance_futures.KLINE_INTERVAL_5MINUTE()

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if (current_Open == current_High):
        minute_candle = "RED"
        print(colored("RECENT 5 MINUTE  :   " + minute_candle, "red"))
    elif (current_Open == current_Low):
        minute_candle = "GREEN"
        print(colored("RECENT 5 MINUTE  :   " + minute_candle, "green"))

    else:
        if (current_Open > current_Close):
            minute_candle = "RED_INDECISIVE"
            print(colored("RECENT 5 MINUTE  :   " + minute_candle, "red"))
        elif (current_Close > current_Open):
            minute_candle = "GREEN_INDECISIVE"
            print(colored("RECENT 5 MINUTE  :   " + minute_candle, "green"))
        else:
            minute_candle = "NO_MOVEMENT"
            print(colored("RECENT 5 MINUTE  :   " + minute_candle, "white"))
    return minute_candle

def five_min_trade():
    position_info = get_position_info()
    trend         = get_clear_direction()
    minute_candle = recent_minute()

    if position_info == "LONGING":
        if (minute_candle == "RED"):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if (minute_candle == "GREEN"):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if trend == "UP_TREND":
            if (minute_candle == "GREEN"):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                binance_futures.open_position("LONG")
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif trend == "DOWN_TREND":
            if (minute_candle == "RED"):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                binance_futures.open_position("SHORT")
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")