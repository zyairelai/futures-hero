while True:
    print("\nHere are the supported Pairs: ")
    print("1. BTC-USDT")
    print("2. ETH-USDT")
    print("3. LTC-USDT")

    input_pair = input("\nChoose your Pair :   ").upper() or 'BTC'

    if (input_pair == '1') or (input_pair == 'BTC'):
        coin            = "BTC"
        quantity        = 0.001     # Minimum 0.001
        leverage        = 75        # Maximum 125 // Recommended 75-99
        threshold       = 0.15
        round_decimal   = 2
        break

    elif (input_pair == '2') or (input_pair == 'ETH'):
        coin            = "ETH"
        quantity        = 0.01      # Minimum 0.01
        leverage        = 50        # Maximum 100 // Recommended 50-75
        threshold       = 0.15
        round_decimal   = 2
        break

    elif (input_pair == '3') or (input_pair == 'LTC'):
        coin            = "LTC"
        quantity        = 0.05      # Minimum 0.01
        leverage        = 30        # Maximum 75 // Recommended 30-45
        threshold       = 0.15
        round_decimal   = 2
        break
    else: print("❗Invalid Number❗Try again❗\n")

universal_threshold = 0.15
pair = coin + "USDT"

print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
# print("Leverage         :   " + str(leverage) + "x")
import binance_futures
print("Current Leverage :   " + binance_futures.position_information()[0].get("leverage") + "x\n")