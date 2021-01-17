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
