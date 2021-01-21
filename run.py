try:
    live_trade = True

    import os
    import time
    import requests
    import socket
    import urllib3
    from datetime import datetime
    from termcolor import colored
    from binance.client import Client
    from binance.exceptions import BinanceAPIException
    import config
    import place_order
    from keys import client
    from get_trend import get_current_trend
    from get_1_minute import get_current_minute
    from get_3_minute import get_3_minute
    from get_position import get_position_info
    def get_timestamp(): return int(time.time() * 1000)

    def trade_action():
        position_info   = get_position_info()
        trend           = get_current_trend()
        minute_candle   = get_current_minute()
        fakeout_candle  = get_3_minute()

        if position_info == "LONGING":
            if (minute_candle == "RED_CANDLE"):# and (fakeout_candle == "RED_CANDLE"):
                print("ACTION           :   💰 CLOSE_LONG 💰")
                if live_trade: place_order.close_position("LONG")
            else: print(colored("ACTION           :   ✊HOLDING_LONG💪", "green"))

        elif position_info == "SHORTING":
            if (minute_candle == "GREEN_CANDLE"):# and (fakeout_candle == "GREEN_CANDLE"):
                print("ACTION           :   💰 CLOSE_SHORT 💰")
                if live_trade: place_order.close_position("SHORT")
            else: print(colored("ACTION           :   ✊HOLDING_SHORT💪", "red"))

        else:
            client.futures_cancel_all_open_orders(symbol=config.pair, timestamp=get_timestamp())
            if trend == "UP_TREND":
                if (minute_candle == "GREEN_CANDLE"):
                    print(colored("Action           :   🚀 GO_LONG 🚀", "green"))
                    if live_trade: place_order.place_order("LONG")
                else: print("ACTION           :   🐺 WAIT 🐺")

            elif trend == "DOWN_TREND":
                if (minute_candle == "RED_CANDLE"):
                    print(colored("Action           :   💥 GO_SHORT 💥", "red"))
                    if live_trade: place_order.place_order("SHORT")
                else: print("ACTION           :   🐺 WAIT 🐺")

            elif trend == "COOLDOWN":
                print("ACTION           :   🐺 WAIT for COOLDOWN 🐺")
                
            else:
                print("ACTION           :   🐺 WAIT 🐺")

    client.futures_change_leverage(symbol=config.pair, leverage=config.leverage, timestamp=get_timestamp())

    while True:
        try:    trade_action()
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