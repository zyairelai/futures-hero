import os
import time
from binance.client import Client

def get_2hour(): # >>> UP_TREND // DOWN_TREND // NO_TRADE_ZONE
    klines = client.futures_klines(symbol=pair, interval=Client.KLINE_INTERVAL_2HOUR, limit=3)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), round_decimal)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), round_decimal)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), round_decimal)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), round_decimal)

    current_Open    = round(((previous_Open + previous_Close) / 2), round_decimal)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), round_decimal)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    if (current_Open == current_High):
        trend = "DOWN_TREND"
        # print("Current TREND    :   🩸 DOWN_TREND 🩸")
    elif (current_Open == current_Low):
        trend = "UP_TREND"
        # print("Current TREND    :   🥦 UP_TREND 🥦")
    else:
        trend = "NO_TRADE_ZONE"
        # print("Current TREND    :   😴 NO_TRADE_ZONE 😴")
    return trend

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

def asset_info():
    global pair
    global quantity
    global leverage
    global threshold
    global stoplimit
    global callbackRate
    global round_decimal
    
    while True:
        print("Here are the supported Coins: ")
        print("1. BTC\n" + "2. ETH\n" + "3. LINK\n" + "4. SUSHI\n")
        input_num = input("Choose your Coin :   ") or '1'

        if input_num == '1': 
            coin            = "BTC"
            quantity        = 0.001
            leverage        = 125
            threshold       = 0.15
            stoplimit       = 0.15
            callbackRate    = 0.3
            round_decimal   = 2
            break

        elif input_num == '2': 
            coin            = "ETH"
            quantity        = 0.01
            leverage        = 100
            threshold       = 0.15
            stoplimit       = 0.15
            callbackRate    = 0.3
            round_decimal   = 2
            break

        elif input_num == '3': 
            coin            = "LINK"
            quantity        = 1
            leverage        = 75
            threshold       = 0.15
            stoplimit       = 0.15
            callbackRate    = 0.3
            round_decimal   = 4
            break

        elif input_num == '4': 
            coin            = "SUSHI"
            quantity        = 1
            leverage        = 50
            threshold       = 0.15
            stoplimit       = 0.15
            callbackRate    = 0.3
            round_decimal   = 4
            break

        else:  print("Invalid Number. Try again.\n")

    pair = coin + "USDT"

    print("Pair Name        :   " + str(pair))
    print("Minimum Quantity :   " + str(quantity))
    print("Maximum Leverage :   " + str(leverage))
    print("Price Movement   :   " + str(threshold))
    print("Stop Limit       :   " + str(stoplimit))
    print("Call Back Rate   :   " + str(callbackRate))
    print("Round Decimal    :   " + str(round_decimal))
    print()

asset_info()

start = time.time()
print("\nThe <2_hour.py> return value is : " + get_2hour())
print(f"Time Taken: {time.time() - start} seconds\n")