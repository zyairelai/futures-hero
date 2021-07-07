def compute(digit, dataset):
    import pandas as pd
    df = pd.DataFrame(dataset)
    ema = df.ewm(span=digit).mean()
    return ema[0].values.tolist()

def current(EMA_list) : return float(EMA_list[-1])
def previous(EMA_list): return float(EMA_list[-2])

def HIGHEST_LINE(low, mid, high):
    current_lines = [current(low), current(mid), current(high)]
    return max(current_lines)

def MIDDLE_LINE(low, mid, high):
    current_lines = [current(low), current(mid), current(high)]
    return sorted(current_lines)[1]

def LOWEST_LINE(low, mid, high):
    current_lines = [current(low), current(mid), current(high)]
    return min(current_lines)

def UPWARD_MOVEMENT(EMA_list):
    if current(EMA_list) > previous(EMA_list): return True

def DOWNWARD_MOVEMENT(EMA_list):
    if current(EMA_list) < previous(EMA_list): return True

def DELTA_UPWARD(low, mid, high):
    if UPWARD_MOVEMENT(low) and UPWARD_MOVEMENT(mid) and UPWARD_MOVEMENT(high): return True

def DELTA_DOWNWARD(low, mid, high):
    if DOWNWARD_MOVEMENT(low) and DOWNWARD_MOVEMENT(mid) and DOWNWARD_MOVEMENT(high): return True

def ABSOLUTE_UPTREND(low, mid, high):
    if current(low) > current(mid) and current(mid) > current(high) and DELTA_UPWARD(low, mid, high): return True

def ABSOLUTE_DOWNTREND(low, mid, high):
    if current(high) > current(mid) and current(mid) > current(low) and DELTA_DOWNWARD(low, mid, high): return True
