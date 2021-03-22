import os
import config
import heikin_ashi
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored
from heikin_ashi import current_candle
from heikin_ashi import pattern_broken
from heikin_ashi import pencil_wick_test
from heikin_ashi import strength_of_current
from get_position import get_unRealizedProfit

live_trade = config.live_trade
profit = 0.3 # This float times leverage is the expected profit percentage

# ==========================================================================================================================================================================
#                    JACK_RABBIT - IN AND OUT QUICK, SOMETIMES MIGHT GET YOU STUCK IN A TRADE AND LIQUIDATED WHEN DIRECTION CHANGE
# ==========================================================================================================================================================================
def lets_make_some_money():
    # RETRIEVE KLINES and INFORMATION
    position_info = get_position.get_position_info()
    klines_1min   = binance_futures.KLINE_INTERVAL_1MINUTE()
    klines_1HOUR  = binance_futures.KLINE_INTERVAL_1HOUR()
    klines_6HOUR  = binance_futures.KLINE_INTERVAL_6HOUR()
    
    heikin_ashi.output_current(klines_6HOUR)
    heikin_ashi.output_current(klines_1HOUR)
    heikin_ashi.output_current(klines_1min)

    if position_info == "LONGING":
        if EXIT_LONG(klines_6HOUR, klines_1HOUR, klines_1min):
            if live_trade: binance_futures.close_position("LONG")
            record_timestamp(klines_1HOUR, "JACK_RABBIT")
            print("ACTION           :   💰 CLOSE_LONG 💰")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if EXIT_SHORT(klines_6HOUR, klines_1HOUR, klines_1min):
            if live_trade: binance_futures.close_position("SHORT")
            record_timestamp(klines_1HOUR, "JACK_RABBIT")
            print("ACTION           :   💰 CLOSE_SHORT 💰")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if check_direction(klines_6HOUR) == "GREEN" and GO_LONG(klines_1HOUR, klines_1min) and (retrieve_timestamp("JACK_RABBIT") != current_kline_timestamp(klines_1HOUR)):
            if live_trade: binance_futures.open_position("LONG", trade_amount(klines_6HOUR, klines_1HOUR))
            record_timestamp(klines_1HOUR, "JACK_RABBIT")
            print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

        elif check_direction(klines_6HOUR) == "RED" and GO_SHORT(klines_1HOUR, klines_1min) and (retrieve_timestamp("JACK_RABBIT") != current_kline_timestamp(klines_1HOUR)):
            if live_trade: binance_futures.open_position("SHORT", trade_amount(klines_6HOUR, klines_1HOUR))
            record_timestamp(klines_1HOUR, "JACK_RABBIT")
            print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                        ENTRY_EXIT CONDITIONS
# ==========================================================================================================================================================================
def check_direction(klines_6HOUR):
    if strength_of_current(klines_6HOUR) == "STRONG":
        if current_candle(klines_6HOUR) == "GREEN" or current_candle(klines_6HOUR) == "GREEN_INDECISIVE" : direction = "GREEN"
        elif current_candle(klines_6HOUR) == "RED" or current_candle(klines_6HOUR) == "RED_INDECISIVE" : direction = "RED"
        else: direction = "INDECISIVE"

    elif strength_of_current(klines_6HOUR) == "WEAK":
        if current_candle(klines_6HOUR) == "GREEN": direction = "RED"
        elif current_candle(klines_6HOUR) == "RED": direction = "GREEN"
        else: direction = "INDECISIVE"

    else: direction = "INDECISIVE"
    return direction
    
def GO_LONG(klines_1HOUR, klines_1min):
    if volume_confirmation(klines_1HOUR):
        if (current_candle(klines_1HOUR) == "GREEN" or current_candle(klines_1HOUR) == "GREEN_INDECISIVE") and \
           (strength_of_current(klines_1HOUR) == "STRONG" and pattern_broken(klines_1HOUR) == "NOT_BROKEN") and \
           (strength_of_current(klines_1min)  == "STRONG" and current_candle(klines_1min)  == "GREEN" and pencil_wick_test(klines_1min)):
            return True

def GO_SHORT(klines_1HOUR, klines_1min):
    if volume_confirmation(klines_1HOUR):
        if (current_candle(klines_1HOUR) == "RED" or current_candle(klines_1HOUR) == "RED_INDECISIVE") and \
           (strength_of_current(klines_1HOUR) == "STRONG" and pattern_broken(klines_1HOUR) == "NOT_BROKEN") and \
           (strength_of_current(klines_1min)  == "STRONG" and current_candle(klines_1min)  == "RED" and pencil_wick_test(klines_1min)):
            return True

def EXIT_LONG(klines_6HOUR, klines_1HOUR, klines_1min):
    if get_unRealizedProfit(profit) == "PROFIT":
        if heikin_ashi.previous_Close(klines_1min) > heikin_ashi.current_Close(klines_1min) or current_candle(klines_1min) != "GREEN":
            return True
    else: # Cut loss when the 6HOUR is going against you
        if (current_candle(klines_6HOUR) != "GREEN" or (current_candle(klines_6HOUR) == "GREEN" and strength_of_current(klines_6HOUR) == "WEAK")) and \
           (current_candle(klines_1HOUR) == "RED" and strength_of_current(klines_1HOUR) == "STRONG"): return True

def EXIT_SHORT(klines_6HOUR, klines_1HOUR, klines_1min):
    if get_unRealizedProfit(profit) == "PROFIT":
        if heikin_ashi.previous_Close(klines_1min) < heikin_ashi.current_Close(klines_1min) or current_candle(klines_1min) != "RED":
            return True
    else: # Cut loss when the 6HOUR is going against you
        if (current_candle(klines_6HOUR) != "RED" or (current_candle(klines_6HOUR) == "RED" and strength_of_current(klines_6HOUR) == "WEAK")) and \
           (current_candle(klines_1HOUR) == "GREEN" and strength_of_current(klines_1HOUR) == "STRONG"): return True

def volume_confirmation(klines):
    if heikin_ashi.volume_weakening(klines):
        return binance_futures.current_volume(klines) > binance_futures.previous_volume(klines)
    else: return (binance_futures.current_volume(klines) > (binance_futures.previous_volume(klines) / 5))

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

def record_timestamp(kline, filename):
    if not os.path.exists("TIMESTAMP"): os.makedirs("TIMESTAMP")
    if not os.path.exists(os.path.join("TIMESTAMP", config.pair)): os.makedirs(os.path.join("TIMESTAMP", config.pair))

    with open((os.path.join("TIMESTAMP", config.pair, filename + ".txt")), "w", encoding="utf-8") as timestamp_record:
        timestamp_record.write(str(current_kline_timestamp(kline)))

def retrieve_timestamp(filename):
    with open((os.path.join("TIMESTAMP", config.pair, filename + ".txt")), "r", encoding="utf-8") as timestamp_record:
        return int(timestamp_record.read())

def current_kline_timestamp(kline):
    return kline[-1][0] # This will return <int> type of timestamp

record_timestamp(binance_futures.KLINE_INTERVAL_1HOUR(), "JACK_RABBIT")

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
    if heikin_ashi.volume_formation(klines_6HOUR) or heikin_ashi.volume_breakout(klines_6HOUR):
        if clear_direction(klines_6HOUR) == "GREEN" or clear_direction(klines_6HOUR) == "RED": 
            trade_amount = config.quantity * 3
        else: trade_amount = config.quantity * 2
    else: trade_amount = config.quantity

    return trade_amount
