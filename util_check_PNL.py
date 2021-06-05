import config, binance_futures_api
from termcolor import colored
from datetime import datetime

now = datetime.utcnow()
midnight = now.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
midnight_timestamp = int(datetime.timestamp(midnight) * 1000)

for coinlist in range(len(config.pair)):
    i, overall_PNL, win, lose = 0, 0, 0, 0
    trades_list    = binance_futures_api.account_trades(coinlist, midnight_timestamp)
    position_info  = binance_futures_api.position_information(coinlist)
    markPrice      = float(position_info.get('markPrice'))
    positionAmt    = abs(float(position_info.get('positionAmt')))
    fees_in_USDT   = round(((markPrice * positionAmt * 0.1) / 100), 2)

    for trade in trades_list:
        overall_PNL = overall_PNL + (float(trade.get('realizedPnl')) - fees_in_USDT)
        if (float(trade.get('realizedPnl'))) > 0 :
            i = i + 1
            win = win + 1
            print(str(i) + ".  " + trade.get('realizedPnl'))
        elif (float(trade.get('realizedPnl'))) < 0 :
            i = i + 1
            lose = lose + 1
            print(str(i) + ". " + trade.get('realizedPnl') + " LOSER TRADE")
        else: continue

    print(config.pair[coinlist])
    print("TOTAL TRADES     :   " + str(i) + " TRADES")
    print("WIN-LOSE RATIO   :   " + str(win) + "-" + str(lose))

    if overall_PNL > 0 : print(colored("Overall PNL for today : " + str(round(overall_PNL, 2)) + " USDT", "green"))
    elif overall_PNL < 0 : print(colored("Overall PNL for today : " + str(round(overall_PNL, 2)) + " USDT", "red"))
    else: print("Overall PNL for today : " + str(round(overall_PNL, 2)) + " USDT")
    print()

    # print(colored(config.pair[coinlist], display))
    # print(colored("TOTAL TRADES          : " + str(i) + " TRADES", display))
    # print(colored("WIN-LOSE RATIO        : " + str(win) + "-" + str(lose), display))
    # print(colored("Overall PNL for today : " + str(round(overall_PNL, 2)) + " USDT", display))
    # print()
