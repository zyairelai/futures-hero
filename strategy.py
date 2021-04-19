import os
import config
import heikin_ashi
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored
from heikin_ashi import war_formation
from heikin_ashi import current_candle, previous_candle
from heikin_ashi import strength_of_current, strength_of_previous

live_trade = config.live_trade

def profit_threshold(response):
    if get_position.get_positionSize(response) == (config.quantity * 3): return 0.3
    elif get_position.get_positionSize(response) == config.quantity: return 0.4
    else: return 0.2

# ==========================================================================================================================================================================
#                   Jackrabbit Martingale_Strategy - IN AND OUT QUICK, SOMETIMES MIGHT GET YOU STUCK IN A TRADE AND LIQUIDATED WHEN DIRECTION CHANGE
# ==========================================================================================================================================================================

def lets_make_some_money():
    # RETRIEVE KLINES and INFORMATION
    response = binance_futures.position_information()[0]
    mark_price   = binance_futures.mark_price()
    klines_1min  = binance_futures.KLINE_INTERVAL_1MINUTE()
    klines_5min  = binance_futures.KLINE_INTERVAL_5MINUTE()
    klines_30MIN = binance_futures.KLINE_INTERVAL_30MINUTE()
    klines_1HOUR = binance_futures.KLINE_INTERVAL_1HOUR()
    klines_2HOUR = binance_futures.KLINE_INTERVAL_2HOUR()
    klines_6HOUR = binance_futures.KLINE_INTERVAL_6HOUR()
    
    heikin_ashi.output_previous(klines_6HOUR)
    heikin_ashi.output_current(klines_6HOUR)
    heikin_ashi.output_current(klines_1HOUR)
    heikin_ashi.output_current(klines_5min)
    heikin_ashi.output_current(klines_1min)

    position_info = get_position.get_position_info(response)
    profit = profit_threshold(response)

    if position_info == "LONGING":
        if EXIT_LONG(profit, klines_1min, klines_5min, klines_30MIN, klines_1HOUR, klines_6HOUR):
            if live_trade: binance_futures.close_position("LONG")
            # record_timestamp(klines_5min)
            print("ACTION           :   💰 CLOSE_LONG 💰")
        elif THROTTLE_LONG(response, mark_price, klines_1HOUR, klines_2HOUR, klines_6HOUR):
            if live_trade: binance_futures.throttle("LONG")
            print("ACTION           :   🔥 THROTTLE_LONG 🔥")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if EXIT_SHORT(profit, klines_1min, klines_5min, klines_30MIN, klines_1HOUR, klines_6HOUR):
            if live_trade: binance_futures.close_position("SHORT")
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            # record_timestamp(klines_5min)
        elif THROTTLE_SHORT(response, mark_price, klines_1HOUR, klines_2HOUR, klines_6HOUR):
            if live_trade: binance_futures.throttle("SHORT")
            print("ACTION           :   🔥 THROTTLE_SHORT 🔥")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        # current_kline_timestamp(klines_5min) != retrieve_timestamp() and 
        if clear_direction(klines_6HOUR) == "GREEN" and GO_LONG(mark_price, klines_1min, klines_5min, klines_30MIN, klines_1HOUR, klines_6HOUR):
            if live_trade: binance_futures.open_position("LONG", config.quantity)
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

        elif clear_direction(klines_6HOUR) == "RED" and GO_SHORT(mark_price, klines_1min, klines_5min, klines_30MIN, klines_1HOUR, klines_6HOUR):
            if live_trade: binance_futures.open_position("SHORT", config.quantity)
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                        ENTRY_EXIT CONDITIONS
# ==========================================================================================================================================================================

def clear_direction(klines):
    if (previous_candle(klines) == "GREEN" or previous_candle(klines) == "GREEN_INDECISIVE"): previous = "GREEN"
    elif (previous_candle(klines) == "RED" or previous_candle(klines) == "RED_INDECISIVE"): previous = "RED"
    else: previous = "INDECISIVE"

    if (current_candle(klines) == "GREEN" or current_candle(klines) == "GREEN_INDECISIVE") and strength_of_current(klines) == "STRONG" : current = "GREEN"
    elif (current_candle(klines) == "RED" or current_candle(klines) == "RED_INDECISIVE" and strength_of_current(klines) == "STRONG") : current = "RED"
    else: current = "INDECISIVE"

    if previous == "GREEN" and current == "GREEN": direction = "GREEN"
    elif previous == "RED" and current == "RED": direction = "RED"
    else: direction = "INDECISIVE"
    return direction
    
