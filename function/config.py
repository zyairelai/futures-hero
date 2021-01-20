while True:
    print("\nHere are the supported Pairs: ")
    print("1. BTC-USDT")
    print("2. ETH-USDT")
    print("3. LTC-USDT")

    input_pair = input("\nChoose your Pair :   ").upper() or 'BTC'

    if (input_pair == '1') or (input_pair == 'BTC'):
        coin            = "BTC"
        quantity        = 0.005     # 1USDT == 0.005 @ 35000USDT @ 125x
        leverage        = 125       # Maximum 125
        threshold       = 0.15      # Optimal 0.15 for entry
        stoplimit       = 0.10      # shall be 70-100% of threshold
        callbackRate    = 0.1       # Same as StopLimit == 0.1 , but with secure Profit 
        round_decimal   = 2
        break

    elif (input_pair == '2') or (input_pair == 'ETH'):
        coin            = "ETH"
        quantity        = 0.1       # 1USDT == 0.1 ETH @ 1200USDT @ 100x
        leverage        = 100       # Maximum 100
        threshold       = 0.15
        stoplimit       = 0.1
        callbackRate    = 0.1
        round_decimal   = 2
        break

    elif (input_pair == '3') or (input_pair == 'LTC'):
        coin            = "LTC"
        quantity        = 0.5       # 1USDT == 0.5 LTC @ 150USDT @ 75x
        leverage        = 75        # Maximum 75
        threshold       = 0.15                                  # Might need to increase threshold
        stoplimit       = 0.10                                  # And decrease stoplimit to reduce lose
        callbackRate    = 0.1
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
