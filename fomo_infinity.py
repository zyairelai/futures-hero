try:
    live_trade = False

    import os
    import time
    import requests
    import socket
    import urllib3
    import config
    import binance_futures
    from datetime import datetime
    from termcolor import colored
    from get_minute import get_current_minute
    from get_minute import recent_minute_count
    from get_position import get_position_info
    from pencil_wick import pencil_wick_test
    from binance.exceptions import BinanceAPIException

    def infinity():
        title           = "ACTION           :   "
        position_info   = get_position_info()
        recent_minute   = recent_minute_count(5)
        minute_candle   = get_current_minute()

        if position_info == "LONGING":
            if (minute_candle == "RED") or (pencil_wick_test("GREEN") == "FAIL"):
                print(title + "💰 CLOSE_LONG 💰")
                if live_trade: binance_futures.close_position("LONG")
            else: print(colored(title + "HOLDING_LONG", "green"))

        elif position_info == "SHORTING":
            if (minute_candle == "GREEN") or (pencil_wick_test("RED") == "FAIL"):
                print(title + "💰 CLOSE_SHORT 💰")
                if live_trade: binance_futures.close_position("SHORT")
            else: print(colored(title + "HOLDING_SHORT", "red"))

        else:
            if (minute_candle == "GREEN") and (recent_minute == "GREEN"):
                if (pencil_wick_test("GREEN") == "PASS"):
                    print(colored(title + "🚀 GO_LONG 🚀", "green"))
                    if live_trade: binance_futures.open_position("LONG")

            elif (minute_candle == "RED") and (recent_minute == "RED"):
                if (pencil_wick_test("RED") == "PASS"):
                    print(colored(title + "💥 GO_SHORT 💥", "red"))
                    if live_trade: binance_futures.open_position("SHORT")

            else: print(title + "🐺 WAIT 🐺")

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

    # Initialize SETUP
    if live_trade:
        if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()
        if int(binance_futures.position_information()[0].get("leverage")) != config.leverage:
            binance_futures.change_leverage()
            print("Changed Leverage :   " + binance_futures.position_information()[0].get("leverage") + "x\n")

    while True:
        try:
            infinity()
            time.sleep(2)

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

except KeyboardInterrupt: print("\n\nAborted.\n")
