# FOMO STRATEGY : Check on 1HR, entry on 1 minute
# AVOID FAKE OUT : Confirmation with 5 minute

import config
import direction
import get_position
import HA_current
import place_order
import binance_futures_api
from datetime import datetime
from termcolor import colored

def lets_make_some_money(i):
    response = binance_futures_api.position_information(i)
    mark_price   = binance_futures_api.mark_price(i)
    klines_1min  = binance_futures_api.KLINE_INTERVAL_1MINUTE(i)
    klines_1HOUR = binance_futures_api.KLINE_INTERVAL_1HOUR(i)
    klines_6HOUR = binance_futures_api.KLINE_INTERVAL_6HOUR(i)
    position_info = get_position.get_position_info(i, response)
    profit_threshold = get_position.profit_threshold()

    HA_current.output(mark_price, klines_1HOUR)
    HA_current.output(mark_price, klines_1min)
    
    leverage = config.leverage[i]
    if int(response.get("leverage")) != leverage: binance_futures_api.change_leverage(i, leverage)
    if response.get('marginType') != "isolated": binance_futures_api.change_margin_to_ISOLATED(i)

    if position_info == "LONGING":
        if place_order.EXIT_LONG(response, mark_price, profit_threshold, klines_1min):
            binance_futures_api.close_position(i, "LONG")

        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if place_order.EXIT_SHORT(response, mark_price, profit_threshold, klines_1min):
            binance_futures_api.close_position(i, "SHORT")

        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if place_order.GO_LONG_EMA(mark_price, klines_1min, klines_1HOUR):
            if direction.absolute_clear_direction(mark_price, klines_6HOUR) == "GREEN": trade_amount = config.quantity[i] * 3
            elif direction.clear_direction(mark_price, klines_6HOUR) == "GREEN": trade_amount = config.quantity[i] * 2
            else: trade_amount = config.quantity[i] 
            binance_futures_api.open_position(i, "LONG", trade_amount)

        elif place_order.GO_SHORT_EMA(mark_price, klines_1min, klines_1HOUR):
            if direction.absolute_clear_direction(mark_price, klines_6HOUR) == "RED": trade_amount = config.quantity[i] * 3
            elif direction.clear_direction(mark_price, klines_6HOUR) == "RED": trade_amount = config.quantity[i] * 2
            else: trade_amount = config.quantity[i] 
            binance_futures_api.open_position(i, "SHORT", trade_amount)

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
