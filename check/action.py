import time

# get_current_trend() >>> DOWN_TREND // UP_TREND // NO_TRADE_ZONE
# get_minute_candle() >>> RED_CANDLE // GREEN_CANDLE // RED_INDECISIVE // GREEN_INDECISIVE // CLOSE_ALL_POSITION

start           =   time.time()
trend           =   "UP_TREND"
minute_candle   =   "RED_CANDLE"

def get_trade_action(trend, minute_candle):
    if trend == "NO_TRADE_ZONE":
        # Close all position at and quit trading
        print("Action           :   Close Everything and Wait 🦄")
        trade_action = "CLOSE_ALL_POSITION"

    elif (trend == "UP_TREND"):
        if (minute_candle == "GREEN_CANDLE"):
            print("Action           :   GO_LONG 🚀")
            trade_action = "GO_LONG"
        elif (minute_candle == "GREEN_INDECISIVE"):
            print("Action           :   WAIT 🐺")
            trade_action = "WAIT"
        elif (minute_candle == "RED_CANDLE") or (minute_candle == "RED_INDECISIVE"):
            print("Action           :   CLOSE_LONG 😋 && WAIT 🐺")
            trade_action = "CLOSE_LONG"

    elif (trend == "DOWN_TREND"):
        if (minute_candle == "RED_CANDLE"):
            print("Action           :   GO_SHORT 💥")
            trade_action = "GO_SHORT"
        elif (minute_candle == "RED_INDECISIVE"):
            print("Action           :   WAIT 🐺")
            trade_action = "WAIT"
        elif (minute_candle == "GREEN_CANDLE") or (minute_candle == "GREEN_INDECISIVE"):
            print("Action           :   CLOSE_SHORT 😋 && WAIT 🐺")
            trade_action = "CLOSE_SHORT"

    else:
        print("❗Something in get_trade_action() is going wrong❗")
        trade_action = "CLOSE_ALL_POSITION"

    return trade_action

result = get_trade_action(trend, minute_candle)
print("\nThe <action.py> return value is : " + result + "\n")
print(f"Time Taken: {time.time() - start} seconds\n")
