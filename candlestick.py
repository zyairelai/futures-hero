import config, os
import binance_futures
from datetime import datetime
from termcolor import colored
troubleshooting = config.troubleshooting

def open(klines)  : return float(klines[-1][1])
def high(klines)  : return float(klines[-1][2])
def low(klines)   : return float(klines[-1][3])
def close(klines) : return float(klines[-1][4])
def timestamp_of(kline): return kline[-1][0]

def candle_body(klines): return abs(open(klines) - close(klines))

def upper_wick(klines):
    if candle_color(klines) == "GREEN": return high(klines) - close(klines)
    elif candle_color(klines) == "RED": return high(klines) - open(klines)
    else: return 0

def lower_wick(klines):
    if candle_color(klines) == "GREEN": return open(klines) - low(klines)
    elif candle_color(klines) == "RED": return close(klines) - low(klines)
    else: return 0

def candle_color(klines):
    if close(klines) > open(klines): color = "GREEN"
    elif close(klines) < open(klines): color = "RED"
    else: "INDECISIVE"
    return color

def strong_candle(klines):
    if candle_body(klines) > lower_wick(klines) or candle_body(klines) > upper_wick(klines):
        if candle_color(klines) == "GREEN":
            if candle_body(klines) > lower_wick(klines) or lower_wick(klines) > (upper_wick(klines) + candle_body(klines)): return True
        elif candle_color(klines) == "RED":
            if candle_body(klines) > upper_wick(klines) or upper_wick(klines) > (lower_wick(klines) + candle_body(klines)): return True
