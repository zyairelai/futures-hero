import candlestick
import heikin_ashi

def strong_trend(klines):
    if candlestick.candle_color(klines) == "GREEN" and candlestick.strong_candle(klines) and heikin_ashi.VALID_CANDLE(klines) == "GREEN": return "GREEN"
    elif candlestick.candle_color(klines) == "RED" and candlestick.strong_candle(klines) and heikin_ashi.VALID_CANDLE(klines) == "RED" : return "RED"

def both_color(klines):
    if candlestick.candle_color(klines) == "GREEN" and heikin_ashi.VALID_CANDLE(klines) == "GREEN": return "GREEN"
    elif candlestick.candle_color(klines) == "RED" and heikin_ashi.VALID_CANDLE(klines) == "RED" : return "RED"

def reversal(klines):
    if heikin_ashi.VALID_CANDLE(klines) == "GREEN" and candlestick.candle_color(klines) == "RED": return True
    elif heikin_ashi.VALID_CANDLE(klines) == "RED" and candlestick.candle_color(klines) == "GREEN": return True
