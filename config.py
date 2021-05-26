live_trade  = False
throttle    = False

# The Risk_Level model to choose.
# Read the first line for each risk_level_x.py module
risk_level = [ 2 ]

coin     = ["BTC"]
quantity = [0.001]

# ====================================================
#        !! DO NOT CHANGE THE LEVERAGE !!
# ====================================================
leverage, pair = [], []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    if   coin[i] == "BTC": leverage.append(40)
    elif coin[i] == "ETH": leverage.append(30)
    else: leverage.append(20)

    print("Pair Name        :   " + pair[i])
    print("Trade Quantity   :   " + str(quantity[i]) + " " + coin[i])
    print("Leverage         :   " + str(leverage[i]))
    print()

# ====================================================
#       Troubleshooting mode for @zyairelai
# ====================================================
troubleshooting = False
clear_direction = True
