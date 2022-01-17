import api_binance
import time
import config
import random
import strategies.combined
import strategies.ichimoku
import strategies.volume
import strategies.william_fractal
import os, requests, socket, urllib3
from webhook_launcher import telegram_bot_sendtext
from datetime import datetime
from termcolor import colored
from binance.exceptions import BinanceAPIException
print(colored("------ LIVE TRADE IS ENABLED ------\n", "green")) if config.live_trade else print(colored("THIS IS BACKTESTING\n", "red")) 

choose_your_fighter = strategies.combined
#fees 
taker_fees    = 0.2

def lets_make_some_money(pair, leverage, quantity): 
    print("--------------")
    print(pair)

    # Retrieve Infomation for Initial Trade Setup
    response = api_binance.position_information(pair)
    if response[0].get('marginType') != "isolated": api_binance.change_margin_to_ISOLATED(pair)
    if int(response[0].get("leverage")) != leverage: api_binance.change_leverage(pair, leverage)

    hero = choose_your_fighter.futures_hero(pair)
    # print(hero)

    if api_binance.LONG_SIDE(response) == "NO_POSITION":
        if hero["GO_LONG"].iloc[-1]:
            api_binance.market_open_long(pair, quantity)
        else: print("_LONG_SIDE : 🐺 WAIT 🐺")

    if api_binance.LONG_SIDE(response) == "LONGING":
        if hero["EXIT_LONG"].iloc[-1] and in_Profit(response[1]):
            api_binance.market_close_long(pair, response)
            print("EXIT "+str(float(response[1].get('entryPrice')))+" | Actual: "+str(float(response[1].get('markPrice')))+" | positionAmt: "+str(float(response[1].get('positionAmt')))+" | unRealizedProfit "+str(float(response[1].get('unRealizedProfit')))+"| InProfit "+str(in_Profit_show(response[1])))
        else: 
            print(colored("_LONG_SIDE : HOLDING_LONG", "green"))
            print("Entry Price "+str(float(response[1].get('entryPrice')))+" | Actual: "+str(float(response[1].get('markPrice')))+" | positionAmt: "+str(float(response[1].get('positionAmt')))+" | unRealizedProfit "+str(float(response[1].get('unRealizedProfit')))+"| InProfit "+str(in_Profit_show(response[1])))

    if api_binance.SHORT_SIDE(response) == "NO_POSITION":
        if hero["GO_SHORT"].iloc[-1]:
            api_binance.market_open_short(pair, quantity)
        else: print("SHORT_SIDE : 🐺 WAIT 🐺")

    if api_binance.SHORT_SIDE(response) == "SHORTING":
        if hero["EXIT_SHORT"].iloc[-1] and in_Profit(response[2]):
            api_binance.market_close_short(pair, response)
            print("EXIT "+str(float(response[2].get('entryPrice')))+" | Actual: "+str(float(response[2].get('markPrice')))+" | positionAmt: "+str(float(response[2].get('positionAmt')))+" | unRealizedProfit "+str(float(response[2].get('unRealizedProfit')))+"| InProfit "+str(in_Profit_show(response[2])))
        else: 
            print(colored("SHORT_SIDE : HOLDING_SHORT", "red"))
            print("Entry Price "+str(float(response[2].get('entryPrice')))+" | Actual: "+str(float(response[2].get('markPrice')))+" | positionAmt: "+str(float(response[2].get('positionAmt')))+" | unRealizedProfit "+str(float(response[2].get('unRealizedProfit')))+"| InProfit "+str(in_Profit_show(response[2])))

    print("Last action executed @ " + datetime.now().strftime("%H:%M:%S") + "\n")

def in_Profit(response):
    # taker_fees    = 0.2 changed to 0.3 to tried
    global taker_fees
    markPrice     = float(response.get('markPrice'))
    positionAmt   = abs(float(response.get('positionAmt')))
    unRealizedPNL = round(float(response.get('unRealizedProfit')), 2)
    breakeven_PNL = (markPrice * positionAmt * taker_fees) / 100
    return True if unRealizedPNL > breakeven_PNL else False

def in_Profit_show(response):
    # taker_fees    = 0.2 changed to 0.3 to tried
    #taker_fees    = 0.2
    global taker_fees
    markPrice     = float(response.get('markPrice'))
    positionAmt   = abs(float(response.get('positionAmt')))
    unRealizedPNL = round(float(response.get('unRealizedProfit')), 2)
    breakeven_PNL = (markPrice * positionAmt * taker_fees) / 100
    return round(breakeven_PNL,4)

try:
    while True:
        try:
            for i in range(len(config.pair)):
                pair     = config.pair[i]
                leverage = config.leverage[i]
                quantity = config.quantity[i]
                lets_make_some_money(pair, leverage, quantity)
                time.sleep(random.randint(1, 3)) #sleep to avoid penality

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
                telegram_bot_sendtext(" ERROR RESPONSE API BINANCE: "+ str(e)+"")

except KeyboardInterrupt: print("\n\nAborted.\n")
