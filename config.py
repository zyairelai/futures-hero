live_trade      = True      # False to see the output & verify your API key is working
clear_direction = False     # True to minimize lose, False to maximize profit
troubleshooting = False     # Troubleshooting mode for @zyairelai

print("Which pair do you want to trade?")
print("1. BTC_USDT")
print("2. ETH_USDT")
user_input = input("\nEnter a number   :   ") or '1'

# Asset Configuration

if user_input == '2':
    coin            = "ETH"
    quantity        = 0.01
    leverage        = 40
    round_decimal   = 1

else:
    coin            = "BTC"
    quantity        = 0.001     # Minimum 0.001, if good trending it will raise up to 3x of this amount
    leverage        = 50        # Maximum 125 // Recommended 30-40
    round_decimal   = 0         # Some crypto pairs like chainlink read up to 3 decimal place of USDT

pair = coin + "USDT"
print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print("Set Levarage     :   " + str(leverage))
print()
