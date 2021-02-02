import config
import binance_futures
from datetime import datetime
from termcolor import colored
from get_hour import get_hour
from get_minute import recent_minute
from get_minute import emergency_minute
from get_position import get_position_info

def get_current_minute():
    title = "CURRENT MINUTE   :   "
    klines = binance_futures.KLINE_INTERVAL_1MINUTE()

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), config.round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), config.round_decimal)
    first_Open      = round(((first_run_Open + first_run_Close) / 2), config.round_decimal)
    first_Close     = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), config.round_decimal)
    previous_Open   = round(((first_Open + first_Close) / 2), config.round_decimal)
    previous_Close  = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[1][3]) + float(klines[2][4])) / 4), config.round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), config.round_decimal)
    current_Close   = round(((float(klines[3][1]) + float(klines[3][2]) + float(klines[3][3]) + float(klines[3][4])) / 4), config.round_decimal)
    current_High    = max(float(klines[3][2]), current_Open, current_Close)
    current_Low     = min(float(klines[3][3]), current_Open, current_Close)

    if (current_Open == current_High):
        minute_candle = "RED"
        print(colored(title + minute_candle, "red"))

    elif (current_Open == current_Low):
        minute_candle = "GREEN"
        print(colored(title + minute_candle, "green"))

    elif (current_Open > current_Close):
        minute_candle = "RED_INDECISIVE"
        print(colored(title + minute_candle, "red"))

    elif (current_Close > current_Open):
        minute_candle = "GREEN_INDECISIVE"
        print(colored(title + minute_candle, "green"))

    else:
        minute_candle = "NO_MOVEMENT"
        print(colored(title + minute_candle, "yellow"))

    return minute_candle

def scalping_no_trend():
    title = "ACTION           :   "
    position_info = get_position_info()
    minute_candle = get_current_minute()

    if position_info == "LONGING": print(colored(title + "HOLDING_LONG", "green"))
    elif position_info == "SHORTING": print(colored(title + "HOLDING_SHORT", "red"))
    else:
        binance_futures.cancel_all_open_orders()
        if (minute_candle == "GREEN"):
            binance_futures.open_position("LONG")
            binance_futures.set_stop_loss("LONG")
            binance_futures.set_take_profit("LONG")
            print(colored(title + "🚀 GO_LONG 🚀", "green"))

        elif (minute_candle == "RED"):
            binance_futures.open_position("SHORT")
            binance_futures.set_stop_loss("SHORT")
            binance_futures.set_take_profit("SHORT")
            print(colored(title + "💥 GO_SHORT 💥", "red"))

        else: print(title + "🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")