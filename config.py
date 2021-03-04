live_trade      = True      # False to see the output & verify your API key is working
troubleshooting = False     # Troubleshooting mode for @zyairelai

# ====================================================
# Prompt User Input
# ====================================================
print("Which pair do you want to trade?")
print("1. BTC_USDT")
print("2. ETH_USDT")
print("3. BNB_USDT")
# print("4. LTC_USDT")
# print("5. ADA_USDT")
# print("6. BCH_USDT")
# print("7. DOT_USDT")
# print("8. EOS_USDT")
# print("9. LINK_USDT")
# print("0. Others")
user_input = input("\nEnter a number   :   ")

# ====================================================
# Asset Configuration
# ====================================================
if user_input == '0':
    coin = input("Enter COIN SYMBOL:   ").upper()
    quantity = input("Enter Trade Qty  :   ")

elif user_input == '2':
    coin        = "ETH"
    quantity    = 0.01      # 0.1 @1520 == $5.64

elif user_input == '3':
    coin        = "BNB"
    quantity    = 0.1       # 1 @252 == $10.08

# ====================================================
# Coins below are adjusted to approx ~$10 EXCEPT BTC
# ====================================================
elif user_input == '4':
    coin        = "LTC"
    quantity    = 1.5

elif user_input == '5':
    coin        = "ADA"
    quantity    = 200

elif user_input == '6':
    coin        = "BCH"
    quantity    = 0.5

elif user_input == '7':
    coin        = "DOT"
    quantity    = 10

elif user_input == '8':
    coin        = "EOS"
    quantity    = 100

elif user_input == '9':
    coin        = "LINK"
    quantity    = 10

else:
    coin        = "BTC"
    quantity    = 0.001     # Minimum 0.001

# ====================================================
# Adjust Optimal Leverage
# ====================================================
if   coin == "BTC": leverage = 50
elif coin == "ETH": leverage = 40
else: leverage = 30

pair = coin + "USDT"
print("Pair Name        :   " + str(pair))
print("Trade Quantity   :   " + str(quantity) + " " + str(coin))
print("Set Levarage     :   " + str(leverage))
print()
