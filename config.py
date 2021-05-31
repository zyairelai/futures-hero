live_trade = False

# Adding to the losing position to pull back the entry price (Liquidation on Binance is when you hit 80%)
enable_throttle = False

# Cut loss when the percentage hits, enabled this will not trigger Throttle :)
enable_stoploss = True
stoploss_percentage = 50

# The Risk_Level model to choose.
# Read the first line for each risk_level_x.py module
risk_level = [ 3 ]

coin     = ["BTC"]
quantity = [0.001]

# profit_margin * leverage = Actual Profit Percentage.
# Minimum is 0.1 to cover the fees!!!
profit_margin = 0.2

# ====================================================
#        !! DO NOT CHANGE THE LEVERAGE !!
# ====================================================
leverage, pair = [], []
for i in range(len(coin)):
    pair.append(coin[i] + "USDT")
    if   coin[i] == "BTC": leverage.append(60)
    elif coin[i] == "ETH": leverage.append(40)
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
