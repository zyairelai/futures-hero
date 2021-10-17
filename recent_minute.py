negative_six = -6
def initial_Open(klines)  : return (float(klines[negative_six][1]) + float(klines[negative_six][4])) / 2
def initial_Close(klines) : return (float(klines[negative_six][1]) + float(klines[negative_six][2]) + float(klines[negative_six][3]) + float(klines[negative_six][4])) / 4

negative_five = -5
def firstrun_Open(klines) : return float((initial_Open(klines) + initial_Close(klines)) / 2)
def firstrun_Close(klines): return (float(klines[negative_five][1]) + float(klines[negative_five][2]) + float(klines[negative_five][3]) + float(klines[negative_five][4])) / 4
def firstrun_High(klines) : return max(float(klines[negative_five][2]), firstrun_Open(klines), firstrun_Close(klines))
def firstrun_Low(klines)  : return min(float(klines[negative_five][3]), firstrun_Open(klines), firstrun_Close(klines))
def firstrun_candle(klines): return candle_color(firstrun_Open(klines), firstrun_Close(klines))

negative_four = -4
def fourth_Open(klines)  : return (float(klines[negative_four][1]) + float(klines[negative_four][4])) / 2
def fourth_Close(klines) : return (float(klines[negative_four][1]) + float(klines[negative_four][2]) + float(klines[negative_four][3]) + float(klines[negative_four][4])) / 4
def fourth_High(klines)  : return max(float(klines[negative_four][2]), firstrun_Open(klines), firstrun_Close(klines))
def fourth_Low(klines)   : return min(float(klines[negative_four][3]), firstrun_Open(klines), firstrun_Close(klines))
def fourth_candle(klines): return candle_color(fourth_Open(klines), fourth_Close(klines))

negative_three = -3
def third_Open(klines)   : return float((fourth_Open(klines) + fourth_Close(klines)) / 2)
def third_Close(klines)  : return (float(klines[negative_three][1]) + float(klines[negative_three][2]) + float(klines[negative_three][3]) + float(klines[negative_three][4])) / 4
def third_High(klines)   : return max(float(klines[negative_three][2]), third_Open(klines), third_Close(klines))
def third_Low(klines)    : return min(float(klines[negative_three][3]), third_Open(klines), third_Close(klines))
def third_candle(klines) : return candle_color(third_Open(klines), third_Close(klines))

negative_two = -2
def second_Open(klines)  : return float((third_Open(klines) + third_Close(klines)) / 2)
def second_Close(klines) : return (float(klines[negative_two][1]) + float(klines[negative_two][2]) + float(klines[negative_two][3]) + float(klines[negative_two][4])) / 4
def second_High(klines)  : return max(float(klines[negative_two][2]), second_Open(klines), second_Close(klines))
def second_Low(klines)   : return min(float(klines[negative_two][3]), second_Open(klines), second_Close(klines))
def second_candle(klines): return candle_color(second_Open(klines), second_Close(klines))

negative_one = -1
def current_open(klines) : return float((second_Open(klines) + second_Close(klines)) / 2)
def current_close(klines): return (float(klines[negative_one][1]) + float(klines[negative_one][2]) + float(klines[negative_one][3]) + float(klines[negative_one][4])) / 4
def current_high(klines) : return max(float(klines[negative_one][2]), current_open(klines), current_close(klines))
def current_low(klines)  : return min(float(klines[negative_one][3]), current_open(klines), current_close(klines))
def current_candle(klines): return candle_color(current_open(klines), current_close(klines))

def candle_color(open_candle, close_candle):
    if close_candle > open_candle: return "GREEN"
    elif open_candle > close_candle: return "RED"
    else: return "NO_MOVEMENT"

def recent_candles(klines):
    if  current_candle(klines) == "GREEN" and \
        firstrun_candle(klines) == "GREEN" and second_candle(klines) == "GREEN" and \
        third_candle(klines) == "GREEN" and fourth_candle(klines) == "GREEN" : return "GREEN"

    elif current_candle(klines) == "RED" and \
        firstrun_candle(klines) == "RED" and second_candle(klines) == "RED" and \
        third_candle(klines) == "RED" and fourth_candle(klines) == "RED" : return "RED"
