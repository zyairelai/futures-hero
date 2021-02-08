live_trade      = True
clear_direction = True      # True to minimize lose, False to maximize profit

# Asset Configuration
coin            = "BTC"
quantity        = 0.003     # Minimum 0.001
leverage        = 125       # Maximum 125 // Recommended 75-99 // Oracle 50x
round_decimal   = 2

pair = coin + "USDT"
print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print()
