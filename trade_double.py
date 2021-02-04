import config
import get_minute
import binance_futures
from datetime import datetime
from termcolor import colored
from get_hour import get_hour
from pencil_wick import pencil_wick_test
from get_position import get_position_info
from get_position import get_unRealizedProfit
from get_clear_direction import get_clear_direction

def with_stoploss():
    position_info = get_position_info()
    if config.clear_direction: main_hour = get_clear_direction(config.main_hour)
    else: main_hour = get_hour(config.main_hour)
    support_hour  = get_hour(1)
    five_minute   = get_minute.current_minute(5)
    one_minute    = get_minute.current_minute(1)
    emergency     = get_minute.emergency_minute()

    if position_info == "LONGING":
        if binance_futures.get_open_orders() == []: binance_futures.set_stop_loss("LONG")
        pencil_wick = pencil_wick_test("GREEN")
        if ((five_minute == "RED") or (five_minute == "RED_INDECISIVE") or (emergency == "RED") or (pencil_wick == "FAIL")) and (get_unRealizedProfit == "PROFIT"):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if binance_futures.get_open_orders() == []: binance_futures.set_stop_loss("SHORT")
        pencil_wick = pencil_wick_test("RED")
        if ((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE") or (emergency == "GREEN") or (pencil_wick == "FAIL")) and (get_unRealizedProfit == "PROFIT"):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()
        if main_hour == "UP_TREND" and support_hour == "UP_TREND":
            if (one_minute == "GREEN") and ((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                binance_futures.open_position("LONG")
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif main_hour == "DOWN_TREND" and support_hour == "DOWN_TREND":
            if (one_minute == "RED") and ((five_minute == "RED") or (five_minute == "RED_INDECISIVE")):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                binance_futures.open_position("SHORT")
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def without_stoploss():
    position_info = get_position_info()
    if config.clear_direction: main_hour = get_clear_direction(config.main_hour)
    else: main_hour = get_hour(config.main_hour)
    support_hour  = get_hour(1)
    five_minute   = get_minute.current_minute(5)
    one_minute    = get_minute.current_minute(1)
    emergency     = get_minute.emergency_minute()

    if position_info == "LONGING":
        pencil_wick = pencil_wick_test("GREEN")
        if (five_minute == "RED") or (five_minute == "RED_INDECISIVE") or (emergency == "RED") or (pencil_wick == "FAIL"):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        pencil_wick = pencil_wick_test("RED")
        if (five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE") or (emergency == "GREEN") or (pencil_wick == "FAIL"):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        binance_futures.cancel_all_open_orders()
        if main_hour == "UP_TREND" and support_hour == "UP_TREND":
            if (one_minute == "GREEN") and ((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                binance_futures.open_position("LONG")
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif main_hour == "DOWN_TREND" and support_hour == "DOWN_TREND":
            if (one_minute == "RED") and ((five_minute == "RED") or (five_minute == "RED_INDECISIVE")):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                binance_futures.open_position("SHORT")
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")