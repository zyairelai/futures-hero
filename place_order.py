import config, get_position, HA_current, HA_previous

def GO_LONG(mark_price, klines_1min, klines_5min, klines_1HOUR):
        if HA_current.war_formation(mark_price, klines_1min) and \
            HA_current.heikin_ashi(mark_price, klines_1min) == "GREEN" and \
            HA_current.heikin_ashi(mark_price, klines_5min)  == "GREEN" and \
            HA_current.heikin_ashi(mark_price, klines_1HOUR) == "GREEN" : return True

def GO_SHORT(mark_price, klines_1min, klines_5min, klines_1HOUR):
        if HA_current.war_formation(mark_price, klines_1min) and \
            HA_current.heikin_ashi(mark_price, klines_1min) == "RED" and \
            HA_current.heikin_ashi(mark_price, klines_5min)  == "RED" and \
            HA_current.heikin_ashi(mark_price, klines_1HOUR) == "RED" : return True

def GO_LONG_FOCUS(mark_price, klines_1min, klines_1HOUR):
        if HA_current.war_formation(mark_price, klines_1min) and \
            HA_current.heikin_ashi(mark_price, klines_1min) == "GREEN" and \
            HA_current.heikin_ashi(mark_price, klines_1HOUR) == "GREEN": return True

def GO_SHORT_FOCUS(mark_price, klines_1min, klines_1HOUR):
        if HA_current.war_formation(mark_price, klines_1min) and \
            HA_current.heikin_ashi(mark_price, klines_1min) == "RED" and \
            HA_current.heikin_ashi(mark_price, klines_1HOUR) == "RED": return True

def EXIT_LONG(response, mark_price, profit, klines_1min):
    if get_position.profit_or_loss(response, profit) == "PROFIT":
        if HA_previous.close(klines_1min) > mark_price: return True

def EXIT_SHORT(response, mark_price, profit, klines_1min):
    if get_position.profit_or_loss(response, profit) == "PROFIT":
        if HA_previous.close(klines_1min) < mark_price: return True

# Adding to the position to pull back the entry price when the maintenance margin is below 70%
throttle_threshold = -0.7

def THROTTLE_LONG(i, response, mark_price, klines_6HOUR):
    if HA_current.heikin_ashi(mark_price, klines_6HOUR) != "RED" and \
        get_position.get_positionSize(response) < (config.quantity[i] * 9) and \
        get_position.get_unrealizedProfit(response) < get_position.get_margin(response) * throttle_threshold:
        return True

def THROTTLE_SHORT(i, response, mark_price, klines_6HOUR):
    if HA_current.heikin_ashi(mark_price, klines_6HOUR) != "GREEN" and \
        get_position.get_positionSize(response) < (config.quantity[i] * 9) and \
        get_position.get_unrealizedProfit(response) < get_position.get_margin(response) * throttle_threshold:
        return True
