try:
    import os, time, requests, socket, urllib3
    import config, binance_futures, strategy
    from datetime import datetime
    from termcolor import colored
    from binance.exceptions import BinanceAPIException

    if not os.path.exists(config.pair): os.makedirs(config.pair)

    if config.live_trade: print(colored("LIVE TRADE IS ENABLED\n", "green"))
    else: print(colored("LIVE TRADE IS NOT ENABLED\n", "red"))

    leverage = int(config.leverage / 2.5) # AUTO ADJUST LEVERAGE
    if int(binance_futures.position_information()[0].get("leverage")) != leverage:
        binance_futures.change_leverage(leverage)
        print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))

    def added_to_job(): strategy.lets_make_some_money()

    while True:
        try:
            added_to_job()
            time.sleep(3)

        except (socket.timeout,
                BinanceAPIException,
                urllib3.exceptions.ProtocolError,
                urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                ConnectionResetError, KeyError, OSError) as e:

            if not os.path.exists(config.pair): os.makedirs(config.pair)
            with open((os.path.join(config.pair, "ERROR.txt")), "a", encoding="utf-8") as error_message:
                error_message.write("[!] " + config.pair + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n")
                error_message.write(str(e) + "\n\n")

except KeyboardInterrupt: print("\n\nAborted.\n")
