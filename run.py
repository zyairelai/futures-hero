try:
    import os
    import time
    import requests
    import socket
    import urllib3
    import config
    import get_hour
    import dead_or_alive
    import binance_futures
    from datetime import datetime
    from termcolor import colored
    from binance.exceptions import BinanceAPIException
    from apscheduler.schedulers.blocking import BlockingScheduler

    if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()
    if int(binance_futures.position_information()[0].get("leverage")) != config.leverage:
        binance_futures.change_leverage(config.leverage)
        print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))

    use_SL = input("Use Stoploss? [Y/n] ") or 'n'

    if use_SL == 'Y':
        print(colored("Stoploss Enabled", "green"))
        use_stoploss = True
        percentage = input("Percentage % that you are willing to lose (Default 70): ") or '70'
        print(colored("Stoploss         :   " + percentage + "%\n"))
    else:
        print(colored("Stoploss Disabled\n", "red"))
        use_stoploss = False
        percentage = 0

    def added_to_job():
        if get_hour.get_hour(6) == "NO_TRADE_ZONE": dead_or_alive.fomo(use_stoploss, int(percentage))
        else: dead_or_alive.dead_or_alive(use_stoploss, int(percentage))

    while True:
        try:
            # added_to_job()
            # time.sleep(8)

            scheduler = BlockingScheduler()
            scheduler.add_job(added_to_job, 'cron', second='0,5,10,15,20,25,30,35,40,45,50,55')
            scheduler.start()

        except (BinanceAPIException,
                ConnectionResetError,
                socket.timeout,
                urllib3.exceptions.ProtocolError,
                urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout) as e:

            if not os.path.exists("Error_Message"): os.makedirs("Error_Message")
            with open((os.path.join("Error_Message", config.pair + ".txt")), "a", encoding="utf-8") as error_message:
                error_message.write("[!] " + config.pair + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n")
                error_message.write(str(e) + "\n\n")

except KeyboardInterrupt: print("\n\nAborted.\n")
