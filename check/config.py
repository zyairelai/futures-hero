while True:
    print("Here are the supported Coins: ")
    print("1. BTC")
    print("2. ETH")
    print("3. BNB")
    print("4. LINK")
    print("5. SUSHI")

    input_num = input("\nChoose your Coin :   ") or '1'

    if input_num == '1': 
        coin            = "BTC"
        quantity        = 0.001     # Minimum 0.001
        leverage        = 125       # 1 - 125
        threshold       = 0.15      # Optimal 0.15
        stoplimit       = 0.15      # shall be 70-100% of threshold
        callbackRate    = 0.3       # Still testing
        round_decimal   = 2
        break

    elif input_num == '2': 
        coin            = "ETH"
        quantity        = 0.02      # Minimum 0.05
        leverage        = 100       # 1 - 100
        threshold       = 0.15
        stoplimit       = 0.15
        callbackRate    = 0.3
        round_decimal   = 2
        break

    elif input_num == '3': 
        coin            = "BNB"
        quantity        = 0.5       # Minimum 0.5
        leverage        = 75        # 1 - 75
        threshold       = 0.15
        stoplimit       = 0.15
        callbackRate    = 0.3
        round_decimal   = 4
        break

    elif input_num == '4': 
        coin            = "LINK"
        quantity        = 1         # Minimum 1
        leverage        = 75        # 1 - 75
        threshold       = 0.15
        stoplimit       = 0.15
        callbackRate    = 0.3
        round_decimal   = 4
        break

    elif input_num == '5': 
        coin            = "SUSHI"
        quantity        = 1         # Minimum 1
        leverage        = 50        # 1 - 50
        threshold       = 0.15
        stoplimit       = 0.15
        callbackRate    = 0.3
        round_decimal   = 4
        break

    else: print("[!] Invalid Number. Try again.\n")

pair = coin + "USDT"

print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print("Leverage         :   " + str(leverage) + "x")
print("Price Movement   :   " + str(threshold) + " %")
print("Stop Limit       :   " + str(stoplimit) + " %")
print("Call Back Rate   :   " + str(callbackRate) + " %")
print("Round Decimal    :   " + str(round_decimal) + " decimal place")
print()
