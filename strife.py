import os, config
import candlestick
import heikin_ashi
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored
from heikin_ashi import war_formation
from heikin_ashi import current_candle, previous_candle
from heikin_ashi import strength_of_current, strength_of_previous

live_trade = config.live_trade
def profit_threshold(): return 0.2 

def lets_make_some_money():
    response = binance_futures.position_information()[0]
    mark_price   = binance_futures.mark_price()
    klines_1min  = binance_futures.KLINE_INTERVAL_1MINUTE()
    klines_5min  = binance_futures.KLINE_INTERVAL_5MINUTE()
    klines_1HOUR = binance_futures.KLINE_INTERVAL_1HOUR()

    position_info = get_position.get_position_info(response)
    profit = profit_threshold()

    if candlestick.strong_candle(klines_1HOUR): strength = "STRONG "
    else: strength = "WEAK "
    print("CANDLESTICK COLOR:   " + strength + candlestick.candle_color(klines_1HOUR))
    heikin_ashi.output_current(klines_1HOUR)
    heikin_ashi.output_current(klines_5min)
    heikin_ashi.output_current(klines_1min)

    if position_info == "LONGING":
        if EXIT_LONG(profit, klines_1min, klines_5min, klines_1HOUR):
            if live_trade: binance_futures.close_position("LONG")
            print("ACTION           :   💰 CLOSE_LONG 💰")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if EXIT_SHORT(profit, klines_1min, klines_5min, klines_1HOUR):
            if live_trade: binance_futures.close_position("SHORT")
            print("ACTION           :   💰 CLOSE_SHORT 💰")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if clear_direction(klines_1HOUR) == "GREEN" and GO_LONG(mark_price, klines_1min, klines_5min):
            if live_trade: binance_futures.open_position("LONG", config.quantity)
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

        elif clear_direction(klines_1HOUR) == "RED" and GO_SHORT(mark_price, klines_1min, klines_5min):
            if live_trade: binance_futures.open_position("SHORT", config.quantity)
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def clear_direction(klines):
    if candlestick.candle_color(klines) == "GREEN" and candlestick.strong_candle(klines): candle = "GREEN"
    elif candlestick.candle_color(klines) == "RED" and candlestick.strong_candle(klines): candle = "RED"
    else: candle = "INDECISIVE"

    if (current_candle(klines) == "GREEN" or current_candle(klines) == "GREEN_INDECISIVE") and strength_of_current(klines) == "STRONG" : current = "GREEN"
    elif (current_candle(klines) == "RED" or current_candle(klines) == "RED_INDECISIVE" and strength_of_current(klines) == "STRONG") : current = "RED"
    else: current = "INDECISIVE"

    if candle == "GREEN" and current == "GREEN": direction = "GREEN"
    elif candle == "RED" and current == "RED": direction = "RED"
    else: direction = "INDECISIVE"
    return direction

def GO_LONG(mark_price, klines_1min, klines_5min):
    if war_formation(mark_price, klines_5min) and war_formation(mark_price, klines_1min) and \
        (current_candle(klines_5min) == "GREEN" or current_candle(klines_5min) == "GREEN_INDECISIVE") and strength_of_current(klines_5min) == "STRONG" and \
        (current_candle(klines_1min) == "GREEN" and strength_of_current(klines_1min) == "STRONG"): return True

def GO_SHORT(mark_price, klines_1min, klines_5min):
    if war_formation(mark_price, klines_5min) and war_formation(mark_price, klines_1min) and \
        (current_candle(klines_5min) == "RED" or current_candle(klines_5min) == "RED_INDECISIVE") and strength_of_current(klines_5min) == "STRONG" and \
        (current_candle(klines_1min) == "RED" and strength_of_current(klines_1min) == "STRONG"): return True

def EXIT_LONG(profit, klines_1min, klines_5min, klines_1HOUR):
    if get_position.profit_or_loss(profit) == "PROFIT":
        if heikin_ashi.previous_Close(klines_1min) > heikin_ashi.current_Close(klines_1min) or current_candle(klines_1min) != "GREEN": return True
    elif clear_direction(klines_1HOUR) == "RED": return True

def EXIT_SHORT(profit, klines_1min, klines_5min, klines_1HOUR):
    if get_position.profit_or_loss(profit) == "PROFIT":
        if heikin_ashi.previous_Close(klines_1min) < heikin_ashi.current_Close(klines_1min) or current_candle(klines_1min) != "RED": return True
        elif clear_direction(klines_1HOUR) == "GREEN": return True
