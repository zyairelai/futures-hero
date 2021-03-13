# futures-jackrabbit
Leverage Trading Automation on Binance Futures.  
This is a `Set and Forget` script, means you need to keep it running 24/7 and forget about it.  

# DISCLAIMER
This automation software is purely handcoded by [@zyairelai](https://github.com/zyairelai) from scratch with my personal manual trading strategy.  
Kindly provide feedback through my email `zyairelai@gmail.com` if you are using my repository.  
If you had modified or improved my code feel free to share with me and we may have futher discussion on this project!  
Anybody may copy, redistribute, modify of the software. However, limited to NON-COMMERCIAL USED only.  

LEVERAGE TRADING IS A HIGH RISK GAME.  
PLEASE MANAGE YOUR RISK LEVEL BEFORE USING MY SCRIPT.

# WALLET MANAGEMENT TUTORIAL
This is a very crude, yet, ridiculously simple strategy with high risk high reward.  
Hence, your wallet management skill becomes the priority to your success using this project.  
The recommendation trade amount in this project is 5% of your Futures Wallet as your total trade amount.  
```
For Example, I trade only BTCUSDT.
I have 10 USDT in my Futures Wallet. The maximum amount that I will place for one position is 0.5 USDT.

Second Example, I want to trade both BTCUSDT and ETHUSDT at the same time
I want to place 0.5 USDT for each position.
This will require my Futures Wallet to have at least 20 USDT to do so. 
So I can place 0.5 USDT for BTCUSDT position and 0.5 USDT for ETHUSDT position.
The total trade amount in this case will be 1 USDT, which is 5% of 20 USDT in my whole Futures Wallet.

REMEMBER 5% IS THE KEY
```


## 1. Environment Setup
Paste the following into your Default Shell
```
export API_KEY="your_binance_api_key"
export API_SECRET="your_binance_secret_key"
```

Or as an ALTERNATIVE, you can change `line 7-9` in `binance_futures.py` to following: 
```
api_key     = "your_binance_api_key"
api_secret  = "your_binance_secret_key"
client      = Client(api_key, api_secret)
```

## 2. Pip3 Requirements
You need to have these libraries installed:
```
pip3 install apscheduler==3.6.3
pip3 install cryptography==3.2 
pip3 install python-binance==0.7.9
pip3 install termcolor==1.1.0
```

## 3. Before Running......
Make sure you go to `config.py`, read the comments and adjust your `RISK LEVEL` !  
The script is mainly focusing on `BTC/USDT` and `ETH/USDT` movement pattern.  
If you'd like to test with other pairs, you can tweak around with `config.py`.

## 4. Run
Let's make the magic happens!
```
python3 run.py
```
To check the trend, position, realizedPNL and many others:
```
python3 check.py
```

## 5. Donate for MORE!!
If you found this useful to generate your passive income, feel free to donate to me so I can IMPROVE MORE!  
```
BTC  (BTC)   : 15VowsyMp9A5DWbKbZEVt4A4r7dQQgddtn
ETH  (ERC20) : 0x7701948f0477e629c5bb5d79f99b833133ab30d5
USDT (ERC20) : 0x7701948f0477e629c5bb5d79f99b833133ab30d5
```
