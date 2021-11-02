import api_binance
import config
import strategy
import os, requests, socket, urllib3
from datetime import datetime
from termcolor import colored
from binance.exceptions import BinanceAPIException
print(colored("LIVE TRADE IS ENABLED\n", "green")) if config.live_trade else print(colored("THIS IS BACKTESTING\n", "red")) 

print_logs = True
cover_fees = config.cover_fees

def lets_make_some_money(pair, leverage, quantity): 
    print(pair)

    # Retrieve Infomation for Initial Trade Setup
    response = api_binance.position_information(pair)
    if response[0].get('marginType') != "isolated": api_binance.change_margin_to_ISOLATED(pair)
    if int(response[0].get("leverage")) != config.leverage[i]: api_binance.change_leverage(pair, leverage)
    
    hero = strategy.futures_hero(pair)
    if print_logs : print(hero)

    if api_binance.LONG_SIDE(response) == "NO_POSITION":
        if hero["GO_LONG"].iloc[-1]:
            api_binance.market_open_long(pair, quantity)
        else: print("_LONG_SIDE : 🐺 WAIT 🐺")

    if api_binance.LONG_SIDE(response) == "LONGING":
        if hero["EXIT_LONG"].iloc[-1] and cover_fees:
            api_binance.market_close_long(i, response)
        else: print(colored("_LONG_SIDE : HOLDING_LONG", "green"))

    if api_binance.SHORT_SIDE(response) == "NO_POSITION":
        if hero["GO_SHORT"].iloc[-1]:
            api_binance.market_open_short(pair, quantity)
        else: print("SHORT_SIDE : 🐺 WAIT 🐺")

    if api_binance.SHORT_SIDE(response) == "SHORTING":
        if hero["EXIT_SHORT"].iloc[-1] and cover_fees:
            api_binance.market_close_short(i, response)
        else: print(colored("SHORT_SIDE : HOLDING_SHORT", "red"))

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

try:
    while True:
        try:
            for i in range(len(config.pair)):
                pair     = config.pair[i]
                leverage = config.leverage[i]
                quantity = config.quantity[i]
                lets_make_some_money(pair, leverage, quantity)

        except (socket.timeout,
                BinanceAPIException,
                urllib3.exceptions.ProtocolError,
                urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ConnectTimeout,
                requests.exceptions.ReadTimeout,
                ConnectionResetError, KeyError, OSError) as e:

            if not os.path.exists("ERROR"): os.makedirs("ERROR")
            with open((os.path.join("ERROR", config.pair[i] + ".txt")), "a", encoding="utf-8") as error_message:
                error_message.write("[!] " + config.pair[i] + " - " + "Created at : " + datetime.today().strftime("%d-%m-%Y @ %H:%M:%S") + "\n" + str(e) + "\n\n")
                print(e)

except KeyboardInterrupt: print("\n\nAborted.\n")
