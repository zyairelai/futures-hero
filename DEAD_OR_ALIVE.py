import os
import config
import heikin_ashi
import get_position
import binance_futures
from datetime import datetime
from termcolor import colored

def lets_make_some_money():
    position_info = get_position.get_position_info()
    six_hour      = heikin_ashi.get_hour(6)
    four_hour     = heikin_ashi.get_hour(4)
    one_hour      = heikin_ashi.get_hour(1)

    if position_info == "LONGING":
        if CONDITION_EXIT_LONG(six_hour, four_hour, one_hour):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")

        elif THROTTLE_LONG(six_hour):
            print("ACTION           :   🔥 THROTTLE 🔥")
            binance_futures.throttle("LONG")
            record_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())

        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if CONDITION_EXIT_SHORT(six_hour, four_hour, one_hour):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")

        elif THROTTLE_SHORT(six_hour):
            print("ACTION           :   🔥 THROTTLE 🔥")
            binance_futures.throttle("SHORT")
            record_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())

        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if (six_hour == "GREEN" or four_hour == "GREEN"):
            if GO_LONG(one_hour):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                if config.live_trade:
                    binance_futures.open_position("LONG", config.quantity)
                    record_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif (six_hour == "RED" or four_hour == "RED"):
            if GO_SHORT(one_hour):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                if config.live_trade:
                    binance_futures.open_position("SHORT", config.quantity)
                    record_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

from heikin_ashi import pattern_broken
from heikin_ashi import one_hour_exit_test
from heikin_ashi import one_minute_exit_test

def GO_LONG(one_hour):
    if  (pattern_broken("1HOUR") == "NOT_BROKEN") and \
        ((one_hour == "GREEN") or (one_hour == "GREEN_INDECISIVE")) and volume_confirmation("1HOUR"): return True

def GO_SHORT(one_hour):
    if  (pattern_broken("1HOUR") == "NOT_BROKEN") and \
        ((one_hour == "RED") or (one_hour == "RED_INDECISIVE")) and volume_confirmation("1HOUR"): return True

def CONDITION_EXIT_LONG(six_hour, four_hour, one_hour):
    if  (get_position.get_unRealizedProfit() == "PROFIT" and (one_hour == "RED" or one_hour == "RED_INDECISIVE" or six_hour != "GREEN")) or \
        (get_position.get_unRealizedProfit() == "PROFIT" and one_hour_exit_test("GREEN") and one_minute_exit_test("GREEN") and volume_confirmation("1HOUR")) or \
        (get_position.get_unRealizedProfit() == "LOSS" and ((six_hour == "RED" or four_hour == "RED") and volume_confirmation("1HOUR"))):
        return True

def CONDITION_EXIT_SHORT(six_hour, four_hour, one_hour):
    if  (get_position.get_unRealizedProfit() == "PROFIT" and (one_hour == "GREEN" or one_hour == "GREEN_INDECISIVE" or six_hour != "RED")) or \
        (get_position.get_unRealizedProfit() == "PROFIT" and one_hour_exit_test("RED") and one_minute_exit_test("RED") and volume_confirmation("1HOUR")) or \
        (get_position.get_unRealizedProfit() == "LOSS" and ((six_hour == "GREEN" or four_hour == "GREEN") and volume_confirmation("1HOUR"))):
        return True

def THROTTLE_LONG(six_hour):
    if  (get_position.get_unRealizedProfit() == "LOSS") and (six_hour != "RED" and volume_confirmation("1HOUR")) and \
        (retrieve_timestamp() != current_kline_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())):
        return True

def THROTTLE_SHORT(six_hour):
    if  (get_position.get_unRealizedProfit() == "LOSS") and (six_hour != "GREEN" and volume_confirmation("1HOUR")) and \
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
