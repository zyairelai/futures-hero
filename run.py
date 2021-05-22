try:
    import os, requests, socket, urllib3
    import config, risk_level_1, risk_level_2, risk_level_3
    from datetime import datetime
    from termcolor import colored
    from binance.exceptions import BinanceAPIException

    if config.live_trade: print(colored("LIVE TRADE IS ENABLED\n", "green"))
    else: print(colored("LIVE TRADE IS NOT ENABLED\n", "red"))

    while True:
        try:
            for i in range(len(config.pair)):
                if config.risk_level == 1: risk_level_1.lets_make_some_money(i)
                elif config.risk_level == 2: risk_level_2.lets_make_some_money(i)
                else: risk_level_3.lets_make_some_money(i)

        except (socket.timeout,
                BinanceAPIException,
                urllib3.exceptions.ProtocolError,
                urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                ConnectionResetError, KeyError, OSError) as e:

            if not os.path.exists(config.pair[i]): os.makedirs(config.pair[i])
            with open((os.path.join(config.pair[i], "ERROR.txt")), "a", encoding="utf-8") as error_message:
                error_message.write("[!] " + config.pair[i] + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n")
                error_message.write(str(e) + "\n\n")

except KeyboardInterrupt: print("\n\nAborted.\n")
