live_trade      = True      # False to see the output & verify your API key is working
troubleshooting = False     # Troubleshooting mode for @zyairelai

print("Which pair do you want to trade?")
print("1. BTC_USDT")
print("2. ETH_USDT")
print("3. BNB_USDT")
user_input = input("\nEnter a number   :   ")

# Asset Configuration
if user_input == '2':
    coin            = "ETH"
    quantity        = 0.01      # 0.1 @1520 == $5.64
    leverage        = 30

elif user_input == '3':
    coin            = "BNB"
    quantity        = 0.1       # 1 @252 == $10.08
    leverage        = 25

else:
    coin            = "BTC"
    quantity        = 0.001     # Minimum 0.001, if good trending it will raise up to 3x of this amount // 0.01 @47500 == $12
    leverage        = 40        # Maximum 125 // Recommended 30-40

pair = coin + "USDT"
print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print("Set Levarage     :   " + str(leverage))
print()
