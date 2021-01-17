import os
import time
from binance.client import Client
def get_timestamp(): return int(time.time() * 1000)

input_num = input("1. BTC\n" + "2. ETH\n" + "3. LINK\n" + "4. SUSHI\n" + "[+] Enter Number: ")
if input_num == '1': coin = "BTC"
elif input_num == '2': coin = "ETH"
elif input_num == '3': coin = "LINK"
elif input_num == '4': coin = "SUSHI"
else: coin = "BTC"
pair = coin + "USDT"

# Get environment variables
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)

# RealizedPNL
i , overall_PNL = 0, 0 
trades_list = client.futures_account_trades(symbol=pair, timestamp=get_timestamp(), limit=100)
for trade in trades_list:
    overall_PNL = overall_PNL + float(trade.get('realizedPnl'))
    if (float(trade.get('realizedPnl'))) > 0 : 
        i = i + 1
        print(str(i) + ".  " + trade.get('realizedPnl'))
    elif (float(trade.get('realizedPnl'))) < 0 : 
        i = i + 1
        print(str(i) + ". " + trade.get('realizedPnl') + " LOSER TRADE")
    else: continue

print("\n[!] Overall PNL over the last 50 trades: " + str(overall_PNL) + "\n")