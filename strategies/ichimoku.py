import modules.candlestick

test_module = False

def futures_hero(pair):
    # Fetch the raw klines data
    dataset = modules.candlestick.get_klines(pair, '1h')

    # Define Threshold
    conversion_line_period = 9
    base_line_period = 26
    lead_span_b_period = 52
    displacement = 1

    # Conversion Line / Tenkan Sen
    cl_high = dataset['high'].rolling(conversion_line_period).max()
    cl_low = dataset['low'].rolling(conversion_line_period).min()
    dataset['conversion_line'] = (cl_high + cl_low) / 2

    # Base Line / Kijun Sen
    bl_high = dataset['high'].rolling(base_line_period).max()
    bl_low = dataset['low'].rolling(base_line_period).min()
    dataset['base_line'] = (bl_high + bl_low) / 2

    # Leading Span A / Senkou Sen A
    dataset['green_line'] = ((dataset.conversion_line + dataset.base_line) / 2)

    # Leading Span B / Senkou Sen B
    lead_span_b_high = dataset['high'].rolling(lead_span_b_period).max()
    lead_span_b_low = dataset['low'].rolling(lead_span_b_period).min()
    dataset['red_line'] = ((lead_span_b_high + lead_span_b_low) / 2)

    # Displacement / Lagging Span / Chikou Span 
    dataset['lagging_span'] = dataset['close'].shift(-displacement)

    clean = dataset[["timestamp", "open", "high", "low", "close", "volume", "green_line", "red_line"]].copy()
    
    # Apply Place Order Condition
    clean["GO_LONG"] = clean.apply(GO_LONG_CONDITION, axis=1)
    clean["GO_SHORT"] = clean.apply(GO_SHORT_CONDITION, axis=1)
    clean["EXIT_LONG"] = clean.apply(EXIT_LONG_CONDITION, axis=1)
    clean["EXIT_SHORT"] = clean.apply(EXIT_SHORT_CONDITION, axis=1)
    clean.dropna(inplace=True)

    return clean

indicator = "close"

def GO_LONG_CONDITION(dataset):
    if  dataset["green_line"] > dataset["red_line"] and \
        dataset["green_line"] < dataset[indicator] : return True
    else: return False

def GO_SHORT_CONDITION(dataset):
    if  dataset["red_line"] > dataset["green_line"] and \
        dataset["red_line"] > dataset[indicator] : return True
    else: return False

def EXIT_LONG_CONDITION(dataset):
    if dataset[indicator] < dataset["green_line"] : return True
    else: return False

def EXIT_SHORT_CONDITION(dataset):
    if dataset[indicator] > dataset["green_line"] : return True
    else: return False

if test_module:
    run = futures_hero("BTCUSDT")
    print(run)