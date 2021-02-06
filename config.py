live_trade      = True
clear_direction = True      # True to minimize lose, False to maximize profit

# Asset Configuration
coin            = "BTC"
quantity        = 0.003     # Minimum 0.001
leverage        = 50        # Maximum 125 // Recommended 75-99 // Oracle 50x
round_decimal   = 2
exit_threshold  = 0.1       # Used in double_confirm() and standard_main_hour()

pair = coin + "USDT"
print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print()
