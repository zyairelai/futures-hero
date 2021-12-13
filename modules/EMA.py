def apply_EMA(dataset, EMA_threshold):
    dataset[str(EMA_threshold) + 'EMA'] = dataset['close'].ewm(span=EMA_threshold).mean()
    clean = dataset[["timestamp", str(EMA_threshold) + "EMA"]].copy()
    return clean
