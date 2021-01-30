import binance_futures
from datetime import datetime
from termcolor import colored
from get_hour import get_hour
from get_minute import recent_minute
from get_minute import emergency_minute
from get_position import get_position_info

def double_confirm(main, support):
    position_info = get_position_info()
    main_hour     = get_hour(main)
    support_hour  = get_hour(support)
    minute_candle = recent_minute()
    emergency     = emergency_minute()

    if position_info == "LONGING":
        if (minute_candle == "RED") or (minute_candle == "RED_INDECISIVE") or (emergency == "RED"):
            print("ACTION           :   💰 CLOSE_LONG 💰")
            binance_futures.close_position("LONG")
        else: print(colored("ACTION           :   HOLDING_LONG", "green"))

    elif position_info == "SHORTING":
        if (minute_candle == "GREEN") or (minute_candle == "GREEN_INDECISIVE") or (emergency == "GREEN"):
            print("ACTION           :   💰 CLOSE_SHORT 💰")
            binance_futures.close_position("SHORT")
        else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

    else:
        if main_hour == "UP_TREND" and support_hour == "UP_TREND":
            if (minute_candle == "GREEN") and (emergency != "RED"):
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))
                binance_futures.open_position("LONG")
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif main_hour == "DOWN_TREND" and support_hour == "DOWN_TREND":
            if (minute_candle == "RED") and (emergency != "GREEN"):
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))
                binance_futures.open_position("SHORT")
            else: print("ACTION           :   🐺 WAIT 🐺")

        else: print("ACTION           :   🐺 WAIT 🐺")

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")