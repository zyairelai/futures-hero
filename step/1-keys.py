import os
from binance.client import Client

# Paste the following into your Default Shell
"""
export API_OWNER="your_binance_username"
export API_KEY="your_api_key"
export API_SECRET="your_secret_key"
"""

# Get environment variables
api_owner   = os.environ.get('API_OWNER')
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')

# Check Your Environment
print("API OWNER        :   " + api_owner)
print("API Key          :   " + api_key)
print("API Secret Key   :   " + api_secret)

# Create Object to call Python Function
# client = Client(keys.api_key, keys.api_secret)

# Historical BLVT NAV Kline/Candlestick 
# https://binance-docs.github.io/apidocs/futures/en/#taker-buy-sell-volume
# [0] Open Timestamp            
# [1] Open                      HA_Open   = (previous HA_Open + previous HA_Close) / 2
# [2] High                      HA_Close  = (Open + High + Low + Close) / 4
# [3] Low                       HA_High   = maximum of High, HA_Open, HA_Close
# [4] Close                     HA_Low    = minimum of Low, HA_Open, HA_Close