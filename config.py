while True:
    print("\nHere are the supported Pairs: ")
    print("1. BTC-USDT")
    print("2. ETH-USDT")
    # print("3. LTC-USDT")

    input_pair = input("\nChoose your Pair :   ").upper() or 'BTC'

    if (input_pair == '1') or (input_pair == 'BTC'):
        coin            = "BTC"
        quantity        = 0.001
        leverage        = 75        # Maximum 125
        threshold       = 0.15      # Optimal 0.15 for entry
        exit_threshold  = 0.2
        stoplimit       = 0.2       # shall be 70-100% of threshold
        round_decimal   = 2
        break

    elif (input_pair == '2') or (input_pair == 'ETH'):
        coin            = "ETH"
        quantity        = 0.04
        leverage        = 50        # Maximum 100
        threshold       = 0.15
        stoplimit       = 0.20
        round_decimal   = 2
        break

    # elif (input_pair == '3') or (input_pair == 'LTC'):
    #     coin            = "LTC"
    #     quantity        = 0.5
    #     leverage        = 30        # Maximum 75
    #     threshold       = 0.15
    #     stoplimit       = 0.20
    #     round_decimal   = 2
    #     break

    else: print("❗Invalid Number❗Try again❗\n")

pair = coin + "USDT"

print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print("Leverage         :   " + str(leverage) + "x")
print("Price Movement   :   " + str(threshold) + " %")
print("Stop Limit       :   " + str(stoplimit) + " %")
print("Round Decimal    :   " + str(round_decimal) + " decimal place")
print()
