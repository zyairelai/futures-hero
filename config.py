while True:
    print("\nHere are the supported Pairs: ")
    print("1. BTC-USDT")
    print("2. ETH-USDT")

    input_pair = input("\nChoose your Pair :   ").upper() or 'BTC'

    if (input_pair == '1') or (input_pair == 'BTC'):
        coin            = "BTC"
        quantity        = 0.001     # Minimum 0.001
        leverage        = 99        # Maximum 125 // Recommended 75-100
        entry_threshold = 0.15
        exit_threshold  = 0.1
        round_decimal   = 2
        break

    elif (input_pair == '2') or (input_pair == 'ETH'):
        coin            = "ETH"
        quantity        = 0.02      # Minimum 0.01
        leverage        = 75        # Maximum 100 // Recommended 50-75
        entry_threshold = 0.15
        exit_threshold  = 0.1
        round_decimal   = 2
        break

    else: print("❗Invalid Number❗Try again❗\n")

pair = coin + "USDT"

print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print("Leverage         :   " + str(leverage) + "x")
print("Entry Threshold  :   " + str(entry_threshold) + " %")
print("Exit Threshold   :   " + str(exit_threshold) + " %")
print()
