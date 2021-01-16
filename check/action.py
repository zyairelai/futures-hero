import os
import time
from binance.client import Client
live_trade = False # Always False !!!!!!
def get_timestamp(): return int(time.time() * 1000)

start    = time.time()
pair     = "BTC" + "USDT"
quantity = 0.001
threshold = 0.15

# Fill your own condition
position_info = "NO_POSITION"       # >>> LONGING  //  SHORTING  // NO_POSITION
trend         = "NO_TRADE_ZONE"     # >>> UP_TREND // DOWN_TREND // NO_TRADE_ZONE
minute_candle = "GREEN_INDECISIVE"  # >>> RED_CANDLE // GREEN_CANDLE // RED_INDECISIVE // GREEN_INDECISIVE // SOMETHING_IS_WRONG

def trade_action(position_info, trend, minute_candle):
    if position_info == "LONGING":
        if (minute_candle == "RED_CANDLE"):
            if live_trade: client.futures_create_order(symbol=pair, side="SELL", type="MARKET", quantity=quantity, timestamp=get_timestamp())
            print("Action           :   💰 CLOSE_LONG 💰")
        else:
            print("Action           :   ✊🥦 HOLDING_LONG 🥦💪")

    elif position_info == "SHORTING":
        if (minute_candle == "GREEN_CANDLE"):
            if live_trade: client.futures_create_order(symbol=pair, side="BUY", type="MARKET", quantity=quantity, timestamp=get_timestamp())
            print("Action           :   💰 CLOSE_SHORT 💰")
        else:
            print("Action           :   ✊🩸 HOLDING_SHORT 🩸💪")

    else:
        client.futures_cancel_all_open_orders(symbol=pair, timestamp=get_timestamp())
        if trend == "UP_TREND":
            if (minute_candle == "GREEN_CANDLE"):
                if live_trade: 
                    client.futures_create_order(symbol=pair, side="BUY", type="MARKET", quantity=quantity, timestamp=get_timestamp())
                    client.futures_create_order(symbol=pair, side="SELL", type="TRAILING_STOP_MARKET", callbackRate=(round(threshold*2),1), quantity=quantity, timestamp=get_timestamp())
                print("Action           :   🚀 GO_LONG 🚀")
            else:
                print("Action           :   🐺 WAIT 🐺")

        elif trend == "DOWN_TREND":
            if (minute_candle == "RED_CANDLE"):
                if live_trade: 
                    client.futures_create_order(symbol=pair, side="SELL", type="MARKET", quantity=quantity, timestamp=get_timestamp())
                    client.futures_create_order(symbol=pair, side="BUY", type="TRAILING_STOP_MARKET", callbackRate=(round(threshold*2),1), quantity=quantity, timestamp=get_timestamp())
                print("Action           :   💥 GO_SHORT 💥")
            else:
                print("Action           :   🐺 WAIT 🐺")
        else:
            print("Action           :   🐺 WAIT 🐺")

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

trade_action(position_info, trend, minute_candle)
print(f"Time Taken: {time.time() - start} seconds\n")
