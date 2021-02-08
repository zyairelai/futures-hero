live_trade      = True      # False to see the output && verify your API key is working
clear_direction = True      # True to minimize lose, False to maximize profit

# Asset Configuration
coin            = "BTC"
quantity        = 0.001     # Minimum 0.001, if good trending it will raise up to 3x of this amount
leverage        = 30        # Maximum 125 // Recommended 75-99 // Oracle 50x
round_decimal   = 2

pair = coin + "USDT"
print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print()
