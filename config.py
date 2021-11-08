live_trade = False

coin     = ["ETH"]
quantity = [0.002]

# For Backtesting Multiple Pairs
# coin     = ["BTC", "ETH", "BNB", "BCH", "LTC", "XRP", "ADA", "EOS"]
# quantity = [1, 1, 1, 1, 1, 1, 1, 1]

# ====================================================
#        !! DO NOT CHANGE THE LEVERAGE !!
# ====================================================
leverage, pair = [], []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    if   coin[i] == "BTC": leverage.append(50)
    elif coin[i] == "ETH": leverage.append(40)
    else: leverage.append(30)

    print("Pair Name        :   " + pair[i])
    print("Trade Quantity   :   " + str(quantity[i]) + " " + coin[i])
    print("Leverage         :   " + str(leverage[i]))
    print()
