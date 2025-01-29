'''The functions in this script are used to close positons. close_position_long and close_position_short will close the
position as soon as a take profit or stop loss level is reached. Since main.py is iterating through a dataframe, looking
at data at the end of each timeframe, the high and low of each datapoint is used to determine whether or not the take
profit or stop loss was reached. This is because in a live market scenario, that price level would have been reached
while the candle was forming and closed at that time, not when the candle was closed.

close_position_long_trailing and close_position_short_trailing use trailing stop logic to allow profitable positions
to remain open as the price continues to rise or fall. The take profit and stop loss levels are adjusted as the price moves.
For example, if a long position is open and the price moves upward and reaches the take profit level, a new take profit
and stop loss level will be set, allowing the position to capture more profitability.'''

import plot

def close_position_long(high, low, tp, sl, initial_price):
    if low <= sl:
        trade_long = -1
    elif high >= tp:
        trade_long = 1
    else:
        trade_long = 0
    return trade_long

def close_position_short(high, low, tp, sl, initial_price):
    if high >= sl:
        trade_short = -1
    elif low <= tp:
        trade_short = 1
    else:
        trade_short = 0
    return trade_short

def close_position_long_trailing(df, high, low, tp, sl, initial_price, count, i, look_ahead, plot_on):
    if low <= sl:
        trade_long = -1
    elif high >= tp:
        if count == 0: # The variabel count is used to keep track of how many times the position reaches a profitable level
            tp = tp * 1.005 # The first time the happens, only the take profit level is updated
        elif count == 1:
            tp = tp * 1.005
            sl = initial_price * 1.005 # When the second level is reached, the stop loss is set so that the position will close while profitalbe
        else:
            tp = tp * 1.005
            sl = tp * 0.99 # After the first two profit levels are reached, the stop loss follows the profit level by 1%, adjust this as desired
        trade_long = 0
        count += 1
        plot.plot_next_120_closes(df, 'open_position', i, look_ahead, 'Close', initial_price, tp, sl, 'MA_20', 'MA_50', 'null', plot_on)
    else:
        trade_long = 0
    return trade_long, tp, sl, count

# The logic for trailing stop on a short position is the inverse of the logic for a long position
def close_position_short_trailing(df, high, low, tp, sl, initial_price, count, i, look_ahead, plot_on):
    if high >= sl:
        trade_short = -1
    elif low <= tp:
        if count == 0:
            tp = tp / 1.005
        elif count == 1:
            tp = tp / 1.005
            sl = initial_price / 1.005
        else:
            tp = tp / 1.005
            sl = tp / 0.99
        count += 1
        trade_short = 0
        plot.plot_next_120_closes(df, 'open_position', i, look_ahead, 'Close', initial_price, tp, sl, 'MA_20', 'MA_50', 'null', plot_on)
    else:
        trade_short = 0
    return trade_short, tp, sl, count

