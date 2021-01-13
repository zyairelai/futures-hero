def trade_action(trend, minute_candle, position_info):
    if position_info == "LONGING":
        if trend == "UP_TREND":
            if (minute_candle == "GREEN_CANDLE") or (minute_candle == "GREEN_INDECISIVE"):
                print("Action           :   WAIT 🐺")           # WAIT
            elif (minute_candle == "RED_CANDLE") or (minute_candle == "RED_INDECISIVE"):
                print("Action           :   CLOSE_LONG 😋")     # CLOSE_LONG
            else:
                print("❗SOMETHING_IS_WRONG in trade_action()❗")
        elif trend == "DOWN_TREND":
            if (minute_candle == "GREEN_CANDLE") or (minute_candle == "GREEN_INDECISIVE"):
                print("Action           :   WAIT 🐺")           # CLOSE_LONG
            elif (minute_candle == "RED_CANDLE") or (minute_candle == "RED_INDECISIVE"):
                print("Action           :   CLOSE_LONG 😭")           # WAIT
            else:
                print("❗SOMETHING_IS_WRONG in trade_action()❗")
        else:
            if (minute_candle == "GREEN_CANDLE") or (minute_candle == "GREEN_INDECISIVE"):
                print("Action           :   WAIT 🐺")           # WAIT
            elif (minute_candle == "RED_CANDLE") or (minute_candle == "RED_INDECISIVE"):
                print("Action           :   CLOSE_LONG 😭")     # CLOSE_LONG
            else:
                print("❗SOMETHING_IS_WRONG in trade_action()❗")

    elif position_info == "SHORTING":
        if trend == "UP_TREND":
            if (minute_candle == "GREEN_CANDLE") or (minute_candle == "GREEN_INDECISIVE"):
                print("Action           :   CLOSE_SHORT 😭")    # CLOSE_SHORT
            elif (minute_candle == "RED_CANDLE") or (minute_candle == "RED_INDECISIVE"):
                print("Action           :   WAIT 🐺")           # WAIT
            else:
                print("❗SOMETHING_IS_WRONG in trade_action()❗")
        elif trend == "DOWN_TREND":
            if (minute_candle == "GREEN_CANDLE") or (minute_candle == "GREEN_INDECISIVE"):
                print("Action           :   CLOSE_SHORT 😭")    # CLOSE_SHORT
            elif (minute_candle == "RED_CANDLE") or (minute_candle == "RED_INDECISIVE"):
                print("Action           :   WAIT 🐺")           # WAIT
            else:
                print("❗SOMETHING_IS_WRONG in trade_action()❗")
        else:
            if (minute_candle == "GREEN_CANDLE") or (minute_candle == "GREEN_INDECISIVE"):
                print("Action           :   CLOSE_SHORT 😭")    # CLOSE_SHORT
            elif (minute_candle == "RED_CANDLE") or (minute_candle == "RED_INDECISIVE"):
                print("Action           :   WAIT 🐺")           # WAIT
            else:
                print("❗SOMETHING_IS_WRONG in trade_action()❗")

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