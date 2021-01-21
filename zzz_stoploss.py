live_trade = False
stop_loss = False
trailing_stop = False

import config
import place_order
import time
from keys import client
from termcolor import colored
def get_timestamp(): return int(time.time() * 1000)

def trade_action(position_info, trend, minute_candle):
    if position_info == "LONGING":
        if trend == "UP_TREND":
            if (minute_candle == "RED_CANDLE"):
                print("ACTION           :   💰 CLOSE_LONG 💰")
                if live_trade: place_order.close_position("LONG")
            else: print(colored("ACTION           :   ✊🥦 HOLDING_LONG 🥦💪", "green"))

        else: # HERE IS FOR STOP LOSS DOUBLE ORDER HANDLING
            if not (minute_candle == "GREEN_CANDLE") or not (minute_candle == "WEAK_GREEN"):
                print("ACTION           :   😭 CLOSE_LONG 😭")
                if live_trade: place_order.close_position("LONG")
            else: print(colored("ACTION           :   ✊🥦 HOLDING_LONG 🥦💪", "green"))

    elif position_info == "SHORTING":
        if trend == "DOWN_TREND":
            if (minute_candle == "GREEN_CANDLE"):
                print("ACTION           :   💰 CLOSE_SHORT 💰")
                if live_trade: place_order.close_position("SHORT")
            else: print(colored("ACTION           :   ✊🩸 HOLDING_SHORT 🩸💪", "red"))

        else: # HERE IS FOR STOP LOSS DOUBLE ORDER HANDLING
            if not (minute_candle == "RED_CANDLE") or not (minute_candle == "WEAK_RED"):
                print("ACTION           :   😭 CLOSE_LONG 😭")
                if live_trade: place_order.close_position("SHORT")
            else: print(colored("ACTION           :   ✊🩸 HOLDING_SHORT 🩸💪", "red"))

    else:
        client.futures_cancel_all_open_orders(symbol=config.pair, timestamp=get_timestamp())
        if trend == "UP_TREND":
            if (minute_candle == "GREEN_CANDLE"):
                print(colored("Action           :   🚀 GO_LONG 🚀", "green"))
                if live_trade:
                    place_order.place_order("LONG")
                    if trailing_stop: place_order.set_trailing_stop("LONG")
                    if stop_loss: place_order.set_stop_loss("LONG")
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif trend == "DOWN_TREND":
            if (minute_candle == "RED_CANDLE"):
                print(colored("Action           :   💥 GO_SHORT 💥", "red"))
                if live_trade:
                    place_order.place_order("SHORT")
                    if trailing_stop: place_order.set_trailing_stop("SHORT")
                    if stop_loss: place_order.set_stop_loss("SHORT")
            else: print("ACTION           :   🐺 WAIT 🐺")

        elif trend == "COOLDOWN":
            print("ACTION           :   🐺 WAIT for COOLDOWN 🐺")

        else:
            print("ACTION           :   🐺 WAIT 🐺")
