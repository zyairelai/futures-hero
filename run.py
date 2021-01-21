try:
    live_trade = True
    stop_loss  = False
    trailing_stop = False

    import os
    import time
    import requests
    import socket
    import urllib3
    from binance.client import Client
    from binance.exceptions import BinanceAPIException
    from datetime import datetime
    import config
    import place_order
    from keys import client
    from get_trend import get_current_trend
    from get_minute import get_current_minute
    from get_position import get_position_info
    def get_timestamp(): return int(time.time() * 1000)

    def trade_action(position_info, trend, minute_candle):
        if position_info == "LONGING":
            if trend == "UP_TREND":
                if (minute_candle == "RED_CANDLE"):
                    print("Action           :   💰 CLOSE_LONG 💰")
                    if live_trade: place_order.close_position("LONG")
                else: print("Action           :   ✊🥦 HOLDING_LONG 🥦💪")
            else:
                # HERE IS FOR STOP LOSS DOUBLE ORDER HANDLING
                if not (minute_candle == "GREEN_CANDLE") or not (minute_candle == "WEAK_GREEN"):
                    print("Action           :   😭 CLOSE_LONG 😭")
                    if live_trade: place_order.close_position("LONG")
                else: print("Action           :   ✊🥦 HOLDING_LONG 🥦💪")

        elif position_info == "SHORTING":
            if trend == "DOWN_TREND":
                if (minute_candle == "GREEN_CANDLE"):
                    print("Action           :   💰 CLOSE_SHORT 💰")
                    if live_trade: place_order.close_position("SHORT")
                else: print("Action           :   ✊🩸 HOLDING_SHORT 🩸💪")
            else:
                # HERE IS FOR STOP LOSS DOUBLE ORDER HANDLING
                if not (minute_candle == "RED_CANDLE") or not (minute_candle == "WEAK_RED"):
                    print("Action           :   😭 CLOSE_LONG 😭")
                    if live_trade: place_order.close_position("SHORT")
                else: print("Action           :   ✊🥦 HOLDING_LONG 🥦💪")

        else:
            client.futures_cancel_all_open_orders(symbol=config.pair, timestamp=get_timestamp())
            if trend == "UP_TREND":
                if (minute_candle == "GREEN_CANDLE"):
                    print("Action           :   🚀 GO_LONG 🚀")
                    if live_trade:
                        place_order.place_order("LONG")
                        if trailing_stop: place_order.set_trailing_stop("LONG")
                        if stop_loss: place_order.set_stop_loss("LONG")
                else: print("Action           :   🐺 WAIT 🐺")

            elif trend == "DOWN_TREND":
                if (minute_candle == "RED_CANDLE"):
                    print("Action           :   💥 GO_SHORT 💥")
                    if live_trade:
                        place_order.place_order("SHORT")
                        if trailing_stop: place_order.set_trailing_stop("SHORT")
                        if stop_loss: place_order.set_stop_loss("SHORT")
                else: print("Action           :   🐺 WAIT 🐺")

            elif trend == "COOLDOWN":
                print("Action           :   🐺 WAIT for COOLDOWN 🐺")

            else:
                print("Action           :   🐺 WAIT 🐺")

    client.futures_change_leverage(symbol=config.pair, leverage=config.leverage, timestamp=get_timestamp())

    while True:
        try:
            trade_action(get_position_info(), get_current_trend(), get_current_minute())
        except (BinanceAPIException,
                ConnectionResetError,
                socket.timeout,
                urllib3.exceptions.ProtocolError,
                urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout) as e:

            if not os.path.exists("Error_Message"): os.makedirs("Error_Message")
            with open((os.path.join("Error_Message", config.pair + ".txt")), "a") as error_message:
                error_message.write("[!] " + config.pair + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n")
                error_message.write(str(e) + "\n\n")
            continue

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")
        time.sleep(5)

except KeyboardInterrupt: print("\n\nAborted.\n")