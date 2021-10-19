live_trade = True

coin     = ["DOT", "KSM", "ATOM", "HNT"]
quantity = [3.7, 0.4, 4.3, 7]


# profit_margin * leverage = Actual Profit Percentage.
profit_margin = 0.4

# ====================================================
#        !! DO NOT CHANGE THE LEVERAGE !!
# ====================================================
leverage, pair = [], []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    if   coin[i] == "BTC": leverage.append(50)
    elif coin[i] == "ETH": leverage.append(40)
    else: leverage.append(25)

    print("Pair Name        :   " + pair[i])
    print("Trade Quantity   :   " + str(quantity[i]) + " " + coin[i])
    print("Leverage         :   " + str(leverage[i]))
    print()
