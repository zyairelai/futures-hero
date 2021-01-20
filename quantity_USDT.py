def calculate_Quantity():
    coin            = "BTC"
    pair            = "BTCUSDT"
    quantity        = 0.003     # 1USDT == 0.003 BTC @ 37XXX
    leverage        = 125       # Maximum 125
    threshold       = 0.15      # Optimal 0.15 for entry
    stoplimit       = 0.12      # shall be 70-100% of threshold
    callbackRate    = 0.2
    round_decimal   = 2