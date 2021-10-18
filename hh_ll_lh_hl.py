import numpy as np
import pandas as pd
import ccxt

pair = 'BTC/USDT'
timeframe = '1m'

client = ccxt.binanceusdm()

data = client.fetch_ohlcv(pair, timeframe, limit=1500)

ohlcv = pd.DataFrame(data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
ohlcv = ohlcv.set_index('timestamp')
ohlcv.index = pd.to_datetime(ohlcv.index, unit='ms')

high = None
low = None

for i in range(len(ohlcv.index) + 1):
    if i == 0: # Print timestamp of first candle to debug
        print(f'{ohlcv.index[i]} - First candle')
    
    try:
        if i >= 2: # We need first 2 bars to look back on
            if  ohlcv['high'][i] >= ohlcv['high'][i - 2] and\
                ohlcv['high'][i] >= ohlcv['high'][i - 1] and\
                ohlcv['high'][i] >= ohlcv['high'][i + 2] and\
                ohlcv['high'][i] >= ohlcv['high'][i + 1]:
                
                if high == None:
                    high = {'timestamp': ohlcv.index[i], 'high': ohlcv['high'][i], 'type': 'hh'}
                elif ohlcv['close'][i] > high['high']:
                    high = {'timestamp': ohlcv.index[i], 'high': ohlcv['high'][i], 'type': 'hh'}
                else:
                    high = {'timestamp': ohlcv.index[i], 'high': ohlcv['high'][i], 'type': 'lh'}
                    
                print(f'{high["timestamp"]} - {high["type"]}  {high["high"]}')
            
            if  ohlcv['low'][i] <= ohlcv['low'][i - 2] and\
                ohlcv['low'][i] <= ohlcv['low'][i - 1] and\
                ohlcv['low'][i] <= ohlcv['low'][i + 2] and\
                ohlcv['low'][i] <= ohlcv['low'][i + 1]:

                if low == None:
                    low = {'timestamp': ohlcv.index[i], 'low': ohlcv['low'][i], 'type': 'll'}
                elif ohlcv['close'][i] < low['low']:
                    low = {'timestamp': ohlcv.index[i], 'low': ohlcv['low'][i], 'type': 'll'}
                else:
                    low = {'timestamp': ohlcv.index[i], 'low': ohlcv['low'][i], 'type': 'hl'}
                
                print(f'{low["timestamp"]} - {low["type"]}  {low["low"]}')
    
    except IndexError:
        continue