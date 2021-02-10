live_trade      = True      # False to see the output && verify your API key is working
clear_direction = True      # True to minimize lose, False to maximize profit

while True:
    print("\nHere are the supported Pairs: ")
    print("1. BTC-USDT")
    print("2. ETH-USDT")
    print("3. LTC-USDT")
    print("4. BNB-USDT")
    print("5. BCH-USDT")
    print("6. EOS-USDT")
    print("7. LINK-USDT")
    print("8. XRP-USDT")
    # print("9. ")
    # print("0. Others (Require More Input)")

    input_pair = input("\nChoose your Pair :   ").upper() or 'BTC'

    if (input_pair == '1') or (input_pair == 'BTC'):
        coin            = "BTC"
        quantity        = 0.001     # Minimum 0.001, if good trending it will raise up to 3x of this amount
        leverage        = 25        # Maximum 125 // Recommended 25-35 // Oracle 50x
        round_decimal   = 2         # Some crypto pairs like chainlink read up to 3 decimal place of USDT
        break

    elif (input_pair == '2') or (input_pair == 'ETH'):
        coin            = "ETH"
        quantity        = 0.01
        leverage        = 20        # Maximum 100 // Recommended 20-30 // Oracle 40x
        round_decimal   = 2
        break

    elif (input_pair == '3') or (input_pair == 'LTC'):
        coin            = "LTC"
        quantity        = 0.05
        leverage        = 15
        round_decimal   = 2
        break

    elif (input_pair == '4') or (input_pair == 'BNB'):
        coin            = "BNB"
        quantity        = 0.05
        leverage        = 15
        round_decimal   = 3
        break

    elif (input_pair == '5') or (input_pair == 'BCH'):
        coin            = "BCH"
        quantity        = 0.01
        leverage        = 15
        round_decimal   = 2
        break

    elif (input_pair == '6') or (input_pair == 'EOS'):
        coin            = "EOS"
        quantity        = 2
        leverage        = 15
        round_decimal   = 3
        break

    elif (input_pair == '7') or (input_pair == 'LINK'):
        coin            = "LINK"
        quantity        = 0.5
        leverage        = 15
        round_decimal   = 3
        break

    elif (input_pair == '8') or (input_pair == 'XRP'):
        coin            = "XRP"
        quantity        = 10
        leverage        = 15
        round_decimal   = 4
        break

    else: print("❗Invalid Number❗Try again❗\n")

pair = coin + "USDT"
print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print()
