live_trade      = True    # False to see the output & verify your API key is working
troubleshooting = False   # Troubleshooting mode for @zyairelai

# ====================================================
#                  Prompt User Input
# ====================================================
print("Which pair do you want to trade?")
print("1. BTC_USDT")
print("2. ETH_USDT")
# print("3. BNB_USDT")
# Add More Coins Here

# print("0. Others")
user_input = input("\nEnter a number   :   ")
# ====================================================
#                 Asset Configuration
# ====================================================
if user_input == '0':
    coin = input("Enter COIN_SYMBOL:   ").upper()
    quantity = input("Enter Trade Qty  :   ")

elif user_input == '2':
    coin     = "ETH"
    quantity = 0.01

elif user_input == '3':
    coin     = "BNB"
    quantity = 0.05

# You can add more coins here

else:
    coin     = "BTC"
    quantity = 0.001

# ====================================================
#        !! DO NOT CHANGE THESE LEVERAGE !!
# ====================================================
if   coin == "BTC": leverage = 125
elif coin == "ETH": leverage = 100
else: leverage = 75
# ====================================================
#               Output Settings Status
# ====================================================
pair = coin + "USDT"
print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print()
