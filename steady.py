import os, config, volume
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

def profit_threshold():
    return 0.2 # This number times leverage is the realized PnL Percentage
    # For example, BTC leverage 50x * 0.2 = 10% It will take profit when it reaches 10%
    # Do note that the fees Binance charges is 0.15 * 50 = 7.5% 

# ==========================================================================================================================================================================
#     Jackrabbit Martingale_Strategy - IN AND OUT QUICK, SOMETIMES MIGHT GET YOU STUCK IN A TRADE AND LIQUIDATED WHEN DIRECTION CHANGE
# ==========================================================================================================================================================================

def lets_make_some_money():
    for i in range(len(config.pair)):
        response = binance_futures.position_information(i)[0]
        mark_price   = binance_futures.mark_price(i)
        klines_1min  = binance_futures.KLINE_INTERVAL_1MINUTE(i)
        klines_30MIN = binance_futures.KLINE_INTERVAL_30MINUTE(i)
        klines_1HOUR = binance_futures.KLINE_INTERVAL_1HOUR(i)
        klines_6HOUR = binance_futures.KLINE_INTERVAL_6HOUR(i)
        klines_12HOUR = binance_futures.KLINE_INTERVAL_12HOUR(i)
        position_info = get_position.get_position_info(i, response)
        profit = profit_threshold()

        heikin_ashi.output_previous(klines_6HOUR)
        heikin_ashi.output_current(mark_price, klines_6HOUR)
        heikin_ashi.output_current(mark_price, klines_1HOUR)
        heikin_ashi.output_current(mark_price, klines_1min)
        
        if response.get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED(i)
        if int(response.get("leverage")) != config.leverage[i]: binance_futures.change_leverage(i, config.leverage[i])

        if position_info == "LONGING":
            if EXIT_LONG(response, mark_price, profit, klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
                if live_trade: binance_futures.close_position(i, "LONG")
                print("ACTION           :   💰 CLOSE_LONG 💰")
            elif THROTTLE_LONG(i, response, mark_price, klines_1HOUR, klines_6HOUR):
                if live_trade: binance_futures.throttle(i, "LONG")
                print("ACTION           :   🔥 THROTTLE_LONG 🔥")
            else: print(colored("ACTION           :   HOLDING_LONG", "green"))

        elif position_info == "SHORTING":
            if EXIT_SHORT(response, mark_price, profit, klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
                if live_trade: binance_futures.close_position(i, "SHORT")
                print("ACTION           :   💰 CLOSE_SHORT 💰")
            elif THROTTLE_SHORT(i, response, mark_price, klines_1HOUR, klines_6HOUR):
                if live_trade: binance_futures.throttle(i, "SHORT")
                print("ACTION           :   🔥 THROTTLE_SHORT 🔥")
            else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

        else:
            if clear_direction(mark_price, klines_6HOUR) == "GREEN" and direction_confirmation(mark_price, klines_12HOUR) == "GREEN" and \
                GO_LONG(mark_price, klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
                if live_trade: binance_futures.open_position(i, "LONG", config.quantity[i])
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

            elif clear_direction(mark_price, klines_6HOUR) == "RED" and direction_confirmation(mark_price, klines_12HOUR) == "RED" and \
                GO_SHORT(mark_price, klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
                if live_trade: binance_futures.open_position(i, "SHORT", config.quantity[i])
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

            else: print("ACTION           :   🐺 WAIT 🐺")

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                        ENTRY_EXIT CONDITIONS
# ==========================================================================================================================================================================

def clear_direction(mark_price, klines):
    if (current_candle(klines) == "GREEN" or current_candle(klines) == "GREEN_INDECISIVE") and strength_of_current(mark_price, klines) == "STRONG" : current = "GREEN"
    elif (current_candle(klines) == "RED" or current_candle(klines) == "RED_INDECISIVE" and strength_of_current(mark_price, klines) == "STRONG") : current = "RED"
    else: current = "INDECISIVE"

    if previous_candle(klines) == "GREEN" and current == "GREEN": direction = "GREEN"
    elif previous_candle(klines) == "RED" and current == "RED": direction = "RED"
    else: direction = "INDECISIVE"
    return direction

def direction_confirmation(mark_price, klines):
    if (current_candle(klines) == "GREEN" or current_candle(klines) == "GREEN_INDECISIVE") and strength_of_current(mark_price, klines) == "STRONG" : return "GREEN"
    elif (current_candle(klines) == "RED" or current_candle(klines) == "RED_INDECISIVE" and strength_of_current(mark_price, klines) == "STRONG") : return "RED"
    else: return "INDECISIVE"

def GO_LONG(mark_price, klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
    if not hot_zone(klines_30MIN, klines_6HOUR): # and not volume.volume_declining(klines_1HOUR):
        if war_formation(mark_price, klines_1min) and candlestick.candle_color(klines_1min) == "GREEN" and \
           (candlestick.candle_color(klines_1HOUR) == "GREEN" and candlestick.strong_candle(klines_1HOUR)) and \
           (current_candle(klines_1HOUR) == "GREEN" or current_candle(klines_1HOUR) == "GREEN_INDECISIVE") and strength_of_current(mark_price, klines_1HOUR) == "STRONG" and \
           (current_candle(klines_1min) == "GREEN" and strength_of_current(mark_price, klines_1min) == "STRONG"): return True

def GO_SHORT(mark_price, klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
    if not hot_zone(klines_30MIN, klines_6HOUR): # and not volume.volume_declining(klines_1HOUR):
        if war_formation(mark_price, klines_1min) and candlestick.candle_color(klines_1min) == "RED" and \
           (candlestick.candle_color(klines_1HOUR) == "RED" and candlestick.strong_candle(klines_1HOUR)) and \
           (current_candle(klines_1HOUR) == "RED" or current_candle(klines_1HOUR) == "RED_INDECISIVE") and strength_of_current(mark_price, klines_1HOUR) == "STRONG" and \
           (current_candle(klines_1min) == "RED" and strength_of_current(mark_price, klines_1min) == "STRONG"): return True

def EXIT_LONG(response, mark_price, profit, klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
    if get_position.profit_or_loss(response, profit) == "PROFIT":
        # if (current_candle(klines_1min) == "RED" or current_candle(klines_1min) == "RED_INDECISIVE") and strength_of_current(mark_price, klines_1min) == "STRONG": return True
        if heikin_ashi.previous_Close(klines_1min) > heikin_ashi.current_Close(klines_1min) or current_candle(klines_1min) != "GREEN": return True
    else:
        # Cut loss when both the 1HOUR and 6HOUR is going against you
        if not hot_zone(klines_30MIN, klines_6HOUR) and clear_direction(mark_price, klines_6HOUR) == "RED": return True

def EXIT_SHORT(response, mark_price, profit, klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
    if get_position.profit_or_loss(response, profit) == "PROFIT":
        # if (current_candle(klines_1min) == "GREEN" or current_candle(klines_1min) == "GREEN_INDECISIVE") and strength_of_current(mark_price, klines_1min) == "STRONG": return True
        if heikin_ashi.previous_Close(klines_1min) < heikin_ashi.current_Close(klines_1min) or current_candle(klines_1min) != "RED": return True
    else:
        # Cut loss when both the 1HOUR and 6HOUR is going against you
        if not hot_zone(klines_30MIN, klines_6HOUR) and clear_direction(mark_price, klines_6HOUR) == "GREEN": return True

# Adding to the losing position to pull back the entry price when the maintenance margin is below 70%
throttle_threshold = -0.7
max_throttle_size  = 8

def THROTTLE_LONG(i, response, mark_price, klines_1HOUR, klines_6HOUR):
    if clear_direction(mark_price, klines_6HOUR) == "GREEN" and get_position.get_positionSize(response) < (config.quantity[i] * max_throttle_size) and \
        get_position.get_unrealizedProfit(response) < get_position.get_margin(response) * throttle_threshold: return True

def THROTTLE_SHORT(i, response, mark_price, klines_1HOUR, klines_6HOUR):
    if clear_direction(mark_price, klines_6HOUR) == "RED" and get_position.get_positionSize(response) < (config.quantity[i] * max_throttle_size) and \
        get_position.get_unrealizedProfit(response) < get_position.get_margin(response) * throttle_threshold: return True

def hot_zone(klines_30MIN, klines_6HOUR):
    if klines_6HOUR[-1][0] == klines_30MIN[-1][0]: return True
