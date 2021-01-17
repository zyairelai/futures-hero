loop = False

import os
import time
from binance.client import Client

def get_current_minute(): # >>> RED_CANDLE // GREEN_CANDLE // WEAK_RED // WEAK_GREEN // RED_INDECISIVE // GREEN_INDECISIVE // SOMETHING_IS_WRONG
    klines = client.futures_klines(symbol=pair, interval=Client.KLINE_INTERVAL_1MINUTE, limit=3)

    first_run_Open  = round(((float(klines[0][1]) + float(klines[0][4])) / 2), 2)
    first_run_Close = round(((float(klines[0][1]) + float(klines[0][2]) + float(klines[0][3]) + float(klines[0][4])) / 4), 2)
    previous_Open   = round(((first_run_Open + first_run_Close) / 2), 2)
    previous_Close  = round(((float(klines[1][1]) + float(klines[1][2]) + float(klines[1][3]) + float(klines[1][4])) / 4), 2)

    current_Time    = int(klines[2][0])
    current_Open    = round(((previous_Open + previous_Close) / 2), 2)
    current_Close   = round(((float(klines[2][1]) + float(klines[2][2]) + float(klines[2][3]) + float(klines[2][4])) / 4), 2)
    current_High    = max(float(klines[2][2]), current_Open, current_Close)
    current_Low     = min(float(klines[2][3]), current_Open, current_Close)

    price_movement = (current_High - current_Low) / current_Open * 100

    print("The current_Time is  :   " + str(current_Time))
    print("The current_Open is  :   " + str(current_Open))
    print("The current_Close is :   " + str(current_Close))
    print("The current_High is  :   " + str(current_High))
    print("The current_Low is   :   " + str(current_Low))
    print("The price_movement is:   " + str(price_movement))

    if (current_Open == current_High):          
        if (price_movement >= threshold):
            minute_candle = "RED_CANDLE"
            print("Current MINUTE   :   🩸🩸🩸 RED 🩸🩸🩸")
        else:
            minute_candle = "WEAK_RED"
            print("Current MINUTE   :   🩸 WEAK_RED 🩸")
    elif (current_Open == current_Low):         
        if (price_movement >= threshold):
            minute_candle = "GREEN_CANDLE"
            print("Current MINUTE   :   🥦🥦🥦 GREEN 🥦🥦🥦")
        else:
            minute_candle = "WEAK_GREEN"
            print("Current MINUTE   :   🥦 WEAK_GREEN 🥦")
    else:
        if (current_Open > current_Close):
            print("Current MINUTE   :   🩸 RED_INDECISIVE 🩸")
            minute_candle = "RED_INDECISIVE"
        elif (current_Close > current_Open):
            print("Current MINUTE   :   🥦 GREEN_INDECISIVE 🥦")
            minute_candle = "GREEN_INDECISIVE"
        else:
            minute_candle = "SOMETHING_IS_WRONG"
            print("❗SOMETHING_IS_WRONG in get_minute_candle()❗")
    return minute_candle

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

while loop:
    get_current_minute()
    print()
    time.sleep(5)

start = time.time()
print("\nThe <minute.py> return value is : " + get_current_minute())
print(f"Time Taken: {time.time() - start} seconds\n")