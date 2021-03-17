try:
    import os, time, requests, socket, urllib3
    import config
    import heikin_ashi
    import get_position
    import binance_futures
    from datetime import datetime
    from termcolor import colored
    from binance.exceptions import BinanceAPIException
    from apscheduler.schedulers.blocking import BlockingScheduler

    live_trade  = config.live_trade
    leverage    = int((config.leverage / 5) * 2)
    profit      = 0.3

# ==========================================================================================================================================================================
#                    FOMO - Just a Fomo strategy for testing, if you want to lose money kindly run this
# ==========================================================================================================================================================================

    def lets_make_some_money():
        position_info = get_position.get_position_info()
        kline_15MIN   = binance_futures.KLINE_INTERVAL_15MINUTE()
        klines_1MIN   = binance_futures.KLINE_INTERVAL_1MINUTE()

        print("Firstrun Volume  :   " + str(binance_futures.firstrun_volume(kline_15MIN)))
        print("Previous Volume  :   " + str(binance_futures.previous_volume(kline_15MIN)))
        print("Current Volume   :   " + str(binance_futures.current_volume(kline_15MIN)))

        heikin_ashi.output_firstrun(kline_15MIN)
        heikin_ashi.output_previous(kline_15MIN)

        direction = heikin_ashi.output_current(kline_15MIN)
        heikin_ashi.output_current(klines_1MIN)

        if position_info == "LONGING":
            if EXIT_LONG(klines_1MIN) and get_position.get_unRealizedProfit(profit) == "PROFIT":
                if live_trade: binance_futures.close_position("LONG")
                record_timestamp(kline_15MIN, "FOMO")
                print("ACTION           :   💰 CLOSE_LONG 💰")
            else: print(colored("ACTION           :   HOLDING_LONG", "green"))

        elif position_info == "SHORTING":
            if EXIT_SHORT(klines_1MIN) and get_position.get_unRealizedProfit(profit) == "PROFIT":
                if live_trade: binance_futures.close_position("SHORT")
                record_timestamp(kline_15MIN, "FOMO")
                print("ACTION           :   💰 CLOSE_SHORT 💰")
            else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

        else:
            if (direction == "GREEN") and GO_LONG(klines_1MIN, kline_15MIN) and (retrieve_timestamp("FOMO") != current_kline_timestamp(kline_15MIN)):
                if live_trade: binance_futures.open_position("LONG", config.quantity)
                record_timestamp(kline_15MIN, "FOMO")
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

            elif (direction == "RED") and GO_SHORT(klines_1MIN, kline_15MIN) and (retrieve_timestamp("FOMO") != current_kline_timestamp(kline_15MIN)):
                if live_trade: binance_futures.open_position("SHORT", config.quantity)
                record_timestamp(kline_15MIN, "FOMO")
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

            else: print("ACTION           :   🐺 WAIT 🐺")

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                    ENTRY_EXIT CONDITIONS
# ==========================================================================================================================================================================

    def GO_LONG(klines_1MIN, kline_15MIN):
        if (heikin_ashi.volume_formation(kline_15MIN) or heikin_ashi.volume_breakout(kline_15MIN)) and \
            heikin_ashi.current_candle(klines_1MIN) == "GREEN" and \
            heikin_ashi.strength_of_current(klines_1MIN) == "STRONG" and \
            heikin_ashi.strength_of_current(kline_15MIN) == "STRONG": return True

    def GO_SHORT(klines_1MIN, kline_15MIN):
        if (heikin_ashi.volume_formation(kline_15MIN) or heikin_ashi.volume_breakout(kline_15MIN)) and \
            heikin_ashi.current_candle(klines_1MIN) == "RED" and \
            heikin_ashi.strength_of_current(klines_1MIN) == "STRONG" and \
            heikin_ashi.strength_of_current(kline_15MIN) == "STRONG": return True

    def EXIT_LONG(klines_1MIN):
        if ((heikin_ashi.current_candle(klines_1MIN) == "RED" or heikin_ashi.current_candle(klines_1MIN) == "RED_INDECISIVE") and heikin_ashi.strength_of_current(klines_1MIN) == "STRONG") or \
            (heikin_ashi.previous_Close(klines_1MIN) > heikin_ashi.current_High(klines_1MIN)): return True
            # Secure profit on 1 hour and cut loss when 6 hour change

    def EXIT_SHORT(klines_1MIN):
        if ((heikin_ashi.current_candle(klines_1MIN) == "GREEN" or heikin_ashi.current_candle(klines_1MIN) == "GREEN_INDECISIVE") and heikin_ashi.strength_of_current(klines_1MIN) == "STRONG") or \
            (heikin_ashi.previous_Close(klines_1MIN) < heikin_ashi.current_Low(klines_1MIN)): return True
            # Secure profit on 1 hour and cut loss when 6 hour change

# ==========================================================================================================================================================================
#                                                      RECORD TIMESTAMP
# ==========================================================================================================================================================================

    def record_timestamp(kline, filename):
        if not os.path.exists("TIMESTAMP"): os.makedirs("TIMESTAMP")
        if not os.path.exists(os.path.join("TIMESTAMP", config.pair)): os.makedirs(os.path.join("TIMESTAMP", config.pair))

        with open((os.path.join("TIMESTAMP", config.pair, filename + ".txt")), "w", encoding="utf-8") as timestamp_record:
            timestamp_record.write(str(current_kline_timestamp(kline)))

    def retrieve_timestamp(filename):
        with open((os.path.join("TIMESTAMP", config.pair, filename + ".txt")), "r", encoding="utf-8") as timestamp_record:
            return int(timestamp_record.read())

    def current_kline_timestamp(kline):
        return kline[-1][0] # This will return <int> type of timestamp

# ==========================================================================================================================================================================
#                                                        DEPLOY THE BOT
# ==========================================================================================================================================================================

    if config.live_trade: print(colored("LIVE TRADE IS ENABLED\n", "green"))
    else: print(colored("LIVE TRADE IS NOT ENABLED\n", "red"))

    if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()
    if int(binance_futures.position_information()[0].get("leverage")) != leverage:
        binance_futures.change_leverage(leverage)
        print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))

    record_timestamp(binance_futures.KLINE_INTERVAL_1HOUR(), "FOMO")

    while True:
        try:
            lets_make_some_money()
            time.sleep(5)

        except (socket.timeout,
                BinanceAPIException,
                urllib3.exceptions.ProtocolError,
                urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                ConnectionResetError, KeyError, OSError) as e:

            if not os.path.exists("ERROR"): os.makedirs("ERROR")
            with open((os.path.join("ERROR", config.pair + ".txt")), "a", encoding="utf-8") as error_message:
                error_message.write("[!] " + config.pair + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n")
                error_message.write(str(e) + "\n\n")

except KeyboardInterrupt: print("\n\nAborted.\n")
