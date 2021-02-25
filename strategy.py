import config
import entry_exit
import heikin_ashi
import get_position
import trade_amount
import binance_futures
from datetime import datetime
from termcolor import colored

volume_prefix = 5

def dead_or_alive():
    position_info = get_position.get_position_info()
    direction    = heikin_ashi.get_clear_direction(6)
    one_hour     = heikin_ashi.get_hour(1)
    five_minute  = heikin_ashi.get_current_minute(5)
    one_minute   = heikin_ashi.get_current_minute(1)

    if position_info == "LONGING":
        if entry_exit.DIRECTION_CHANGE_EXIT_LONG(one_hour) or ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG()):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if entry_exit.DIRECTION_CHANGE_EXIT_SHORT(one_hour) or ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_SHORT()):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()
        firstrun_volume = binance_futures.get_volume("FIRSTRUN", "6HOUR")
        previous_volume = binance_futures.get_volume("PREVIOUS", "6HOUR")
        current_volume  = binance_futures.get_volume("CURRENT", "6HOUR")

        if   (firstrun_volume < previous_volume) and (previous_volume < current_volume): trade_amount = config.quantity * 3
        elif (firstrun_volume > previous_volume) and (previous_volume > current_volume): trade_amount = config.quantity * 1
        else:
            if current_volume > previous_volume: trade_amount = config.quantity * 2
            else: trade_amount = config.quantity * 1

        if direction == "GREEN" and ((previous_volume / volume_prefix) > current_volume):
            if entry_exit.GO_LONG(one_minute, five_minute, one_hour):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                if config.live_trade: binance_futures.open_position("LONG", trade_amount)
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif direction == "RED" and ((previous_volume / volume_prefix) > current_volume):
            if entry_exit.GO_SHORT(one_minute, five_minute, one_hour):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                if config.live_trade: binance_futures.open_position("SHORT", trade_amount)
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def one_shot_one_kill():
    position_info = get_position.get_position_info()
    direction    = heikin_ashi.get_clear_direction(6)
    one_hour     = heikin_ashi.get_hour(1)
    five_minute  = heikin_ashi.get_current_minute(5)
    one_minute   = heikin_ashi.get_current_minute(1)

    if position_info == "LONGING":
        if entry_exit.DIRECTION_CHANGE_EXIT_LONG(one_hour) or ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG()):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if entry_exit.DIRECTION_CHANGE_EXIT_SHORT(one_hour) or ((get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_SHORT()):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        # firstrun_volume = binance_futures.get_volume("FIRSTRUN", "6HOUR")
        previous_volume = binance_futures.get_volume("PREVIOUS", "6HOUR")
        current_volume  = binance_futures.get_volume("CURRENT", "6HOUR")

        if direction == "GREEN" and ((previous_volume / volume_prefix) > current_volume):
            if entry_exit.GO_LONG(one_minute, five_minute, one_hour):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                if config.live_trade: binance_futures.open_position("LONG", config.quantity)
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif direction == "RED" and ((previous_volume / volume_prefix) > current_volume):
            if entry_exit.GO_SHORT(one_minute, five_minute, one_hour):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                if config.live_trade: binance_futures.open_position("SHORT", config.quantity)
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")
    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
