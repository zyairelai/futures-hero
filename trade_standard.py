clear_direction = True

import get_minute
import binance_futures
from datetime import datetime
from termcolor import colored
from get_hour import get_hour
from pencil_wick import pencil_wick_test
from get_position import get_pending_PNL
from get_position import get_position_info
from get_clear_direction import get_clear_direction

def with_stoploss():
    position_info = get_position_info()
    if clear_direction: direction = get_clear_direction(6)
    else: direction = get_hour(6)
    five_minute   = get_minute.current_minute(5)
    one_minute    = get_minute.current_minute(1)
    emergency     = get_minute.emergency_minute()

    if position_info == "LONGING":
        pencil_wick = pencil_wick_test("GREEN")
        if ((five_minute == "RED") or (five_minute == "RED_INDECISIVE") or (emergency == "RED") or (pencil_wick == "FAIL")) and (get_pending_PNL == "PROFIT"):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        pencil_wick = pencil_wick_test("RED")
        if ((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE") or (emergency == "GREEN") or (pencil_wick == "FAIL")) and (get_pending_PNL == "PROFIT"):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if direction == "UP_TREND":
            if (one_minute == "GREEN") and ((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")):
                if pencil_wick_test("GREEN") == "PASS":
                    print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                    binance_futures.open_position("LONG")
                else: print("ACTION           :   🐺 WAIT 🐺")
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif direction == "DOWN_TREND":
            pencil_wick = pencil_wick_test("RED")
            if (one_minute == "RED") and ((five_minute == "RED") or (five_minute == "RED_INDECISIVE")):
                if pencil_wick_test("RED") == "PASS":
                    print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                    binance_futures.open_position("SHORT")
                else: print("ACTION           :   🐺 WAIT 🐺")
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def without_stoploss():
    position_info = get_position_info()
    if clear_direction: direction = get_clear_direction(6)
    else: direction = get_hour(6)
    five_minute   = get_minute.current_minute(5)
    one_minute    = get_minute.current_minute(1)
    emergency     = get_minute.emergency_minute()

    if position_info == "LONGING":
        pencil_wick = pencil_wick_test("GREEN")
        if ((five_minute == "RED") or (five_minute == "RED_INDECISIVE") or (emergency == "RED") or (pencil_wick == "FAIL")) and (get_pending_PNL == "PROFIT"):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        pencil_wick = pencil_wick_test("RED")
        if ((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE") or (emergency == "GREEN") or (pencil_wick == "FAIL")) and (get_pending_PNL == "PROFIT"):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if direction == "UP_TREND":
            if (one_minute == "GREEN") and ((five_minute == "GREEN") or (five_minute == "GREEN_INDECISIVE")):
                if pencil_wick_test("GREEN") == "PASS":
                    print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                    binance_futures.open_position("LONG")
                else: print("ACTION           :   🐺 WAIT 🐺")
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif direction == "DOWN_TREND":
            pencil_wick = pencil_wick_test("RED")
            if (one_minute == "RED") and ((five_minute == "RED") or (five_minute == "RED_INDECISIVE")):
                if pencil_wick_test("RED") == "PASS":
                    print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                    binance_futures.open_position("SHORT")
                else: print("ACTION           :   🐺 WAIT 🐺")
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
