## Strategy Description
You can copy any of these strategies and replace the `strategy.py` in the parent folder.

## strategy_hybrid.py
The code use both Heikin Ashi and Normal Candlestick to determine the strength.  
The timeframe is 4HR (main), 1Hr (confirmation), 5min (entry confirmation) and 1min (entry)

## stretegy_heikin_ashi.py
The code use only Heikin Ashi to determine the strength of the trend.  
The timeframe is 4HR (main), 1Hr (confirmation), 5min (entry confirmation) and 1min (entry)

## strategy_one_hour.py
The code use 4HR as main direction and entry on 1HR.
This strategy performance is very poor and this is the request by #Mou1171 to implement this strategy

## weekdays_heikin_ashi.py
Same with `strategy_heikin_ashi.py` but only trades on weekdays.

## weekdays_hybrid.py
Same with `strategy_hybrid.py` but only trades on weekdays.
