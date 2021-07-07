live_trade = True

# Adding to the losing position to pull back the entry price (Liquidation on Binance is when you hit 80%)
enable_throttle = False

# The Risk_Level model to choose.
risk_level = [ 2 ]

coin     = ["BTC"]
quantity = [0.001]

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
    else: leverage.append(30)

    print("Pair Name        :   " + pair[i])
    print("Trade Quantity   :   " + str(quantity[i]) + " " + coin[i])
    print("Leverage         :   " + str(leverage[i]))
    print()

troubleshooting = False
