import config
from termcolor import colored

def get_position_info(i, response): # >>> "LONGING" // "SHORTING" // "NO_POSITION"
    title = config.pair[i] + " POSITION :   "
    positionAmt = float(response.get('positionAmt'))
    unRealizedProfit = round(float(response.get('unRealizedProfit')), 2)

    if (positionAmt > 0):
        position = "LONGING"
        print(colored(title + position, "green"))
        if unRealizedProfit > 0: print(colored("unRealizedProfit :   " + str(unRealizedProfit) + " USDT", "green"))
        else: print(colored("unRealizedProfit :   " + str(unRealizedProfit) + " USDT", "red"))

    elif (positionAmt < 0):
        position = "SHORTING"
        print(colored(title + position, "red"))
        if unRealizedProfit > 0: print(colored("unRealizedProfit :   " + str(unRealizedProfit) + " USDT", "green"))
        else: print(colored("unRealizedProfit :   " + str(unRealizedProfit) + " USDT", "red"))

    else:
        position = "NO_POSITION"
        print(title + position)

    return position

def profit_or_loss(response, taker_maker_fees):
    # One transaction is 0.04 %, buy and sell means 0.04 * 2 = 0.08 %
    # taker_maker_fees = 0.10 # // Always more than 10% to get a happy ending!
    markPrice        = float(response.get('markPrice'))
    positionAmt      = abs(float(response.get('positionAmt')))
    unRealizedProfit = round(float(response.get('unRealizedProfit')), 2)
    breakeven_USDT   = (markPrice * positionAmt * taker_maker_fees) / 100

    if unRealizedProfit > breakeven_USDT: return "PROFIT"
    else: return "LOSS"
