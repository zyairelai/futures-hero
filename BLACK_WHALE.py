try:
    import os, time, requests, socket, urllib3
    import config, binance_futures, strategy
    import heikin_ashi, get_position
    from datetime import datetime
    from termcolor import colored
    from heikin_ashi import war_formation
    from heikin_ashi import current_candle, previous_candle
    from heikin_ashi import strength_of_current, strength_of_previous
    from binance.exceptions import BinanceAPIException
    from apscheduler.schedulers.blocking import BlockingScheduler

    live_trade = config.live_trade

    def profit_threshold(response):
        if get_position.get_positionSize(response) > (config.quantity * 5):
            return 0.2
        else: return 0.5    
    # ==========================================================================================================================================================================
    #                    JACK_RABBIT - IN AND OUT QUICK, SOMETIMES MIGHT GET YOU STUCK IN A TRADE AND LIQUIDATED WHEN DIRECTION CHANGE
    # ==========================================================================================================================================================================
    def lets_make_some_money():
        # RETRIEVE KLINES and INFORMATION
        response = binance_futures.position_information()[0]
        klines_1min  = binance_futures.KLINE_INTERVAL_1MINUTE()
        klines_30MIN = binance_futures.KLINE_INTERVAL_30MINUTE()
        klines_1HOUR = binance_futures.KLINE_INTERVAL_1HOUR()
        klines_2HOUR = binance_futures.KLINE_INTERVAL_2HOUR()
        klines_6HOUR = binance_futures.KLINE_INTERVAL_6HOUR()
        
        heikin_ashi.output_previous(klines_6HOUR)
        heikin_ashi.output_current(klines_6HOUR)
        heikin_ashi.output_current(klines_1HOUR)
        heikin_ashi.output_current(klines_1min)

        position_info = get_position.get_position_info(response)
        profit = profit_threshold(response)

        if position_info == "LONGING":
            if EXIT_LONG(profit, klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
                if live_trade:
                    binance_futures.close_position("LONG")
                print("ACTION           :   💰 CLOSE_LONG 💰")
            elif THROTTLE_LONG(profit, klines_1HOUR, klines_2HOUR, klines_6HOUR):
                if live_trade:
                    binance_futures.throttle("LONG")
                    record_timestamp(klines_2HOUR)
                print("ACTION           :   🔥 THROTTLE_LONG 🔥")
            else: print(colored("ACTION           :   HOLDING_LONG", "green"))

        elif position_info == "SHORTING":
            if EXIT_SHORT(profit, klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
                if live_trade:
                    binance_futures.close_position("SHORT")
                print("ACTION           :   💰 CLOSE_SHORT 💰")
            elif THROTTLE_SHORT(profit, klines_1HOUR, klines_2HOUR, klines_6HOUR):
                if live_trade:
                    binance_futures.throttle("SHORT")
                    record_timestamp(klines_2HOUR)
                print("ACTION           :   🔥 THROTTLE_SHORT 🔥")
            else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

        else:
            if check_direction(klines_6HOUR) == "GREEN" and GO_LONG(klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR): # and (retrieve_timestamp() != current_kline_timestamp(klines_1HOUR)):
                if live_trade:
                    binance_futures.open_position("LONG", config.quantity)
                    record_timestamp(klines_2HOUR)
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

            elif check_direction(klines_6HOUR) == "RED" and GO_SHORT(klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR): # and (retrieve_timestamp() != current_kline_timestamp(klines_1HOUR)):
                if live_trade:
                    binance_futures.open_position("SHORT", config.quantity)
                    record_timestamp(klines_2HOUR)
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

            else: print("ACTION           :   🐺 WAIT 🐺")

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

    # ==========================================================================================================================================================================
    #                                                        ENTRY_EXIT CONDITIONS
    # ==========================================================================================================================================================================
    def check_direction(klines):
        if strength_of_previous(klines) == "STRONG":
            if previous_candle(klines) == "GREEN" or previous_candle(klines) == "GREEN_INDECISIVE" : previous = "GREEN"
            elif previous_candle(klines) == "RED" or previous_candle(klines) == "RED_INDECISIVE" : previous = "RED"
            else: previous = "INDECISIVE"
        else: previous = "INDECISIVE"

        if strength_of_current(klines) == "STRONG":
            if current_candle(klines) == "GREEN" or current_candle(klines) == "GREEN_INDECISIVE" : current = "GREEN"
            elif current_candle(klines) == "RED" or current_candle(klines) == "RED_INDECISIVE" : current = "RED"
            else: current = "INDECISIVE"
        else: current = "INDECISIVE"

        # Volume breakout

        if previous == "GREEN" and current == "GREEN": direction = "GREEN"
        elif previous == "RED" and current == "RED": direction = "RED"
        else: direction = "INDECISIVE"
        return direction
        
    def GO_LONG(klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
        if not hot_zone(klines_30MIN, klines_6HOUR) and check_direction(klines_1HOUR) == "GREEN" and \
        not heikin_ashi.volume_declining(klines_1HOUR) and not heikin_ashi.volume_declining(klines_6HOUR):
            if current_candle(klines_1min) == "GREEN" and strength_of_current(klines_1min) == "STRONG" and war_formation(klines_1min): return True

    def GO_SHORT(klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
        if not hot_zone(klines_30MIN, klines_6HOUR) and check_direction(klines_1HOUR) == "RED" and \
        not heikin_ashi.volume_declining(klines_1HOUR) and not heikin_ashi.volume_declining(klines_6HOUR):
            if current_candle(klines_1min) == "RED" and strength_of_current(klines_1min) == "STRONG" and war_formation(klines_1min): return True

    def EXIT_LONG(profit, klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
        if get_position.get_unRealizedProfit(profit) == "PROFIT":
            if heikin_ashi.previous_Close(klines_1min) > heikin_ashi.current_Close(klines_1min) or current_candle(klines_1min) != "GREEN": return True
        else: # Cut loss when both the 1HOUR and 6HOUR is going against you
            if not hot_zone(klines_30MIN, klines_6HOUR) and check_direction(klines_1HOUR) == "RED" and check_direction(klines_6HOUR) == "RED": return True

    def EXIT_SHORT(profit, klines_1min, klines_30MIN, klines_1HOUR, klines_6HOUR):
        if get_position.get_unRealizedProfit(profit) == "PROFIT":
            if heikin_ashi.previous_Close(klines_1min) < heikin_ashi.current_Close(klines_1min) or current_candle(klines_1min) != "RED": return True
        else: # Cut loss when both the 1HOUR and 6HOUR is going against you
            if not hot_zone(klines_30MIN, klines_6HOUR) and check_direction(klines_1HOUR) == "GREEN" and check_direction(klines_6HOUR) == "GREEN": return True

    def THROTTLE_LONG(profit, klines_1HOUR, klines_2HOUR, klines_6HOUR):
        if get_position.get_unRealizedProfit(profit) == "LOSS":
            if binance_futures.mark_price() < heikin_ashi.previous_Low(klines_1HOUR) and binance_futures.mark_price() < heikin_ashi.firstrun_Low(klines_1HOUR) and \
                retrieve_timestamp() != current_kline_timestamp(klines_2HOUR): return True

    def THROTTLE_SHORT(profit, klines_1HOUR, klines_2HOUR, klines_6HOUR):
        if get_position.get_unRealizedProfit(profit) == "LOSS":
            if binance_futures.mark_price() > heikin_ashi.previous_High(klines_1HOUR) and binance_futures.mark_price() < heikin_ashi.firstrun_High(klines_1HOUR) and \
                retrieve_timestamp() != current_kline_timestamp(klines_2HOUR): return True

    def hot_zone(klines_30MIN, klines_6HOUR):
        if klines_6HOUR[-1][0] == klines_30MIN[-1][0]: return True

    # ==========================================================================================================================================================================
    #                                                  EXTRA ADD-ON WORK IN PROGRESS
    # ==========================================================================================================================================================================

    def slipping_back():
        return "WORK IN PROGRESS"

    def DO_NOT_FUCKING_TRADE():
        return True

    # ==========================================================================================================================================================================
    #                                              SYSTEM TIME RECORD TO AVOID OVER-TRADE
    # ==========================================================================================================================================================================

    def record_timestamp(kline):
        with open((os.path.join(config.pair, "TIMESTAMP.txt")), "w", encoding="utf-8") as timestamp_record:
            timestamp_record.write(str(current_kline_timestamp(kline)))

    def retrieve_timestamp():
        with open((os.path.join(config.pair, "TIMESTAMP.txt")), "r", encoding="utf-8") as timestamp_record:
            return int(timestamp_record.read())

    def current_kline_timestamp(kline):
        return kline[-1][0] # This will return <int> type of timestamp
# ==========================================================================================================================================================================
#                                                        DEPLOY THE BOT
# ==========================================================================================================================================================================

    if config.live_trade: print(colored("LIVE TRADE IS ENABLED\n", "green"))
    else: print(colored("LIVE TRADE IS NOT ENABLED\n", "red"))

    if config.position_mode == "ISOLATED":
        leverage = int(config.leverage / 5) # AUTO ADJUST LEVERAGE
        if binance_futures.position_information()[0].get('marginType') != "isolated":
            binance_futures.change_margin_to_ISOLATED()
            print("Changed to ISOLATED mode")

    else: # if config.position_mode == "CROSSED":
        leverage = int(config.leverage) # AUTO ADJUST LEVERAGE
        if binance_futures.position_information()[0].get('marginType') != "cross":
            binance_futures.change_margin_to_CROSSED()
            print("Changed to CROSSED mode")

    if int(binance_futures.position_information()[0].get("leverage")) != leverage:
        binance_futures.change_leverage(leverage)
        print(colored("CHANGED LEVERAGE :   " + binance_futures.position_information()[0].get("leverage") + "x\n", "red"))

    while True:
        try:
            scheduler = BlockingScheduler()
            scheduler.add_job(lets_make_some_money, 'cron', second='0,10,20,30,40,50')
            scheduler.start()

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
