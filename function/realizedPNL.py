import config
from keys import client

i, overall_PNL = 0, 0
trades_list = client.futures_account_trades(symbol=config.pair, timestamp=int(time.time()*1000), limit=40)

for trade in trades_list:
    overall_PNL = overall_PNL + float(trade.get('realizedPnl'))
    if (float(trade.get('realizedPnl'))) > 0 :
        i = i + 1
        print(str(i) + ".  " + trade.get('realizedPnl'))
    elif (float(trade.get('realizedPnl'))) < 0 :
        i = i + 1
        print(str(i) + ". " + trade.get('realizedPnl') + " LOSER TRADE")
    else: continue
print("\n❗ Overall PNL over the last 20 trades: " + str(round(overall_PNL, 2)) + " USDT\n")