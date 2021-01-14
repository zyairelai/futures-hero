import time

start           =   time.time()
position_info   =   "LONGING"           # >>> LONGING  //  SHORTING  // NO_POSITION
trend           =   "UP_TREND"          # >>> UP_TREND // DOWN_TREND // NO_TRADE_ZONE
minute_candle   =   "GREEN_CANDLE"      # >>> RED_CANDLE // GREEN_CANDLE // RED_INDECISIVE // GREEN_INDECISIVE // SOMETHING_IS_WRONG

def trade_action(position_info, trend, minute_candle):
    if position_info == "LONGING":
        if (minute_candle == "RED_CANDLE") or (minute_candle == "RED_INDECISIVE"):
            print("Action           :   CLOSE_LONG 😋")     ### CREATE SELL ORDER HERE 
        else:
            print("Action           :   HOLDING_LONG 💪🥦")

    elif position_info == "SHORTING":
        if (minute_candle == "GREEN_CANDLE") or (minute_candle == "GREEN_INDECISIVE"):
            print("Action           :   CLOSE_SHORT 😋")    ### CREATE BUY ORDER HERE 
        else:
            print("Action           :   HOLDING_SHORT 💪🩸")

    else:
        if trend == "UP_TREND":
            if (minute_candle == "GREEN_CANDLE"):
                print("Action           :   GO_LONG 🚀")    ### CREATE BUY ORDER HERE 
            else:
                print("Action           :   WAIT 🐺")
        elif trend == "DOWN_TREND":
            if (minute_candle == "RED_CANDLE"):
                print("Action           :   GO_SHORT 💥")   ### CREATE SELL ORDER HERE 
            else:
                print("Action           :   WAIT 🐺")
        else:
            print("Action           :   WAIT 🐺")

trade_action(position_info, trend, minute_candle)
print(f"Time Taken: {time.time() - start} seconds\n")
