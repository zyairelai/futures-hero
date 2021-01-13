import time

start           =   time.time()
position_info   =   "LONGING"           # >>> LONGING  //  SHORTING  // NO_POSITION
trend           =   "UP_TREND"          # >>> UP_TREND // DOWN_TREND // NO_TRADE_ZONE
minute_candle   =   "RED_CANDLE"        # >>> RED_CANDLE // GREEN_CANDLE // RED_INDECISIVE // GREEN_INDECISIVE // SOMETHING_IS_WRONG

def trade_action(position_info, trend, minute_candle):
    if position_info == "LONGING":
        if (minute_candle == "GREEN_CANDLE") or (minute_candle == "GREEN_INDECISIVE"):
            print("Action           :   WAIT 🐺")           # WAIT
            result = "WAIT"
        elif (minute_candle == "RED_CANDLE") or (minute_candle == "RED_INDECISIVE"):
            print("Action           :   CLOSE_LONG 😋")     # CLOSE_LONG
            result = "CLOSE_LONG"
        else:
            print("❗SOMETHING_IS_WRONG in trade_action()❗")
            result = "SOMETHING_IS_WRONG"

    elif position_info == "SHORTING":
        if (minute_candle == "GREEN_CANDLE") or (minute_candle == "GREEN_INDECISIVE"):
            print("Action           :   CLOSE_SHORT 😋")    # CLOSE_SHORT
            result = "CLOSE_SHORT"
        elif (minute_candle == "RED_CANDLE") or (minute_candle == "RED_INDECISIVE"):
            print("Action           :   WAIT 🐺")           # WAIT
            result = "WAIT"
        else:
            print("❗SOMETHING_IS_WRONG in trade_action()❗")
            result = "SOMETHING_IS_WRONG"

    else:
        if trend == "UP_TREND":
            if (minute_candle == "GREEN_CANDLE"):
                print("Action           :   GO_LONG 🚀")
                result = "GO_LONG"
            else:
                print("Action           :   WAIT 🐺")       # WAIT
                result = "WAIT"
        elif trend == "DOWN_TREND":
            if (minute_candle == "RED_CANDLE"):
                print("Action           :   GO_SHORT 💥")
                result = "GO_SHORT"
            else:
                print("Action           :   WAIT 🐺")       # WAIT
                result = "WAIT"
        else:
            print("Action           :   WAIT 🐺")           # WAIT
            result = "WAIT"

    return result

result = trade_action(position_info, trend, minute_candle)
print("\nThe <action.py> return value is : " + result + "\n")
print(f"Time Taken: {time.time() - start} seconds\n")
