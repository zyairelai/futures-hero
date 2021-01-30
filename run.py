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
    from trade_fomo import fomo_trade
    from trade_double import double_confirm
    from trade_standard import standard_main_hour
    from binance.exceptions import BinanceAPIException
    from apscheduler.schedulers.blocking import BlockingScheduler

    # Initialize SETUP
    if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()
    if int(binance_futures.position_information()[0].get("leverage")) != config.leverage:
        binance_futures.change_leverage()
        print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))

    def trade_action():
        try: double_confirm(6, 1)                 # standard_main_hour(hour) // fomo_trade() // double_confirm(main, support)
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

    live_trade = True
    if live_trade:
        if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()
        if int(binance_futures.position_information()[0].get("leverage")) != config.leverage:
            binance_futures.change_leverage()
            print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))

        scheduler = BlockingScheduler()
        scheduler.add_job(trade_action, 'interval', seconds=10)
        scheduler.start()

    else:
        while True:
            try:
                # Trade Function
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
                continue

except KeyboardInterrupt: print("\n\nAborted.\n")
