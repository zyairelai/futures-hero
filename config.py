while True:
    print("\nHere are the supported Pairs: ")
    print("1. BTC-USDT")
    print("2. ETH-USDT")
    print("3. LTC-USDT")
    print("4. BCH-USDT")

    input_num = input("\nChoose your Pair :   ")

    if (input_num == '1') or (input_num == 'btc') or (input_num == 'BTC'):
        coin            = "BTC"
        quantity        = 0.003     # 1USDT == 0.003 BTC @ 37XXX
        leverage        = 125       # Maximum 125
        threshold       = 0.15      # Optimal 0.15 for entry
        stoplimit       = 0.12      # shall be 70-100% of threshold
        callbackRate    = 0.2
        round_decimal   = 2
        break

    elif (input_num == '2') or (input_num == 'eth') or (input_num == 'ETH'):
        coin            = "ETH"
        quantity        = 0.07      # 1USDT == 0.07 ETH @ 1400
        leverage        = 100       # Maximum 100
        threshold       = 0.15
        stoplimit       = 0.12
        callbackRate    = 0.2
        round_decimal   = 2
        break

    elif (input_num == '3') or (input_num == 'ltc') or (input_num == 'LTC'):
        coin            = "LTC"
        quantity        = 0.4       # 1USDT == 0.4 LTC @ 165
        leverage        = 75        # Maximum 75
        threshold       = 0.15
        stoplimit       = 0.12
        callbackRate    = 0.2
        round_decimal   = 2
        break

    elif (input_num == '4') or (input_num == 'bch') or (input_num == 'BCH'):
        coin            = "BCH"
        quantity        = 0.12      # 1USDT == 0.12 BCH @ 535
        leverage        = 75        # Maximum 75
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
