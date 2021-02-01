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
    from trade_double import double_confirmation
    from trade_fomo import fomo_no_trend
    from trade_scalping import scalping_no_trend
    from trade_standard import standard_main_hour
    from binance.exceptions import BinanceAPIException
    from apscheduler.schedulers.blocking import BlockingScheduler

    if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()
    if int(binance_futures.position_information()[0].get("leverage")) != config.leverage:
        binance_futures.change_leverage()
        print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))

    print("Available Strategies: ")
    print("1. double_confirmation")
    print("2. fomo_no_trend")
    print("3. scalping_no_trend")
    print("4. standard_main_hour(6)")
    prompt_TRADE = input("\nChoose Your Strategy: ") or '1'

    def choose_strategy():
        if prompt_TRADE == '1': double_confirmation(6,1)
        elif prompt_TRADE == '2': fomo_no_trend()
        elif prompt_TRADE == '3': scalping_no_trend()
        elif prompt_TRADE == '4': standard_main_hour(6)
        else: double_confirmation(6,1)

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

    scheduler = BlockingScheduler()
    scheduler.add_job(trade_action, 'interval', seconds=10)
    scheduler.start()

except KeyboardInterrupt: print("\n\nAborted.\n")
