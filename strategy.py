import os
import config
import heikin_ashi
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored
from heikin_ashi import current_candle
from heikin_ashi import pattern_broken
from heikin_ashi import war_formation
from heikin_ashi import strength_of_current
from get_position import get_unRealizedProfit

live_trade = config.live_trade
profit = 0.6 # This float times leverage is the expected profit percentage

# ==========================================================================================================================================================================
#                    JACK_RABBIT - IN AND OUT QUICK, SOMETIMES MIGHT GET YOU STUCK IN A TRADE AND LIQUIDATED WHEN DIRECTION CHANGE
# ==========================================================================================================================================================================
def lets_make_some_money():
    # RETRIEVE KLINES and INFORMATION
    position_info = get_position.get_position_info()
    klines_1min   = binance_futures.KLINE_INTERVAL_1MINUTE()
    klines_30MIN  = binance_futures.KLINE_INTERVAL_30MINUTE()
    klines_1HOUR  = binance_futures.KLINE_INTERVAL_1HOUR()
    klines_6HOUR  = binance_futures.KLINE_INTERVAL_6HOUR()
    
    heikin_ashi.output_current(klines_6HOUR)
    heikin_ashi.output_current(klines_1HOUR)
    heikin_ashi.output_current(klines_1min)

    if position_info == "LONGING":
        if EXIT_LONG(klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
            if live_trade: binance_futures.close_position("LONG")
            # record_timestamp(klines_1HOUR)
            print("ACTION           :   💰 CLOSE_LONG 💰")
        #  elif  
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if EXIT_SHORT(klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
            if live_trade: binance_futures.close_position("SHORT")
            # record_timestamp(klines_1HOUR)
            print("ACTION           :   💰 CLOSE_SHORT 💰")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if check_direction(klines_6HOUR) == "GREEN" and GO_LONG(klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR): # and (retrieve_timestamp() != current_kline_timestamp(klines_1HOUR)):
            if live_trade: binance_futures.open_position("LONG", trade_amount(klines_1HOUR, klines_6HOUR))
            # record_timestamp(klines_1HOUR)
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

        elif check_direction(klines_6HOUR) == "RED" and GO_SHORT(klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR): # and (retrieve_timestamp() != current_kline_timestamp(klines_1HOUR)):
            if live_trade: binance_futures.open_position("SHORT", trade_amount(klines_1HOUR, klines_6HOUR))
            # record_timestamp(klines_1HOUR)
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                        ENTRY_EXIT CONDITIONS
# ==========================================================================================================================================================================
def check_direction(klines):
    if strength_of_current(klines) == "STRONG":
        if current_candle(klines) == "GREEN" or current_candle(klines) == "GREEN_INDECISIVE" : direction = "GREEN"
        elif current_candle(klines) == "RED" or current_candle(klines) == "RED_INDECISIVE" : direction = "RED"
        else: direction = "INDECISIVE"

    # elif strength_of_current(klines) == "WEAK":
    #     if current_candle(klines) == "GREEN": direction = "RED"
    #     elif current_candle(klines) == "RED": direction = "GREEN"
    #     else: direction = "INDECISIVE"

    else: direction = "INDECISIVE"
    return direction
    
def GO_LONG(klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
    if not hot_zone(klines_30MIN, klines_6HOUR) and check_direction(klines_1HOUR) == "GREEN" and \
       not heikin_ashi.volume_declining(klines_1HOUR) and not heikin_ashi.volume_declining(klines_6HOUR):
        if current_candle(klines_1min) == "GREEN" and strength_of_current(klines_1min) == "STRONG" and war_formation(klines_1min): return True

def GO_SHORT(klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
    if not hot_zone(klines_30MIN, klines_6HOUR) and check_direction(klines_1HOUR) == "RED" and \
       not heikin_ashi.volume_declining(klines_1HOUR) and not heikin_ashi.volume_declining(klines_6HOUR):
        if current_candle(klines_1min) == "RED" and strength_of_current(klines_1min) == "STRONG" and war_formation(klines_1min): return True

def EXIT_LONG(klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
    if get_unRealizedProfit(profit) == "PROFIT":
        if heikin_ashi.previous_Close(klines_1min) > heikin_ashi.current_Close(klines_1min) or current_candle(klines_1min) != "GREEN": return True
    else: # Cut loss when both the 1HOUR and 6HOUR is going against you
        if not hot_zone(klines_30MIN, klines_6HOUR) and check_direction(klines_1HOUR) == "RED" and check_direction(klines_6HOUR) == "RED": return True

def EXIT_SHORT(klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
    if get_unRealizedProfit(profit) == "PROFIT":
        if heikin_ashi.previous_Close(klines_1min) < heikin_ashi.current_Close(klines_1min) or current_candle(klines_1min) != "RED": return True
    else: # Cut loss when both the 1HOUR and 6HOUR is going against you
        if not hot_zone(klines_30MIN, klines_6HOUR) and check_direction(klines_1HOUR) == "GREEN" and check_direction(klines_6HOUR) == "GREEN": return True

def THROTTLE_LONG(klines_30MIN, klines_1HOUR, klines_6HOUR):
    if get_unRealizedProfit(profit) == "LOSS":
        if retrieve_timestamp() != current_kline_timestamp(klines_1HOUR) and current_kline_timestamp(klines_1HOUR) != current_kline_timestamp(klines_30MIN):
            if heikin_ashi.current_Low(klines_1HOUR) > heikin_ashi.previous_Low(klines_1HOUR): return True

def hot_zone(klines_30MIN, klines_6HOUR):
    if klines_6HOUR[-1][0] == klines_30MIN[-1][0]: return True

# ==========================================================================================================================================================================
#                                                  EXTRA ADD-ON WORK IN PROGRESS
# ==========================================================================================================================================================================

def slipping_back():
    return "WORK IN PROGRESS"

def DO_NOT_FUCKING_TRADE():
    return True

# ==========================================================================================================================================================================
#                                              SYSTEM TIME RECORD TO AVOID OVER-TRADE
# ==========================================================================================================================================================================

def record_timestamp(kline):
    if not os.path.exists(config.pair): os.makedirs(config.pair)
    with open((os.path.join(config.pair, "TIMESTAMP.txt")), "w", encoding="utf-8") as timestamp_record:
        timestamp_record.write(str(current_kline_timestamp(kline)))

def retrieve_timestamp():
    with open((os.path.join(config.pair, "TIMESTAMP.txt")), "r", encoding="utf-8") as timestamp_record:
        return int(timestamp_record.read())

def current_kline_timestamp(kline):
    return kline[-1][0] # This will return <int> type of timestamp

record_timestamp(binance_futures.KLINE_INTERVAL_1HOUR())

# ==========================================================================================================================================================================
#                                                     Auto Adjust Trade Amount
# ==========================================================================================================================================================================
def clear_direction(klines_6HOUR):
    previous_candle = heikin_ashi.previous_candle(klines_6HOUR)
    current_candle  = heikin_ashi.current_candle(klines_6HOUR)
    if (previous_candle == "GREEN") and (current_candle == "GREEN"): trend = "GREEN"
    elif (previous_candle == "RED") and (current_candle == "RED"): trend = "RED"
    else: trend = "NO_TRADE_ZONE"
    return trend

def trade_amount(klines_6HOUR, klines_1HOUR):
    if heikin_ashi.volume_formation(klines_6HOUR) and heikin_ashi.volume_breakout(klines_6HOUR):
        if clear_direction(klines_6HOUR) == "GREEN" or clear_direction(klines_6HOUR) == "RED": 
            trade_amount = config.quantity * 5
        else: trade_amount = config.quantity * 4
    
    elif heikin_ashi.volume_formation(klines_6HOUR) and not heikin_ashi.volume_breakout(klines_6HOUR):
        if clear_direction(klines_6HOUR) == "GREEN" or clear_direction(klines_6HOUR) == "RED": 
            trade_amount = config.quantity * 3
        else: trade_amount = config.quantity * 2

    elif not heikin_ashi.volume_formation(klines_6HOUR) and heikin_ashi.volume_breakout(klines_6HOUR):
        if clear_direction(klines_6HOUR) == "GREEN" or clear_direction(klines_6HOUR) == "RED": 
            trade_amount = config.quantity * 2
        else: trade_amount = config.quantity * 1

    else: trade_amount = config.quantity

    return trade_amount
