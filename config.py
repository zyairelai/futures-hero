while True:
    print("\nHere are the supported Pairs: ")
    print("1. BTC-USDT")
    print("2. ETH-USDT")

    input_num = input("\nChoose your Pair :   ")

    if (input_num == '1') or (input_num == 'btc') or (input_num == 'BTC'):
        coin            = "BTC"
        quantity        = 0.001     # 0.001 BTC == 0.30 USDT @36XXX with leverage 125x
        leverage        = 125       # Maximum 125
        threshold       = 0.15      # Optimal 0.15 for entry
        stoplimit       = 0.12      # shall be 70-100% of threshold
        callbackRate    = 0.2
        round_decimal   = 2
        break

    elif (input_num == '2') or (input_num == 'eth') or (input_num == 'ETH'):
        coin            = "ETH"
        quantity        = 0.02      # 0.02 ETH == 0.25 USDT @12XX with leverage 100x
        leverage        = 100       # Maximum 100
        threshold       = 0.15
        stoplimit       = 0.12
        callbackRate    = 0.2
        round_decimal   = 2
        break

    else: print("❗Invalid Number❗Try again❗\n")

pair = coin + "USDT"

print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print("Leverage         :   " + str(leverage) + "x")
print("Price Movement   :   " + str(threshold) + " %")
print("Stop Limit       :   " + str(stoplimit) + " %")
print("Round Decimal    :   " + str(round_decimal) + " decimal place")
print()
