import time
import requests
import json

bitmex_api_key = "l5KV6v4EXPgBlyH9wfW53Th2"
bitmex_api_secret = "NHehO9cXQg5x30uDqGrFFYDc0hO-cPVtIMkTy7HxEixLf9ZX"

import bitmex
client = bitmex.bitmex()

binSize='1m' # You can change the bin size as needed
past_minute_data = client.Trade.Trade_getBucketed(binSize=binSize, count=1, symbol="ETHUSD", reverse=True).result()[0][0]

processed_min_data = {}
timestamp_minute = str(past_minute_data["timestamp"]).split(':')[0] + ":" + str(past_minute_data["timestamp"]).split(':')[1] + ":00"

processed_min_data["symbol"] = past_minute_data["symbol"]
processed_min_data["Date"] = timestamp_minute
processed_min_data["Open"] = past_minute_data["open"]
processed_min_data["Close"] = past_minute_data["close"]
processed_min_data["Volume"] = past_minute_data["volume"]
processed_min_data["High"] = past_minute_data["high"]
processed_min_data["Low"] = past_minute_data["low"]