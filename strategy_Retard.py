import config
import candlestick
import get_position
import heikin_ashi
import binance_futures_api
from datetime import datetime
from termcolor import colored

def lets_make_some_money(i):
    response = binance_futures_api.position_information(i)
    klines_30min = binance_futures_api.KLINE_INTERVAL_30MINUTE(i)
    klines_6HOUR = binance_futures_api.KLINE_INTERVAL_6HOUR(i)
    position_info = get_position.get_position_info(i, response)

    heikin_ashi.output(klines_6HOUR)
    candlestick.output(klines_6HOUR)

    leverage = config.leverage[i]
    if int(response.get("leverage")) != leverage: binance_futures_api.change_leverage(i, leverage)
    if response.get('marginType') != "isolated": binance_futures_api.change_margin_to_ISOLATED(i)

    if position_info == "LONGING":
        if EXIT_LONG(klines_6HOUR): binance_futures_api.close_position(i, "LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if EXIT_SHORT(klines_6HOUR): binance_futures_api.close_position(i, "SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if GO_LONG(klines_6HOUR) and not hot_zone(klines_30min, klines_6HOUR):
            binance_futures_api.open_position(i, "LONG", config.quantity[i])

        elif GO_SHORT(klines_6HOUR) and not hot_zone(klines_30min, klines_6HOUR):
            binance_futures_api.open_position(i, "SHORT", config.quantity[i])

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def hot_zone(klines_30MIN, klines_6HOUR):
    if klines_6HOUR[-1][0] == klines_30MIN[-1][0]: return True

def GO_LONG(klines_6HOUR):
    if candlestick.hybrid(klines_6HOUR) == "GREEN": return True

def GO_SHORT(klines_6HOUR):
    if candlestick.hybrid(klines_6HOUR) == "RED": return True

def EXIT_LONG(klines_6HOUR):
    if heikin_ashi.VALID_CANDLE(klines_6HOUR) != "GREEN" and candlestick.candle_color(klines_6HOUR) == "RED": return True

def EXIT_SHORT(klines_6HOUR):
    if heikin_ashi.VALID_CANDLE(klines_6HOUR) != "RED" and candlestick.candle_color(klines_6HOUR) == "GREEN": return True
