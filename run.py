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
    from get_minute import get_current_minute
    from get_position import get_position_info
    def get_timestamp(): return int(time.time() * 1000)

    def trade_action():
        position_info   = get_position_info()
        trend           = get_current_trend()
        title           = "ACTION           :   "

        if position_info == "LONGING":
            minute_candle = get_current_minute("ENTRY")
            if (minute_candle == "RED_CANDLE"):
                print(title + "💰 CLOSE_LONG 💰")
                if live_trade: place_order.close_position("LONG")
            else: print(colored("✊ HOLDING_LONG 💪", "green"))

        elif position_info == "SHORTING":
            minute_candle = get_current_minute("EXIT")
            if (minute_candle == "GREEN_CANDLE"):
                print(title + "💰 CLOSE_SHORT 💰")
                if live_trade: place_order.close_position("SHORT")
            else: print(colored(title + "✊ HOLDING_SHORT 💪", "red"))

        else:
            minute_candle = get_current_minute("YOU_KNOW_I_GO_GET")
            if trend == "UP_TREND":
                if (minute_candle == "GREEN_CANDLE"):
                    print(colored(title + "🚀 GO_LONG 🚀", "green"))
                    if live_trade: place_order.place_order("LONG")
                else: print(title + "🐺 WAIT 🐺")

            elif trend == "DOWN_TREND":
                if (minute_candle == "RED_CANDLE"):
                    print(colored(title + "💥 GO_SHORT 💥", "red"))
                    if live_trade: place_order.place_order("SHORT")
                else: print(title + "🐺 WAIT 🐺")
                
            else: print(title + "🐺 WAIT 🐺")

    # Initialize SETUP
    client.futures_change_leverage(symbol=config.pair, leverage=config.leverage, timestamp=get_timestamp())
    if client.futures_position_information(symbol=config.pair, timestamp=get_timestamp)[0].get('marginType') != "isolated":
        client.futures_change_margin_type(symbol=config.pair, marginType="ISOLATED", timestamp=get_timestamp)

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
        time.sleep(1)

except KeyboardInterrupt: print("\n\nAborted.\n")
