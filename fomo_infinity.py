try:

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
    from get_position import get_position_info
    from pencil_wick import pencil_wick_test
    from binance.exceptions import BinanceAPIException

    print()

    prompt_LIVE = input("Enable Live Trade? [Y/n] ")
    if prompt_LIVE == 'Y': 
        live_trade = True
        print(colored("Live Trade Enabled", "green"))
    else: live_trade = False

    prompt_TSL = input("Enable Trailing Stop? [Y/n] ")
    if prompt_TSL == 'Y': 
        trailing_stop = True
        print(colored("Trailing Stop Enabled", "green"))
    else: trailing_stop = False

    print()

    def infinity():
        title           = "ACTION           :   "
        position_info   = get_position_info()

        if position_info == "LONGING":
            print(colored("I_AM_LONGING", "green"))
            # minute_candle = get_current_minute("EXIT")
            # if (minute_candle == "RED") or (pencil_wick_test("GREEN") == "FAIL"):
            #     print(title + "💰 CLOSE_LONG 💰")
            #     if live_trade: binance_futures.close_position("LONG")
            # else: print(colored(title + "HOLDING_LONG", "green"))

        elif position_info == "SHORTING":
            print(colored("I_AM_SHORTING", "green"))
            # minute_candle = get_current_minute("EXIT")
            # if (minute_candle == "GREEN") or (pencil_wick_test("RED") == "FAIL"):
            #     print(title + "💰 CLOSE_SHORT 💰")
            #     if live_trade: binance_futures.close_position("SHORT")
            # else: print(colored(title + "HOLDING_SHORT", "red"))

        else:
            binance_futures.cancel_all_open_orders()
            
            minute_candle = get_current_minute("YOU_KNOW_I_GO_GET")
            if (minute_candle == "GREEN"):
                if (pencil_wick_test("GREEN") == "PASS"):
                    print(colored(title + "🚀 GO_LONG 🚀", "green"))
                    if live_trade: 
                        binance_futures.open_position("LONG")
                        binance_futures.set_take_profit("LONG")
                        binance_futures.set_stop_loss("LONG")

            elif (minute_candle == "RED"):
                if (pencil_wick_test("RED") == "PASS"):
                    print(colored(title + "💥 GO_SHORT 💥", "red"))
                    if live_trade: 
                        binance_futures.open_position("SHORT")
                        binance_futures.set_take_profit("SHORT")
                        binance_futures.set_stop_loss("SHORT")

            else: print(title + "🐺 WAIT 🐺")

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

    # Initialize SETUP
    if live_trade:
        if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()
        if int(binance_futures.position_information()[0].get("leverage")) != config.leverage:
            binance_futures.change_leverage()
            print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))

    while True:
        try:
            infinity()
            time.sleep(3)

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
