# leverage-bot
Leverage Trading Bot on Binance Futures. 

## 1. Requirements
You need to have these libraries installed:
```
pip3 install termcolor==1.1.0
pip3 install cryptography==3.2 
pip3 install python-binance==0.7.5
```
## 2. Environment Setup
Paste the following into your Default Shell
```
export API_OWNER="your_binance_username"
export API_KEY="your_binance_api_key"
export API_SECRET="your_binance_secret_key"
```
To check if your key is saved by your environment, run `python3 check/keys.py`