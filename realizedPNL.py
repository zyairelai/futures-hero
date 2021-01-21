import config
import time
from keys import client
from termcolor import colored
def get_timestamp(): return int(time.time() * 1000)

i, overall_PNL = 0, 0
trades_list = client.futures_account_trades(symbol=config.pair, timestamp=get_timestamp(), limit=60)

for trade in trades_list:
    overall_PNL = overall_PNL + float(trade.get('realizedPnl'))
    if (float(trade.get('realizedPnl'))) > 0 :
        i = i + 1
        print(str(i) + ".  " + trade.get('realizedPnl'))
    elif (float(trade.get('realizedPnl'))) < 0 :
        i = i + 1
        print(str(i) + ". " + trade.get('realizedPnl') + " LOSER TRADE")
    else: continue

if overall_PNL > 0 : print(colored("\nOverall PNL over the last 30 trades: " + str(round(overall_PNL, 2)) + " USDT\n", "green"))
elif overall_PNL < 0 : print(colored("\nOverall PNL over the last 30 trades: " + str(round(overall_PNL, 2)) + " USDT\n", "red"))
else: print("\nOverall PNL over the last 30 trades: " + str(round(overall_PNL, 2)) + " USDT\n")
