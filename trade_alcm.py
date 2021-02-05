import config
import entry_exit
import get_hour
import get_minute
import get_position
import get_clear_direction
import binance_futures
from datetime import datetime
from termcolor import colored
from pencil_wick import pencil_wick_test

def dead_or_alive():
    if int(binance_futures.position_information()[0].get("leverage")) != int(config.leverage/2):
        binance_futures.change_leverage(int(config.leverage/2))
        print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))

    position_info = get_position.get_position_info()
    if config.clear_direction: direction = get_clear_direction.clear_direction(config.main_hour)
    else: direction = get_hour.get_hour(config.main_hour)
    five_minute   = get_minute.current_minute(5)
    one_minute    = get_minute.current_minute(1)
    emergency     = get_minute.emergency_minute()

    if position_info == "LONGING":
        if (get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_LONG(five_minute, emergency):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if (get_position.get_unRealizedProfit() == "PROFIT") and entry_exit.CLOSE_SHORT(five_minute, emergency):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()
        if direction == "UP_TREND":
            if entry_exit.GO_LONG(one_minute, five_minute):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                if config.live_trade: binance_futures.open_position("LONG")
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif direction == "DOWN_TREND":
            if entry_exit.GO_SHORT(one_minute, five_minute):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                if config.live_trade: binance_futures.open_position("SHORT")
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
