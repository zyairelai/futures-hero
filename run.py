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
    from trade_fomo import fomo_no_trend
    from trade_double import double_confirmation
    from trade_standard import standard_main_hour
    from trade_scalping import scalping_no_trend
    from trade_scalping import scalping_with_trend
    from binance.exceptions import BinanceAPIException
    from apscheduler.schedulers.blocking import BlockingScheduler

    if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()
    if int(binance_futures.position_information()[0].get("leverage")) != config.leverage:
        binance_futures.change_leverage()
        print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))

    print("Available Strategies: ")
    print("1. double_confirmation")
    print("2. standard_main_hour")
    print("3. scalping_with_trend")
    print("4. scalping_no_trend")
    print("5. fomo_no_trend")
    prompt_TRADE = input("\nCHOOSE STRATEGY  :   ") or '2'

    def choose_strategy():
        if prompt_TRADE == '1': double_confirmation()
        elif prompt_TRADE == '2': standard_main_hour()
        elif prompt_TRADE == '3': scalping_with_trend()
        elif prompt_TRADE == '4': scalping_no_trend()
        elif prompt_TRADE == '5': fomo_no_trend()
        else: double_confirmation()

    def trade_action():
        try: choose_strategy()
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

    # scheduler = BlockingScheduler()
    # scheduler.add_job(trade_action, 'interval', seconds=8)
    # scheduler.start()

    while True: 
        trade_action()
        time.sleep(5)

except KeyboardInterrupt: print("\n\nAborted.\n")
