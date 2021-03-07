import os
import config
import heikin_ashi
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored

live_trade = config.live_trade

def DEAD_OR_ALIVE():
    position_info = get_position.get_position_info()
    six_hour      = heikin_ashi.get_hour(6)
    four_hour     = heikin_ashi.get_hour(4)
    one_hour      = heikin_ashi.get_hour(1)

    if position_info == "LONGING":
        if get_position.get_unRealizedProfit() == "PROFIT":
            if EXIT_LONG_TAKE_PROFIT(one_hour, four_hour, six_hour):            # Take Profit
                print("ACTION           :   💰 CLOSE_LONG 💰")
                if live_trade: binance_futures.close_position("LONG")
            else: print(colored("ACTION           :   HOLDING_LONG", "green"))
        
        elif get_position.get_unRealizedProfit() == "LOSS":
            if THROTTLE_LONG(four_hour, six_hour):                                  # Throttle - Pushing the initial entry price higher
                print("ACTION           :   🔥 THROTTLE 🔥")
                record_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())
                if live_trade: binance_futures.throttle("LONG")
            elif TAKE_LOSS("LONG", four_hour, six_hour):                            # Stoploss - Only take a loss when direction change against you
                print("ACTION           :   😭 CLOSE_LONG 😭")
                if live_trade: binance_futures.close_position("LONG")
            else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if get_position.get_unRealizedProfit() == "PROFIT":
            if EXIT_SHORT_TAKE_PROFIT(one_hour, four_hour, six_hour):               # Take Profit
                print("ACTION           :   💰 CLOSE_SHORT 💰")
                if live_trade: binance_futures.close_position("SHORT")
            else: print(colored("ACTION           :   HOLDING_SHORT", "red"))
        
        elif get_position.get_unRealizedProfit() == "LOSS":
            if THROTTLE_SHORT(four_hour, six_hour):                                 # Throttle - Pulling the initial entry price power
                print("ACTION           :   🔥 THROTTLE 🔥")
                record_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())
                if live_trade: binance_futures.throttle("SHORT")
            elif TAKE_LOSS("SHORT", four_hour, six_hour):                           # Stoploss - Only take a loss when direction change against you
                print("ACTION           :   😭 CLOSE_SHORT 😭")
                if live_trade: binance_futures.close_position("SHORT")
            else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if (four_hour == "GREEN" or six_hour == "GREEN"):
            if GO_LONG(one_hour):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                record_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())
                if live_trade: binance_futures.open_position("LONG", config.quantity)
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif (four_hour == "RED" or six_hour == "RED"):
            if GO_SHORT(one_hour):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                record_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())
                if live_trade: binance_futures.open_position("SHORT", config.quantity)
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")


def JACK_RABBIT():
    position_info = get_position.get_position_info()
    six_hour      = heikin_ashi.get_hour(6)
    four_hour     = heikin_ashi.get_hour(4)
    one_hour      = heikin_ashi.get_hour(1)

    if position_info == "LONGING":
        if  EXIT_LONG_TAKE_PROFIT(one_hour, four_hour, six_hour) or TAKE_LOSS("LONG", four_hour, six_hour):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            if live_trade: binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if  EXIT_SHORT_TAKE_PROFIT(one_hour, four_hour, six_hour) or TAKE_LOSS("SHORT", four_hour, six_hour):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            if live_trade: binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if (four_hour == "GREEN" or six_hour == "GREEN"):
            if GO_LONG(one_hour):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                record_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())
                if live_trade: binance_futures.open_position("LONG", config.quantity)
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif (four_hour == "RED" or six_hour == "RED"):
            if GO_SHORT(one_hour):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                record_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())
                if live_trade: binance_futures.open_position("SHORT", config.quantity)
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

from heikin_ashi import strength_of
from heikin_ashi import pattern_broken
from heikin_ashi import one_hour_exit_test

