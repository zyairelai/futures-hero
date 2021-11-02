import config
import os, time
from datetime import datetime
from binance.client import Client
from termcolor import colored

# Get environment variables
api_key     = os.environ.get('BINANCE_KEY')
api_secret  = os.environ.get('BINANCE_SECRET')
client      = Client(api_key, api_secret)

def get_timestamp():
    return int(time.time() * 1000)

def midnight():
    midnight = datetime.utcnow().replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    return int(datetime.timestamp(midnight) * 1000)

for i in range(len(config.pair)):
    pair = config.pair[i]
    count, overall_PNL, win, lose = 0, 0, 0, 0
    trades_list    = client.futures_account_trades(symbol=pair, timestamp=get_timestamp(), startTime=midnight())
    position_info  = client.futures_position_information(symbol=pair, timestamp=get_timestamp())[0]
    markPrice      = float(position_info.get('markPrice'))
    positionAmt    = abs(float(position_info.get('positionAmt')))
    fees_in_USDT   = round(((markPrice * positionAmt * 0.1) / 100), 2)

    for trade in trades_list:
        overall_PNL = overall_PNL + (float(trade.get('realizedPnl')) - fees_in_USDT)
        if (float(trade.get('realizedPnl'))) > 0 :
            count = count + 1
            win = win + 1
            print(str(count) + ".  " + trade.get('realizedPnl'))
        elif (float(trade.get('realizedPnl'))) < 0 :
            count = count + 1
            lose = lose + 1
            print(str(count) + ". " + trade.get('realizedPnl') + " LOSER TRADE")
        else: continue

    print(pair)
    print("TOTAL TRADES     :   " + str(count) + " TRADES")
    print("WIN-LOSE RATIO   :   " + str(win) + "-" + str(lose))

    if overall_PNL > 0 : print(colored("Overall PNL for today : " + str(round(overall_PNL, 2)) + " USDT", "green"))
    elif overall_PNL < 0 : print(colored("Overall PNL for today : " + str(round(overall_PNL, 2)) + " USDT", "red"))
    else: print("Overall PNL for today : " + str(round(overall_PNL, 2)) + " USDT")
    print()
