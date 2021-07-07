import config, get_position, HA_current, HA_previous, EMA

EMA_low, EMA_mid, EMA_high = 5,8,13

def GO_LONG(mark_price, klines_1min, klines_5min, klines_1HOUR):
    if  HA_current.war_formation(mark_price, klines_1min) and \
        HA_current.heikin_ashi(mark_price, klines_1min)  == "GREEN" and \
        HA_current.heikin_ashi(mark_price, klines_5min)  == "GREEN" and \
        HA_current.heikin_ashi(mark_price, klines_1HOUR) == "GREEN": return True

def GO_SHORT(mark_price, klines_1min, klines_5min, klines_1HOUR):
    if  HA_current.war_formation(mark_price, klines_1min) and \
        HA_current.heikin_ashi(mark_price, klines_1min)  == "RED" and \
        HA_current.heikin_ashi(mark_price, klines_5min)  == "RED" and \
        HA_current.heikin_ashi(mark_price, klines_1HOUR) == "RED": return True

def GO_LONG_FOCUS(mark_price, klines_1min, klines_1HOUR):
    if  HA_current.war_formation(mark_price, klines_1min) and \
        HA_current.heikin_ashi(mark_price, klines_1min)  == "GREEN" and \
        HA_current.heikin_ashi(mark_price, klines_1HOUR) == "GREEN": return True

def GO_SHORT_FOCUS(mark_price, klines_1min, klines_1HOUR):
    if  HA_current.war_formation(mark_price, klines_1min) and \
        HA_current.heikin_ashi(mark_price, klines_1min)  == "RED" and \
        HA_current.heikin_ashi(mark_price, klines_1HOUR) == "RED": return True

def GO_LONG_EMA(mark_price, klines_1min, klines_1HOUR):
    dataset = HA_current.closing_price_list(klines_1min)
    low  = EMA.compute(EMA_low, dataset)
    mid  = EMA.compute(EMA_mid, dataset)
    high = EMA.compute(EMA_high, dataset)

    if EMA.ABSOLUTE_UPTREND(low, mid, high) and \
        HA_current.war_formation(mark_price, klines_1min) and \
        HA_current.heikin_ashi(mark_price, klines_1min)  == "GREEN" and \
        HA_current.heikin_ashi(mark_price, klines_1HOUR) == "GREEN": return True

def GO_SHORT_EMA(mark_price, klines_1min, klines_1HOUR):
    dataset = HA_current.closing_price_list(klines_1min)
    low  = EMA.compute(EMA_low, dataset)
    mid  = EMA.compute(EMA_mid, dataset)
    high = EMA.compute(EMA_high, dataset)

    if EMA.ABSOLUTE_DOWNTREND(low, mid, high) and \
        HA_current.war_formation(mark_price, klines_1min) and \
        HA_current.heikin_ashi(mark_price, klines_1min)  == "RED" and \
        HA_current.heikin_ashi(mark_price, klines_1HOUR) == "RED": return True

def EXIT_LONG(response, mark_price, profit_threshold, klines_1min):
    if get_position.profit_or_loss(response, profit_threshold) == "PROFIT":
        if mark_price < HA_current.close(klines_1min) or HA_previous.close(klines_1min) > mark_price: return True

def EXIT_SHORT(response, mark_price, profit_threshold, klines_1min):
    if get_position.profit_or_loss(response, profit_threshold) == "PROFIT":
        if mark_price > HA_current.close(klines_1min) or HA_previous.close(klines_1min) < mark_price: return True

# Adding to the position to pull back the entry price when the PnL is below 80%
throttle_threshold = 80

def THROTTLE_LONG(i, response, mark_price, klines_6HOUR):
    if HA_current.heikin_ashi(mark_price, klines_6HOUR) == "GREEN" and \
        get_position.get_positionSize(response) < (config.quantity[i] * 9) and \
        get_position.unrealizedPnL_Percentage(i, response, mark_price) < -throttle_threshold:
        return True

def THROTTLE_SHORT(i, response, mark_price, klines_6HOUR):
    if HA_current.heikin_ashi(mark_price, klines_6HOUR) == "RED" and \
        get_position.get_positionSize(response) < (config.quantity[i] * 9) and \
        -get_position.unrealizedPnL_Percentage(i, response, mark_price) < -throttle_threshold:
        return True
