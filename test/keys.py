import os
from binance.client import Client

# Paste the following into your Default Shell
# export API_OWNER="binance_username"
# export API_KEY="binance_api_key"
# export API_SECRET="binance_secret_key"

# Get environment variables
api_owner   = os.environ.get('API_OWNER')
api_key     = os.environ.get('API_KEY')
api_secret  = os.environ.get('API_SECRET')
client      = Client(api_key, api_secret)
