live_trade = True
stop_loss = False
trailing_stop = True

import os
import time
import config
from binance.client import Client
def get_timestamp(): return int(time.time() * 1000)

# Fill your own condition
position_info = "NO_POSITION"       # >>> LONGING  //  SHORTING  // NO_POSITION
trend         = "NO_TRADE_ZONE"     # >>> UP_TREND // DOWN_TREND // NO_TRADE_ZONE
minute_candle = "GREEN_INDECISIVE"  # >>> RED_CANDLE // GREEN_CANDLE // RED_INDECISIVE // GREEN_INDECISIVE // SOMETHING_IS_WRONG

def trade_action(position_info, trend, minute_candle):
    if position_info == "LONGING":
        if trend == "UP_TREND":
            if (minute_candle == "RED_CANDLE"):
                print("Action           :   💰 CLOSE_LONG 💰")
                if live_trade: client.futures_create_order(symbol=config.pair, side="SELL", type="MARKET", quantity=config.quantity, timestamp=get_timestamp())
            else: print("Action           :   ✊🥦 HOLDING_LONG 🥦💪")
        else:
            if (minute_candle != "GREEN_CANDLE") :
                print("Action           :   😭 CLOSE_LONG 😭")
                if live_trade: client.futures_create_order(symbol=config.pair, side="SELL", type="MARKET", quantity=config.quantity, timestamp=get_timestamp())
            else: print("Action           :   ✊🥦 HOLDING_LONG 🥦💪")

    elif position_info == "SHORTING":
        if trend == "DOWN_TREND":
            if (minute_candle == "GREEN_CANDLE"):
                print("Action           :   💰 CLOSE_SHORT 💰")
                if live_trade: client.futures_create_order(symbol=config.pair, side="BUY", type="MARKET", quantity=config.quantity, timestamp=get_timestamp())
            else: print("Action           :   ✊🩸 HOLDING_SHORT 🩸💪")
        else:
            if (minute_candle != "RED_CANDLE") :
                print("Action           :   😭 CLOSE_LONG 😭")
                if live_trade: client.futures_create_order(symbol=config.pair, side="BUY", type="MARKET", quantity=config.quantity, timestamp=get_timestamp())
            else: print("Action           :   ✊🥦 HOLDING_LONG 🥦💪")

    else:
        client.futures_cancel_all_open_orders(symbol=config.pair, timestamp=get_timestamp())
        if trend == "UP_TREND":
            if (minute_candle == "GREEN_CANDLE"):
                print("Action           :   🚀 GO_LONG 🚀")
                if live_trade: 
                    client.futures_create_order(symbol=config.pair, side="BUY", type="MARKET", quantity=config.quantity, timestamp=get_timestamp())
                    markPrice = float(client.futures_position_information(symbol=config.pair, timestamp=get_timestamp())[0].get('markPrice'))
                    stopPrice = round((markPrice - (markPrice * config.stoplimit / 100)), (config.round_decimal - 1))
                    client.futures_create_order(symbol=config.pair, side="SELL", type="STOP_MARKET", stopPrice=stopPrice, quantity=config.quantity, timeInForce="GTC", timestamp=get_timestamp())
            else: print("Action           :   🐺 WAIT 🐺")

        elif trend == "DOWN_TREND":
            if (minute_candle == "RED_CANDLE"):
                print("Action           :   💥 GO_SHORT 💥")
                if live_trade: 
                    client.futures_create_order(symbol=config.pair, side="SELL", type="MARKET", quantity=config.quantity, timestamp=get_timestamp())
                    markPrice = float(client.futures_position_information(symbol=config.pair, timestamp=get_timestamp())[0].get('markPrice'))
                    stopPrice = round((markPrice + (markPrice * config.stoplimit / 100)), (config.round_decimal - 1))
                    client.futures_create_order(symbol=config.pair, side="BUY", type="STOP_MARKET", stopPrice=stopPrice, quantity=config.quantity, timeInForce="GTC", timestamp=get_timestamp())
            else: print("Action           :   🐺 WAIT 🐺")
        else: print("Action           :   🐺 WAIT 🐺")

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

start = time.time()
trade_action(position_info, trend, minute_candle)
print(f"Time Taken: {time.time() - start} seconds\n")