def GO_LONG(mark_price, klines_1min, klines_5min, klines_30MIN, klines_1HOUR, klines_6HOUR):
    if not hot_zone(klines_30MIN, klines_6HOUR) and not heikin_ashi.volume_declining(klines_1HOUR):
        if (current_candle(klines_1HOUR) == "GREEN" or current_candle(klines_1HOUR) == "GREEN_INDECISIVE") and strength_of_current(klines_1HOUR) == "STRONG" and \
           (current_candle(klines_5min) == "GREEN" or current_candle(klines_5min) == "GREEN_INDECISIVE") and strength_of_current(klines_5min) == "STRONG" and \
           (current_candle(klines_1min) == "GREEN" and strength_of_current(klines_1min) == "STRONG") and \
            war_formation(mark_price, klines_5min) and war_formation(mark_price, klines_1min): return True

def GO_SHORT(mark_price, klines_1min, klines_5min, klines_30MIN, klines_1HOUR, klines_6HOUR):
    if not hot_zone(klines_30MIN, klines_6HOUR) and not heikin_ashi.volume_declining(klines_1HOUR):
        if (current_candle(klines_1HOUR) == "RED" or current_candle(klines_1HOUR) == "RED_INDECISIVE") and strength_of_current(klines_1HOUR) == "STRONG" and \
           (current_candle(klines_5min) == "RED" or current_candle(klines_5min) == "RED_INDECISIVE") and strength_of_current(klines_5min) == "STRONG" and \
           (current_candle(klines_1min) == "RED" and strength_of_current(klines_1min) == "STRONG")  and \
            war_formation(mark_price, klines_5min) and war_formation(mark_price, klines_1min): return True

def EXIT_LONG(profit, klines_1min, klines_5min, klines_30MIN, klines_1HOUR, klines_6HOUR):
    if get_position.profit_or_loss(profit) == "PROFIT":
        # if (current_candle(klines_1min) == "RED" or current_candle(klines_1min) == "RED_INDECISIVE") and strength_of_current(klines_1min) == "STRONG": return True
        if heikin_ashi.previous_Close(klines_1min) > heikin_ashi.current_Close(klines_1min) or current_candle(klines_1min) != "GREEN": return True
    else:
        # Cut loss when both the 1HOUR and 6HOUR is going against you
        if not hot_zone(klines_30MIN, klines_6HOUR) and clear_direction(klines_1HOUR) == "RED" and clear_direction(klines_6HOUR) == "RED": return True

# ADD mark_price on exit to avoid retard exit

def EXIT_SHORT(profit, klines_1min, klines_5min, klines_30MIN, klines_1HOUR, klines_6HOUR):
    if get_position.profit_or_loss(profit) == "PROFIT":
        # if (current_candle(klines_1min) == "GREEN" or current_candle(klines_1min) == "GREEN_INDECISIVE") and strength_of_current(klines_1min) == "STRONG": return True
        if heikin_ashi.previous_Close(klines_1min) < heikin_ashi.current_Close(klines_1min) or current_candle(klines_1min) != "RED": return True
    else:
        # Cut loss when both the 1HOUR and 6HOUR is going against you
        if not hot_zone(klines_30MIN, klines_6HOUR) and clear_direction(klines_1HOUR) == "GREEN" and clear_direction(klines_6HOUR) == "GREEN": return True

# Adding to the losing position to pull back the entry price when the maintenance margin is below 70%
throttle_threshold = -0.7
max_throttle_size  = 9

def THROTTLE_LONG(response, mark_price, klines_1HOUR, klines_2HOUR, klines_6HOUR):
    if clear_direction(klines_6HOUR) != "RED" and get_position.get_positionSize(response) < (config.quantity * max_throttle_size) and \
        get_position.get_unrealizedProfit(response) < get_position.get_margin(response) * throttle_threshold: return True

def THROTTLE_SHORT(response, mark_price, klines_1HOUR, klines_2HOUR, klines_6HOUR):
    if clear_direction(klines_6HOUR) != "GREEN" and get_position.get_positionSize(response) < (config.quantity * max_throttle_size) and \
        get_position.get_unrealizedProfit(response) < get_position.get_margin(response) * throttle_threshold: return True

def hot_zone(klines_30MIN, klines_6HOUR):
    if klines_6HOUR[-1][0] == klines_30MIN[-1][0]: return True

# ==========================================================================================================================================================================
#                                                        SYSTEM RECORD
# ==========================================================================================================================================================================

def record_timestamp(kline):
    with open((os.path.join(config.pair, "TIMESTAMP.txt")), "w", encoding="utf-8") as timestamp_record:
        timestamp_record.write(str(current_kline_timestamp(kline)))

def retrieve_timestamp():
    with open((os.path.join(config.pair, "TIMESTAMP.txt")), "r", encoding="utf-8") as timestamp_record:
        return int(timestamp_record.read())

def current_kline_timestamp(kline):
    return kline[-1][0] # This will return <int> type of timestamp
