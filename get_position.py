import time
import config
import binance_futures
from termcolor import colored

def get_position_info(): # >>> "LONGING" // "SHORTING" // "NO_POSITION"
    title = config.pair + " POSITION :   "

    response = binance_futures.position_information()[0]
    positionAmt = float(response.get('positionAmt'))
    unRealizedProfit = round(float(response.get('unRealizedProfit')), 2)

    if (positionAmt > 0):
        position = "LONGING"
        print(colored(title + position, "green"))
        if unRealizedProfit > 0: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "green"))
        else: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "red"))

    elif (positionAmt < 0):
        position = "SHORTING"
        print(colored(title + position, "red"))
        if unRealizedProfit > 0: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "green"))
        else: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "red"))

    else:
        position = "NO_POSITION"
        print(title + position)

    return position

def get_unRealizedProfit():
    response         = binance_futures.position_information()[0]
    markPrice        = float(response.get('markPrice'))
    positionAmt      = abs(float(response.get('positionAmt')))
    unRealizedProfit = round(float(response.get('unRealizedProfit')), 2)
    taker_maker_fees = 0.2 # One transaction is 0.04 %, buy and sell means 0.04 * 2 = 0.08 % // But always 20% to get a happy ending!
    breakeven_USDT   = (markPrice * positionAmt * taker_maker_fees) / 100

    if unRealizedProfit > breakeven_USDT: return "PROFIT"
    else: return "LOSS"
