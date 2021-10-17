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

swing_high = None
swing_low = None

for i in range(len(ohlcv.index) + 1):
    if i == 0: # Print timestamp of first candle to debug
        print(f'{ohlcv.index[i]} - First candle')
    
    try:
        if i >= 2: # We need first 2 bars to look back on
            if swing_high == None or ohlcv['close'][i] > swing_high:
                if  ohlcv['high'][i] >= ohlcv['high'][i - 2] and\
                    ohlcv['high'][i] >= ohlcv['high'][i - 1] and\
                    ohlcv['high'][i] >= ohlcv['high'][i + 2] and\
                    ohlcv['high'][i] >= ohlcv['high'][i + 1]:
                    swing_high = ohlcv['high'][i]
                    print(f'{ohlcv.index[i]} - Swing high  {swing_high}')
            
            if swing_low == None or ohlcv['close'][i] < swing_low:
                if  ohlcv['low'][i] <= ohlcv['low'][i - 2] and\
                    ohlcv['low'][i] <= ohlcv['low'][i - 1] and\
                    ohlcv['low'][i] <= ohlcv['low'][i + 2] and\
                    ohlcv['low'][i] <= ohlcv['low'][i + 1]:
                    swing_low = ohlcv['low'][i]
                    print(f'{ohlcv.index[i]} - Swing low   {swing_low}')
    
    except IndexError:
        continue