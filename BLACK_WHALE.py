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
    leverage    = int(config.leverage / 2.5)
    profit      = 1
    secure_profit = False

# ==========================================================================================================================================================================
#                                              BLACK_WHALE - GO BIG, WIN BIG, LOSE BIGGER
# ==========================================================================================================================================================================
#                                                                           
# - DESCRIPTION     :   1. Focus on 6HOUR direction
#                       2. Loop less, to minimize stressing the server
#
# - ENTRY CONDITION :   1. 6HOUR - VOLUME is Small > Medium > Large (VOLUME_FORMATION)
#                       2. 6HOUR - Current Volume is DOUBLE than the Previous Volume
#                       3. 6HOUR - CANDLE SIZE is Small > Medium > Large (WAR_FORMATION)
#                       4. 1HOUR - matches with 6HOUR
#
# - EXIT CONDITION  :   1. When the 1HOUR direction change against the position
#                       2. There is no Profit Secure for this strategy
#
# ==========================================================================================================================================================================

    def lets_make_some_money():
        position_info = get_position.get_position_info()
        klines_6HOUR  = binance_futures.KLINE_INTERVAL_6HOUR()
        klines_1HOUR  = binance_futures.KLINE_INTERVAL_1HOUR()

        print("Firstrun Volume  :   " + str(binance_futures.firstrun_volume(klines_6HOUR)))
        print("Previous Volume  :   " + str(binance_futures.previous_volume(klines_6HOUR)))
        print("Current Volume   :   " + str(binance_futures.current_volume(klines_6HOUR)))

        heikin_ashi.output_firstrun(klines_6HOUR)
        heikin_ashi.output_previous(klines_6HOUR)

        direction = heikin_ashi.output_current(klines_6HOUR)
        heikin_ashi.output_current(klines_1HOUR)

        if position_info == "LONGING":
            if EXIT_LONG(klines_1HOUR, klines_6HOUR):
                if live_trade: binance_futures.close_position("LONG")
                print("ACTION           :   💰 CLOSE_LONG 💰")
            else: print(colored("ACTION           :   HOLDING_LONG", "green"))

        elif position_info == "SHORTING":
            if EXIT_SHORT(klines_1HOUR, klines_6HOUR):
                if live_trade: binance_futures.close_position("SHORT")
                print("ACTION           :   💰 CLOSE_SHORT 💰")
            else: print(colored("ACTION           :   HOLDING_SHORT", "red"))

        else:
            if (direction == "GREEN" or direction == "GREEN_INDECISIVE") and GO_LONG(klines_1HOUR, klines_6HOUR):
                if live_trade: binance_futures.open_position("LONG", config.quantity)
                print(colored("ACTION           :   🚀 GO_LONG 🚀", "green"))

            elif (direction == "RED" or direction == "RED_INDECISIVE") and GO_SHORT(klines_1HOUR, klines_6HOUR):
                if live_trade: binance_futures.open_position("SHORT", config.quantity)
                print(colored("ACTION           :   💥 GO_SHORT 💥", "red"))

            else: print("ACTION           :   🐺 WAIT 🐺")

        print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

# ==========================================================================================================================================================================
#                                                    ENTRY_EXIT CONDITIONS
# ==========================================================================================================================================================================

    from heikin_ashi import current_candle
    from heikin_ashi import previous_Close
    from heikin_ashi import current_High
    from heikin_ashi import current_Low
    from heikin_ashi import strength_of_current

    def GO_LONG(klines_1HOUR, klines_6HOUR):
        if (heikin_ashi.volume_formation(klines_6HOUR) or heikin_ashi.volume_breakout(klines_6HOUR) or heikin_ashi.volume_sudden_breakout(klines_1HOUR)) and \
            current_candle(klines_1HOUR) == "GREEN" and \
            strength_of_current(klines_1HOUR) == "STRONG" and \
            strength_of_current(klines_6HOUR) == "STRONG": return True

    def GO_SHORT(klines_1HOUR, klines_6HOUR):
        if (heikin_ashi.volume_formation(klines_6HOUR) or heikin_ashi.volume_breakout(klines_6HOUR) or heikin_ashi.volume_sudden_breakout(klines_1HOUR)) and \
            current_candle(klines_1HOUR) == "RED" and \
            strength_of_current(klines_1HOUR) == "STRONG" and \
            strength_of_current(klines_6HOUR) == "STRONG": return True

    def EXIT_LONG(klines_1HOUR, klines_6HOUR):
        if secure_profit:
            if get_position.get_unRealizedProfit(profit) == "PROFIT":
                if ((current_candle(klines_1HOUR) == "RED" or current_candle(klines_1HOUR) == "RED_INDECISIVE") and strength_of_current(klines_1HOUR) == "STRONG") or \
                    (previous_Close(klines_1HOUR) > current_High(klines_1HOUR)): return True
            else:
                if ((current_candle(klines_6HOUR) == "RED" or current_candle(klines_6HOUR) == "RED_INDECISIVE") and strength_of_current(klines_6HOUR) == "STRONG") or \
                    (previous_Close(klines_6HOUR) > current_High(klines_6HOUR)): return True
        else:
            if ((current_candle(klines_1HOUR) == "RED" or current_candle(klines_1HOUR) == "RED_INDECISIVE") and strength_of_current(klines_1HOUR) == "STRONG") or \
               ((previous_Close(klines_1HOUR) > current_High(klines_1HOUR)) and volume_confirmation(klines_1HOUR)): return True

    def EXIT_SHORT(klines_1HOUR, klines_6HOUR):
        if secure_profit:
            if get_position.get_unRealizedProfit(profit) == "PROFIT":
                if ((current_candle(klines_1HOUR) == "GREEN" or current_candle(klines_1HOUR) == "GREEN_INDECISIVE") and strength_of_current(klines_1HOUR) == "STRONG") or \
                    (previous_Close(klines_1HOUR) < current_Low(klines_1HOUR)): return True
            else:
                if ((current_candle(klines_6HOUR) == "GREEN" or current_candle(klines_6HOUR) == "GREEN_INDECISIVE") and strength_of_current(klines_6HOUR) == "STRONG") or \
                    (previous_Close(klines_6HOUR) < current_Low(klines_6HOUR)): return True
        else:   
            if ((current_candle(klines_1HOUR) == "GREEN" or current_candle(klines_1HOUR) == "GREEN_INDECISIVE") and strength_of_current(klines_1HOUR) == "STRONG") or \
               ((previous_Close(klines_1HOUR) < current_Low(klines_1HOUR)) and volume_confirmation(klines_1HOUR)): return True

    def volume_confirmation(klines):
        return (binance_futures.current_volume(klines) > (binance_futures.previous_volume(klines) / 5))

# ==========================================================================================================================================================================
#                                                        DEPLOY THE BOT
# ==========================================================================================================================================================================

    if config.live_trade: print(colored("LIVE TRADE IS ENABLED\n", "green"))
    else: print(colored("LIVE TRADE IS NOT ENABLED\n", "red"))

    if binance_futures.position_information()[0].get('marginType') != "isolated": binance_futures.change_margin_to_ISOLATED()
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
