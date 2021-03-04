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
    five_minute   = heikin_ashi.get_current_minute(5)
    one_minute    = heikin_ashi.get_current_minute(1)
    previous_volume = binance_futures.get_volume("PREVIOUS", "1HOUR")
    current_volume  = binance_futures.get_volume("CURRENT", "1HOUR")

    if position_info == "LONGING":
        if DIRECTION_CHANGE_EXIT_LONG(one_hour, previous_volume, current_volume):
            if  (get_position.get_unRealizedProfit() == "PROFIT" and heikin_ashi.one_hour_exit_test("GREEN")) or \
                (get_position.get_unRealizedProfit() == "LOSS" and (six_hour == "RED" and volume_confirmation(previous_volume, current_volume))):
                print("ACTION           :   💰 CLOSE_LONG 💰")
                binance_futures.close_position("LONG")
            elif get_position.get_unRealizedProfit() == "LOSS" and retrieve_timestamp() != current_kline_timestamp(binance_futures.KLINE_INTERVAL_2HOUR()):
                print("ACTION           :   🔥 THROTTLE 🔥")
                binance_futures.throttle("LONG")
                record_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())
            else: print(colored("ACTION           :   HOLDING_LONG", "green"))
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if DIRECTION_CHANGE_EXIT_SHORT(one_hour, previous_volume, current_volume):
            if  (get_position.get_unRealizedProfit() == "PROFIT" and heikin_ashi.one_hour_exit_test("RED")) or \
                (get_position.get_unRealizedProfit() == "LOSS" and (six_hour == "GREEN" and volume_confirmation(previous_volume, current_volume))):
                print("ACTION           :   💰 CLOSE_SHORT 💰")
                binance_futures.close_position("SHORT")
            elif get_position.get_unRealizedProfit() == "LOSS" and retrieve_timestamp() != current_kline_timestamp(binance_futures.KLINE_INTERVAL_2HOUR()):
                print("ACTION           :   🔥 THROTTLE 🔥")
                binance_futures.throttle("SHORT")
                record_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())
            else: print(colored("ACTION           :   HOLDING_SHORT", "red"))
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if (six_hour == "GREEN" or four_hour == "GREEN") and volume_confirmation(previous_volume, current_volume):
            if GO_LONG(one_minute, five_minute, one_hour):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                if config.live_trade:
                    binance_futures.open_position("LONG", config.quantity)
                    record_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif (six_hour == "RED" or four_hour == "RED") and volume_confirmation(previous_volume, current_volume):
            if GO_SHORT(one_minute, five_minute, one_hour):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                if config.live_trade:
                    binance_futures.open_position("SHORT", config.quantity)
                    record_timestamp(binance_futures.KLINE_INTERVAL_2HOUR())
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

from heikin_ashi import pattern_broken
from heikin_ashi import pencil_wick_test

def GO_LONG(one_minute, five_minute, one_hour):
    if ((pattern_broken("5MINUTE") == "NOT_BROKEN") and (pattern_broken("1HOUR") == "NOT_BROKEN")) and \
       ((one_minute == "GREEN") and (pencil_wick_test("GREEN", "1MINUTE") == "PASS")) and \
       (((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")) and (pencil_wick_test("GREEN", "5MINUTE") == "PASS")) and \
       ((one_hour == "GREEN") or (one_hour == "GREEN_INDECISIVE") and (pencil_wick_test("RED", "1HOUR") == "FAIL")): return True

def GO_SHORT(one_minute, five_minute, one_hour):
    if ((pattern_broken("5MINUTE") == "NOT_BROKEN") and (pattern_broken("1HOUR") == "NOT_BROKEN")) and \
       ((one_minute == "RED") and (pencil_wick_test("RED", "1MINUTE") == "PASS")) and \
       (((five_minute == "RED") or (five_minute == "RED_INDECISIVE")) and (pencil_wick_test("RED", "5MINUTE") == "PASS")) and \
       ((one_hour == "RED") or (one_hour == "RED_INDECISIVE") and (pencil_wick_test("GREEN", "1HOUR") == "FAIL")): return True

def DIRECTION_CHANGE_EXIT_LONG(one_hour, previous_volume, current_volume):
    if ((one_hour == "RED") or (one_hour == "RED_INDECISIVE")) and volume_confirmation(previous_volume, current_volume): return True

def DIRECTION_CHANGE_EXIT_SHORT(one_hour, previous_volume, current_volume):
    if ((one_hour == "GREEN") or (one_hour == "GREEN_INDECISIVE")) and volume_confirmation(previous_volume, current_volume): return True

def volume_confirmation(previous_volume, current_volume):
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

