try:
    import os
    import time
    import requests
    import socket
    import urllib3
    import config
    import trade_double
    import trade_fomo
    import trade_scalping
    import trade_standard
    import binance_futures
    from datetime import datetime
    from termcolor import colored
    from binance.exceptions import BinanceAPIException

    if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()
    if int(binance_futures.position_information()[0].get("leverage")) != config.leverage:
        binance_futures.change_leverage()
        print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))

    print("Available Strategies: ")
    print("1. double_confirmation")
    print("2. double_confirmation_NO_STOPLOSS")
    print("3. standard_main_hour")
    print("4. standard_main_hour_NO_STOPLOSS")
    print("5. scalping_with_trend")
    print("6. scalping_no_trend")
    print("7. fomo_no_trend")
    prompt_TRADE = input("\nCHOOSE STRATEGY  :   ") or '4'

    def choose_strategy():
        if prompt_TRADE == '1': trade_double.with_stoploss()
        elif prompt_TRADE == '2': trade_double.without_stoploss()
        elif prompt_TRADE == '3': trade_standard.with_stoploss()
        elif prompt_TRADE == '4': trade_standard.without_stoploss()
        elif prompt_TRADE == '5': trade_scalping.with_trend()
        elif prompt_TRADE == '6': trade_scalping.without_trend()
        elif prompt_TRADE == '7': trade_fomo.fomo_no_trend()
        else: trade_standard.without_stoploss()

    while True: 
        try: 
            choose_strategy()
            time.sleep(5)

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

except KeyboardInterrupt: print("\n\nAborted.\n")
