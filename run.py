try:
    import os, time, requests, socket, urllib3
    import config, binance_futures, strategy
    from datetime import datetime
    from termcolor import colored
    from binance.exceptions import BinanceAPIException

    if config.live_trade: print(colored("LIVE TRADE IS ENABLED\n", "green"))
    else: print(colored("LIVE TRADE IS NOT ENABLED\n", "red"))

    print("Futures-OMAX provides 2 modes:")
    print("1. SAFE_MODE - Lower win rate. However, you will not get wiped out. PROMISED.")
    print("2. DEAD_MODE - 90-95% win rate. However, one loss might cause you get WIPED OUT.")
    print("\nWhich mode do you want to enable?")
    user_input = input("Enter a number   :   ")

    if user_input == '2':
        mode = "DEAD_MODE"
        print(colored(mode + " ENABLED\n", "red"))
        leverage = config.leverage
        if binance_futures.position_information()[0].get('marginType') != "cross": binance_futures.change_margin_to_CROSSED()
    else:
        mode = "SAFE_MODE"
        print(colored(mode + " ENABLED\n", "green"))
        leverage = int(config.leverage / 5)
        if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()
    
    if int(binance_futures.position_information()[0].get("leverage")) != leverage:
        binance_futures.change_leverage(leverage)
        print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))

    def added_to_job():
        if mode == "DEAD_MODE": strategy.DEAD_OR_ALIVE()
        elif mode == "SAFE_MODE": strategy.JACK_RABBIT()

    while True:
        try:
            added_to_job()
            time.sleep(5)

        except (socket.timeout,
                BinanceAPIException,
                urllib3.exceptions.ProtocolError,
                urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                ConnectionResetError, KeyError, OSError) as e:

            if not os.path.exists("Error_Message"): os.makedirs("Error_Message")
            with open((os.path.join("Error_Message", config.pair + ".txt")), "a", encoding="utf-8") as error_message:
                error_message.write("[!] " + config.pair + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n")
                error_message.write(str(e) + "\n\n")

except KeyboardInterrupt: print("\n\nAborted.\n")
