import time
import config
import binance_futures
from termcolor import colored

def get_position_info(): # >>> "LONGING" // "SHORTING" // "NO_POSITION"
    title = "CURRENT POSITION :   "

    response = binance_futures.position_information()[0]
    positionAmt = float(response.get('positionAmt'))
    entryPrice  = float(response.get('entryPrice'))
    markPrice   = float(response.get('markPrice'))

    unRealizedProfit = round(float(binance_futures.position_information()[0].get('unRealizedProfit')), config.round_decimal)
    # print(binance_futures.position_information()[0])
    
    if (positionAmt > 0):
        position = "LONGING"
        print(colored(title + position, "green"))
        print("ENTRY PRICE      :   " + str(round(entryPrice, config.round_decimal)))
        print("MARK PRICE       :   " + str(round(markPrice, config.round_decimal)))
        if unRealizedProfit > 0: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "green"))
        else: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "red"))

    elif (positionAmt < 0):
        position = "SHORTING"
        print(colored(title + position, "red"))
        print("ENTRY PRICE      :   " + str(round(entryPrice, config.round_decimal)))
        print("MARK PRICE       :   " + str(round(markPrice, config.round_decimal)))
        if unRealizedProfit > 0: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "green"))
        else: print(colored("unRealizedProfit :   " + str(unRealizedProfit), "red"))

    else:
        position = "NO_POSITION"
        print(title + position)

    return position
