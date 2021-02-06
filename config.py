live_trade      = True
output          = False     # Always False, True For Troubleshooting

# Asset Configuration
coin            = "BTC"
quantity        = 0.001     # Minimum 0.001
leverage        = 40        # Maximum 125 // Recommended 75-99 // Oracle 50x
round_decimal   = 2
exit_threshold  = 0.1       # Used in double_confirm() and standard_main_hour()

# Strategy
main_hour       = 6         # Use either 6 hour or 4 hour as main trend
clear_direction = True      # True to minimize lose, False to maximize profit

pair = coin + "USDT"
print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print()
