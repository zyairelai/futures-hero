import os
import time
from binance.client import Client
def get_timestamp(): return int(time.time() * 1000)

def get_position_info(): # >>> LONGING // SHORTING // NO_POSITION
    position_response = client.futures_position_information(symbol=pair, timestamp=get_timestamp())[0]
    positionAmt = float(position_response.get('positionAmt'))
    print(position_response)

    if (positionAmt > 0):
        position = "LONGING"
    elif (positionAmt < 0):
        position = "SHORTING"
    else:
        position = "NO_POSITION"
    print("Current Position :   " + position)
    return position

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
print("\nThe <position.py> return value is : " + get_position_info())
print(f"Time Taken: {time.time() - start} seconds\n")