def GO_LONG(one_hour):
    if  (strength_of("4HOUR") == "STRONG" or strength_of("6HOUR") == "STRONG") and \
        (strength_of("1HOUR") == "STRONG") and pattern_broken("1HOUR") == "NOT_BROKEN" and \
        (one_hour == "GREEN" or one_hour == "GREEN_INDECISIVE") and \
        volume_confirmation("1HOUR"): return True

def GO_SHORT(one_hour):
    if  (strength_of("4HOUR") == "STRONG" or strength_of("6HOUR") == "STRONG") and \
        (strength_of("1HOUR") == "STRONG") and pattern_broken("1HOUR") == "NOT_BROKEN" and \
        (one_hour == "RED" or one_hour == "RED_INDECISIVE") and \
        volume_confirmation("1HOUR"): return True

def EXIT_LONG_TAKE_PROFIT(one_hour, four_hour, six_hour):
    if  (((one_hour_exit_test("LONG") or one_hour == "RED" or one_hour == "RED_INDECISIVE") and volume_confirmation("1HOUR")) or \
        (six_hour  == "GREEN" or six_hour  == "GREEN_INDECISIVE" and strength_of("6HOUR") == "WEAK") or \
        (four_hour == "GREEN" or four_hour == "GREEN_INDECISIVE" and strength_of("4HOUR") == "WEAK")): return True

def EXIT_SHORT_TAKE_PROFIT(one_hour, four_hour, six_hour):
    if  (((one_hour_exit_test("SHORT") or one_hour == "GREEN" or one_hour == "GREEN_INDECISIVE") and volume_confirmation("1HOUR")) or \
        (six_hour == "RED" or six_hour  == "RED_INDECISIVE" and strength_of("6HOUR") == "WEAK") or \
        (four_hour == "RED" or four_hour == "RED_INDECISIVE" and strength_of("4HOUR") == "WEAK")): return True

def TAKE_LOSS(POSITION, four_hour, six_hour):
    if POSITION == "LONG":
        if  ((four_hour == "RED" or four_hour == "RED_INDECISIVE") and strength_of("4HOUR") == "STRONG") or \
            ((six_hour  == "RED" or six_hour  == "RED_INDECISIVE") and strength_of("6HOUR") == "STRONG"): return True

    elif POSITION == "SHORT":
        if  ((four_hour == "GREEN" or four_hour == "GREEN_INDECISIVE") and strength_of("4HOUR") == "STRONG") or \
            ((six_hour  == "GREEN" or six_hour  == "GREEN_INDECISIVE") and strength_of("6HOUR") == "STRONG"): return True

def THROTTLE_LONG(four_hour, six_hour):
    if  ((four_hour != "RED" or six_hour != "RED") and volume_confirmation("1HOUR")) and \
        (retrieve_timestamp() != current_kline_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())):
        return True

def THROTTLE_SHORT(four_hour, six_hour):
    if  ((four_hour != "RED" or six_hour != "GREEN") and volume_confirmation("1HOUR")) and \
        (retrieve_timestamp() != current_kline_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())):
        return True

def volume_confirmation(INTERVAL):
    previous_volume = binance_futures.get_volume("PREVIOUS", INTERVAL)
    current_volume = binance_futures.get_volume("CURRENT", INTERVAL)
    return (current_volume > (previous_volume / 5))

def record_timestamp(kline):
    current_timestamp = current_kline_timestamp(kline)
    if not os.path.exists("Timestamp_Record"): os.makedirs("Timestamp_Record")
    with open((os.path.join("Timestamp_Record", config.pair + ".txt")), "w", encoding="utf-8") as timestamp_record:
        timestamp_record.write(str(current_timestamp))

def retrieve_timestamp():
    with open((os.path.join("Timestamp_Record", config.pair + ".txt")), "r", encoding="utf-8") as timestamp_record:
        return int(timestamp_record.read())

def current_kline_timestamp(kline):
    return kline[-1][0] # This will return <int> type of timestamp
