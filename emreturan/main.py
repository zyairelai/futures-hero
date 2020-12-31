import sys
import pandas as pd
from heikin_ashi import heikin_ashi

df = pd.read_csv("ohcl.txt", sep="   ", names=['open','high','low','close'],engine='python')

# heikin_ashi_df = pd.DataFrame(columns=['open', 'high', 'low', 'close'])
# heikin_ashi_df['close'] = (df['open'] + df['high'] + df['low'] + df['close']) / 4

# for i in range(len(df)):
#     if i == 0:
#         heikin_ashi_df.iat[0, 0] = df['open'].iloc[0]
#     else:
#         heikin_ashi_df.iat[i, 0] = (heikin_ashi_df.iat[i-1, 0] + heikin_ashi_df.iat[i-1, 3]) / 2
    
# heikin_ashi_df['high'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['high']).max(axis=1)
# heikin_ashi_df['low'] = heikin_ashi_df.loc[:, ['open', 'close']].join(df['low']).min(axis=1)

heikin_ashi_df = heikin_ashi(df)
print(heikin_ashi_df)