check_how_many_trades = 20

import time, os, config
from termcolor import colored
from binance.client import Client

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def get_timestamp():
    return int(time.time() * 1000)

def position_information():
    return client.futures_position_information(symbol=config.pair, timestamp=get_timestamp())

def account_trades(trades):
    return client.futures_account_trades(symbol=config.pair, timestamp=get_timestamp(), limit=(trades*2))

i, overall_PNL = 0, 0
trades_list    = account_trades(check_how_many_trades)
position_info  = position_information()[0]
markPrice      = float(position_info.get('markPrice'))
positionAmt    = abs(float(position_info.get('positionAmt')))
fees_in_USDT   = round(((markPrice * positionAmt * 0.08) / 100), 2)

for trade in trades_list:
    overall_PNL = overall_PNL + float(trade.get('realizedPnl')) - fees_in_USDT
    if (float(trade.get('realizedPnl'))) > 0 :
        i = i + 1
        print(str(i) + ".  " + trade.get('realizedPnl'))
    elif (float(trade.get('realizedPnl'))) < 0 :
        i = i + 1
        print(str(i) + ". " + trade.get('realizedPnl') + " LOSER TRADE")
    else: continue

if overall_PNL > 0 : print(colored("\nOverall PNL over the last " + str(check_how_many_trades) + " trades: " + str(round(overall_PNL, 2)) + " USDT\n", "green"))
elif overall_PNL < 0 : print(colored("\nOverall PNL over the last " + str(check_how_many_trades) + " trades: " + str(round(overall_PNL, 2)) + " USDT\n", "red"))
else: print("\nOverall PNL over the last " + str(check_how_many_trades) + " trades: " + str(round(overall_PNL, 2)) + " USDT\n")