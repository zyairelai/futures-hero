import time
import config
import binance_futures
from termcolor import colored

def get_position_info(): # >>> "LONGING" // "SHORTING" // "NO_POSITION"
    title = "CURRENT POSITION :   "

    response = binance_futures.position_information()[0]
    positionAmt = float(response.get('positionAmt'))
    unRealizedProfit = round(float(binance_futures.position_information()[0].get('unRealizedProfit')), config.round_decimal)
    # print(binance_futures.position_information()[0])

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

def get_pending_PNL():
    unRealizedProfit = round(float(binance_futures.position_information()[0].get('unRealizedProfit')), config.round_decimal)

    if unRealizedProfit > 0: return "PROFIT"
    else: return "LOSS"
