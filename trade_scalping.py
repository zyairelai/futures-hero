stoploss   = 8  # Percentage that you are willing to lose
takeprofit = 20  # Percentage to close position when the profit hits

import config
import get_hour
import get_minute
import get_position
import get_clear_direction
import pencil_wick
import binance_futures
from datetime import datetime
from termcolor import colored

def no_trend():
    title = "ACTION           :   "
    position_info = get_position.get_position_info()
    five_minute   = get_minute.current_minute(5)
    one_minute    = get_minute.current_minute(1)

    if position_info == "LONGING":
        if binance_futures.get_open_orders() == []:
            binance_futures.set_stop_loss("LONG", stoploss)
            binance_futures.set_take_profit("LONG", takeprofit)
        print(colored(title + "HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if binance_futures.get_open_orders() == []:
            binance_futures.set_stop_loss("SHORT", stoploss)
            binance_futures.set_take_profit("SHORT", takeprofit)
        print(colored(title + "HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()
        if entry_exit_condition.ENTER_LONG(one_minute, five_minute):
            if config.live_trade: binance_futures.open_position("LONG")
            print(colored(title + "🚀 GO_LONG 🚀", "green"))

        elif entry_exit_condition.ENTER_SHORT(one_minute, five_minute):
            if config.live_trade: binance_futures.open_position("SHORT")
            print(colored(title + "💥 GO_SHORT 💥", "red"))

        else: print(title + "🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def trend():
    title = "ACTION           :   "
    position_info = get_position.get_position_info()
    if config.clear_direction: direction = get_clear_direction.clear_direction(config.main_hour)
    else: direction = get_hour.get_hour(config.main_hour)
    five_minute   = get_minute.current_minute(5)
    one_minute    = get_minute.current_minute(1)

    if position_info == "LONGING":
        if binance_futures.get_open_orders() == []:
            binance_futures.set_stop_loss("LONG", stoploss)
            binance_futures.set_take_profit("LONG", takeprofit)
        print(colored(title + "HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if binance_futures.get_open_orders() == []:
            binance_futures.set_stop_loss("SHORT", stoploss)
            binance_futures.set_take_profit("SHORT", takeprofit)
        print(colored(title + "HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()
        if direction == "UP_TREND":
            if entry_exit_condition.ENTER_LONG(one_minute, five_minute):
                if config.live_trade: binance_futures.open_position("LONG")
                print(colored(title + "🚀 GO_LONG 🚀", "green"))
            else: print("ACTION           :   🐺 WAIT 🐺")

        if direction == "DOWN_TREND":
            if entry_exit_condition.ENTER_SHORT(one_minute, five_minute):
                if config.live_trade: binance_futures.open_position("SHORT")
                print(colored(title + "💥 GO_SHORT 💥", "red"))
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print(title + "🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")