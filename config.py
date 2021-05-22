live_trade  = False
throttle    = False

# Risk level can be set to 1, 2 or 3
risk_level  = 1

coin     = ["BTC"]
quantity = [0.001]
leverage, pair = [], []

# ====================================================
#        !! DO NOT CHANGE THE LEVERAGE !!
# ====================================================
pair = []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    if   coin[i] == "BTC": leverage.append(50)
    elif coin[i] == "ETH": leverage.append(40)
    else: leverage.append(30)

    print("Pair Name        :   " + pair[i])
    print("Trade Quantity   :   " + str(quantity[i]) + " " + coin[i])
    print("Leverage         :   " + str(leverage[i]))
    print()

# Troubleshooting mode for @zyairelai
troubleshooting = False