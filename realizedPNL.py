import time
import config
import binance_futures
from termcolor import colored

i, overall_PNL = 0, 0
check_how_many_trades = 30
trades_list = binance_futures.account_trades(check_how_many_trades)

for trade in trades_list:
    overall_PNL = overall_PNL + float(trade.get('realizedPnl'))
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
