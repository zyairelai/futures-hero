import os
import time
import numpy as np
from binance.client import Client
import trend 

start = time.time()

result = trend.get_current_trend()
print(result)

print(f"{time.time() - start} seconds\n")