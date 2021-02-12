# futures-omax
Leverage Trading Automation on Binance Futures.

# DISCLAIMER

This automation software is purely handcoded by me [@zyairelai](https://github.com/zyairelai) from scratch with my personal manual trading strategy.  
Kindly provide feedback through my email `zyairelai@gmail.com` if you are using my repository.  
If you had modified or improved my code feel free to share with me and we may have futher discussion on this project!  
Anybody may copy, redistribute, modify of the software. However, limited to NON-COMMERCIAL USED only.  
LEVERAGE TRADING IS A HIGH RISK GAME. PLEASE MANAGE YOUR RISK LEVEL BEFORE USING MY SCRIPT.

## 1. Environment Setup
Paste the following into your Default Shell
```
export API_OWNER="your_binance_username"
export API_KEY="your_binance_api_key"
export API_SECRET="your_binance_secret_key"
```

Or as an alternative, you can change `line 7-10` in `binance_futures.py` to following: 
```
api_owner   = "your_binance_username"
api_key     = "your_binance_api_key"
api_secret  = "your_binance_secret_key"
client      = Client(api_key, api_secret)
```

## 2. Pip3 Requirements
You need to have these libraries installed:
```
pip3 install apscheduler==3.6.3
pip3 install cryptography==3.2 
pip3 install python-binance==0.7.5
pip3 install termcolor==1.1.0
```

## 3. Run
Let's make the magic happens!
```
python3 run.py
```
To check the trend, position, realizedPNL and many others:
```
python3 check.py
```

## 4. Donate for MORE!!
If you found this useful to generate your passive income, feel free to donate to me so I can IMPROVE MORE!  
```
BTC  (BTC)   : 15VowsyMp9A5DWbKbZEVt4A4r7dQQgddtn
ETH  (ERC20) : 0x7701948f0477e629c5bb5d79f99b833133ab30d5
USDT (ERC20) : 0x7701948f0477e629c5bb5d79f99b833133ab30d5
```
