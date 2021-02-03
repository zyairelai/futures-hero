clear_direction = False
stoploss = 10 # Percentage that you are willing to lose
takeprofit = 10 # Close position when the pencentage hits

import get_minute
import binance_futures
from datetime import datetime
from termcolor import colored
from get_hour import get_hour
from get_minute import emergency_minute
from get_position import get_position_info
from get_clear_direction import get_clear_direction

def without_trend():
    title = "ACTION           :   "
    position_info = get_position_info()
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
        if (one_minute == "GREEN") and ((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")):
            binance_futures.open_position("LONG")
            print(colored(title + "🚀 GO_LONG 🚀", "green"))

        elif (one_minute == "RED") and ((five_minute == "RED") or (five_minute == "RED_INDECISIVE")):
            binance_futures.open_position("SHORT")
            print(colored(title + "💥 GO_SHORT 💥", "red"))

        else: print(title + "🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def with_trend():
    title = "ACTION           :   "
    position_info = get_position_info()
    if clear_direction: direction = get_clear_direction(6)
    else: direction = get_hour(6)
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
            if (one_minute == "GREEN") and ((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")):
                binance_futures.open_position("LONG")
                print(colored(title + "🚀 GO_LONG 🚀", "green"))
            else: print("ACTION           :   🐺 WAIT 🐺")

        if direction == "DOWN_TREND":
            if (one_minute == "RED") and ((five_minute == "RED") or (five_minute == "RED_INDECISIVE")):
                binance_futures.open_position("SHORT")
                print(colored(title + "💥 GO_SHORT 💥", "red"))
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print(title + "🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")