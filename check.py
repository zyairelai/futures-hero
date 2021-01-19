import time
import keys
from keys import client

while True:
    print("What do you want to check? ")
    print("1. keys")
    print("2. trend")
    print("3. minute")
    print("4. position")
    print("5. realizedPNL")
    input_num = input("\nEnter a number   :   ") or '1'

    if (input_num == '1'):
        print("API OWNER        :   " + keys.api_owner)
        print("API Key          :   " + keys.api_key)
        print("API Secret Key   :   " + keys.api_secret)
        print()
        break

    elif (input_num == '2'):
        start = time.time()
        import trend
        print("Main direction   :   " + trend.main_direction)
        print("Recent Minute    :   " + trend.recent_minute)
        print("\nThe <trend.py> return value is : " + trend.get_current_trend())
        print(f"Time Taken: {time.time() - start} seconds\n")
        break

    elif (input_num == '3'):
        from minute import get_current_minute
        loop = input("Do you want to loop? [Y/n]") or 'n'
        if loop == 'Y':
            while True:
                get_current_minute()
                print()
                time.sleep(5)
        else:
            start = time.time()
            print("\nThe <minute.py> return value is : " + get_current_minute())
            print(f"Time Taken: {time.time() - start} seconds\n")
        break

    elif (input_num == '4'):
        start = time.time()
        from position import get_position_info
        print("\nThe <position.py> return value is : " + get_position_info())
        print(f"Time Taken: {time.time() - start} seconds\n")
        break

    elif (input_num == '5'):
        import config
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
        break

    else: print("❗Invalid Number❗Try again❗\n")
