EMA_threshold = 50

def apply_EMA(dataset):
    dataset['50EMA'] = dataset['close'].ewm(span=EMA_threshold).mean()
    dataset['trend'] = dataset.apply(identify_trend, axis=1)
    clean = dataset[["timestamp", "50EMA", "trend"]].copy()
    return clean

def identify_trend(dataset):
    if dataset['50EMA'] < EMA_threshold : return "UP"
    else: return "DOWN"
