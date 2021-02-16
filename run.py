try:
    import os, time, requests, socket, urllib3
    import config, binance_futures, strategy
    from datetime import datetime
    from termcolor import colored
    from binance.exceptions import BinanceAPIException
    from apscheduler.schedulers.blocking import BlockingScheduler

    if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()
    if int(binance_futures.position_information()[0].get("leverage")) != config.leverage:
        binance_futures.change_leverage(config.leverage)
        print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))

    print("Which mode do you want to use?")
    print("1. Safe Mode - Only trade one direction to MINIMIZE LOSS")
    print("2. Risk Mode - Might trade against direction to MAXIMIZE PROFITS")
    user_mode = input("Enter a number   :   ") or '1'

    if user_mode == '2': print(colored("RISK MODE ENABLED\n", "red"))
    else: print(colored("SAFE MODE ENABLED\n", "green"))

    def added_to_job():
        if user_mode == '2': strategy.fomo()
        else: strategy.dead_or_alive()

    while True:
        try:
            added_to_job()
            time.sleep(5)

            # scheduler = BlockingScheduler()
            # scheduler.add_job(added_to_job, 'cron', second='0,10,20,30,40,50')
            # scheduler.start()

        except (KeyError,
                socket.timeout,
                BinanceAPIException,
                ConnectionResetError,
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
