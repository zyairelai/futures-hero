import config
from termcolor import colored

def profit_threshold():
    return config.profit_margin

def get_entryPrice(response):
    return abs(float(response.get('entryPrice')))

def get_positionSize(response):
    return abs(float(response.get('positionAmt')))

def unrealizedPnL_Percentage(i, response, mark_price):
    price_diff = mark_price - get_entryPrice(response)
    increased_diff = price_diff / get_entryPrice(response) * 100
    pnl_percentage = increased_diff * config.leverage[i]
    return round(pnl_percentage, 2)

def get_position_info(i, response): # >>> "LONGING" // "SHORTING" // "NO_POSITION"
    title = config.pair[i] + " POSITION :   "
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

def profit_or_loss(response, taker_maker_fees):
    # One transaction is 0.04 %, buy and sell means 0.04 * 2 = 0.08 %
    # taker_maker_fees = 0.15 # // Always 15% to get a happy ending!
    markPrice        = float(response.get('markPrice'))
    positionAmt      = abs(float(response.get('positionAmt')))
    unRealizedProfit = round(float(response.get('unRealizedProfit')), 2)
    breakeven_USDT   = (markPrice * positionAmt * taker_maker_fees) / 100

    if unRealizedProfit > breakeven_USDT: return "PROFIT"
    else: return "LOSS"

def profit_margin_threshold(i):
    profit_margin = config.take_profit_percentage / config.leverage[i]
    return profit_margin