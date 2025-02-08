'''This script iterates through a dataset, analyzing and making decisions on whether or not to open long or short positions.
There are several customizable features available before calling the function that allow the user to easily develop their
own strategy and see whether or not it is profitable. These features are described in detail throughout the script where
they are declared. There is a dataset provided for historical 1 minute Bitcoin data, but this is easily interchangable if
you wish to backtest other assets, whether that be stocks, other cryptocurrencies, commodoties, currencies, etc...'''


import pandas as pd
import math
import warnings
import time

import plot
import close_position
import prepare_data
import utils


warnings.filterwarnings('ignore')
pd.set_option('display.max_rows', None)
pd.set_option('display.precision', 10)

# This is the main function that iterates through the dataframe
# Input variable descriptions are commented at the bottom of the script where they are declared
def load_and_test_model(df, risk, reward, timeout, look_ahead, plot_on, delay, trailing):
    df = df.sort_values(by='Timestamp', ascending=True)
    df = df.dropna()

    # These variables help keep track of overall profitability
    open_position = False

    long_profit = 0
    long_loss = 0
    short_profit = 0
    short_loss = 0

    total_pl = 1
    buy = 0
    sell = 0
    balance = 1000
    initial_balance = balance


    for i in range(len(df)):
        # In order to plot the data, a certain amount of data has to pass, keep this in mind if developing a strategy on higher timeframes
        # Plotting a large amount of data on a higher time frame will limit the amount of data that will be analyzed
        if i < look_ahead * 4:
            continue
        # The iteration can happen quickly, in order to visibly see the trades you can add a delay by adjusting the variable at the bottom of the script
        time.sleep(delay)
        width = 60

        # Print statements showing price and trade data
        utils.print_data(df, i, long_profit, long_loss, short_profit, short_loss, total_pl)

        # Simple strategy for opening trades based on moving averages
        # If 20 period moving average crosses above 50 period moving average, open a long position
        # If 20 period moving average crosses below 50 period moving average, open a short position
        if not open_position:
            if df['MA_20'].iloc[i-1] <= df['MA_50'].iloc[i-1] and df['MA_20'].iloc[i] >= df['MA_50'].iloc[i]:
                initial_price_long = df['Close'].iloc[i]
                sl_long = initial_price_long * 0.99 # Sets a stop loss one percent below the opening price, this can be adjusted to a higher/lower threshold, recent low, etc...
                open_position = True
                buy = 1
                count = 0 # Used to manage trailing stop loss
                index = i # Used to close a position if it has been open for a certain amount of time
                # Leverage is calculated based on the accepted amount of risk per trade and the percantage difference between opening price and stop loss
                leverage = math.floor(risk / (abs(((initial_price_long - sl_long) / initial_price_long)) + 0.0015))
                if leverage < 1:
                    leverage = 1
                if leverage > 100:
                    leverage = 100
                # Take profit price is calculated based on a designated risk to reward ratio
                tp_long = initial_price_long * (1 + (((reward / (1 - (risk + 0.0015))) - 1) / leverage))
                # Plot showing where the position was opened, the take profit level and the stop loss level
                plot.plot_next_120_closes(df, 'open_position', i, look_ahead, 'Close', initial_price_long, tp_long, sl_long, 'MA_20', 'MA_50', 'null', plot_on)
                continue
            # Logic for opening a short position is the inverse of logic for opening a long position
            if df['MA_20'].iloc[i-1] >= df['MA_50'].iloc[i-1] and df['MA_20'].iloc[i] <= df['MA_50'].iloc[i]:
                initial_price_short = df['Close'].iloc[i]
                sl_short = initial_price_short / 0.99
                open_position = True
                sell = 1
                count = 0
                index = i
                leverage = math.floor(risk / (abs(((sl_short - initial_price_short) / initial_price_short)) + 0.0015))
                if leverage < 1:
                    leverage = 1
                if leverage > 100:
                    leverage = 100
                tp_short = initial_price_short / (1 + (((reward / (1 - (risk + 0.0015))) - 1) / leverage))
                plot.plot_next_120_closes(df, 'open_position', i, look_ahead, 'Close', initial_price_short, tp_short, sl_short, 'MA_20', 'MA_50', 'null', plot_on)
                continue
            
        # Once there is an open position, this segment of code will execute    
        else:
            if buy > 0:
                if trailing == 0:
                    # This function will close a position once the price reaches the take profit level or stop loss level
                    trade_long = close_position.close_position_long(df['High'].iloc[i], df['Low'].iloc[i], tp_long, sl_long)
                else:
                    # This function enables a trailing stop, allowing the position to remain open if it is profitable and adjusting the stop loss level along the way
                    trade_long, tp_long, sl_long, count = close_position.close_position_long_trailing(df, df['High'].iloc[i], df['Low'].iloc[i], tp_long, sl_long, initial_price_long, count, i, look_ahead, plot_on)
                utils.print_long_position(initial_price_long, leverage, tp_long, sl_long, df['Close'].iloc[i])
            if sell > 0:
                if trailing == 0:
                    trade_short = close_position.close_position_short(df['High'].iloc[i], df['Low'].iloc[i], tp_short, sl_short)
                else:
                    trade_short, tp_short, sl_short, count = close_position.close_position_short_trailing(df, df['High'].iloc[i], df['Low'].iloc[i], tp_short, sl_short, initial_price_short, count, i, look_ahead, plot_on)
                utils.print_short_position(initial_price_short, leverage, tp_short, sl_short, df['Close'].iloc[i])
            
            # This will close the position if it has been open for a designated amount of time, denoting timeout to 0 disables this code
            if timeout != 0:
                if i > index + timeout:
                    if buy == 1:
                        if 1 + ((df['Close'].iloc[i] - initial_price_long) / df['Close'].iloc[i]) > 1:
                            trade_long = 1
                            tp_long = df['Close'].iloc[i]
                        else:
                            trade_long = -1
                            sl_long = df['Close'].iloc[i]
                        input('lskdjflskd')
                    if sell == 1:
                        if 1 + ((initial_price_short - df['Close'].iloc[i]) / initial_price_short) > 1:
                            trade_short = 1
                            tp_short = df['Close'].iloc[i]
                        else:
                            trade_short = -1
                            sl_short = df['Close'].iloc[i]
                        input('lskdfj')
                
            '''This segment of code will close the position once the designated levels have been reached. The function for 
            closing positions returns a 1 for a profitable trade or a -1 for a loss. However in the function for a trailing
            stop loss, the position is only closed once a stop loss level is reached. If a take profit level is reached,
            the stop loss loevel is then adjusted, resulting in a profitable trade even if the stop loss level is reached. A
            -1 is always returned in this case, so there is logic present to identify whether or not a -1 is a profitable
            trade or a loss.'''  
            if buy > 0:
                if trade_long == -1:
                    pl_long = 1 + (((sl_long - initial_price_long) / initial_price_long) - 0.0015) * leverage
                    balance = balance * pl_long
                    total_pl = 1 + ((balance - initial_balance) / initial_balance)
                    if sell == 0:
                        open_position = False
                    buy = 0
                    index = i
                    trade_long = 0
                    # If trailing stop is turned on, only the stop loss level will close the position, however the stop loss level is adjusted along the way, sometimes resulting in a profitable trade
                    if pl_long > 1:
                        long_profit += 1
                    else:
                        long_loss += 1
                    plot.plot_next_120_closes(df, 'close_position', i, look_ahead, 'Close', initial_price_long, tp_long, sl_long, 'MA_20', 'MA_50', sl_long, plot_on)
                elif trade_long == 1:
                    pl_long = 1 + (((tp_long - initial_price_long) / initial_price_long) - 0.0015) * leverage
                    balance = balance * pl_long
                    total_pl = 1 + ((balance - initial_balance) / initial_balance)
                    if sell == 0:
                        open_position = False
                    buy = 0
                    long_profit += 1
                    trade_long = 0
                    plot.plot_next_120_closes(df, 'close_position', i, look_ahead, 'Close', initial_price_long, tp_long, sl_long, 'MA_20', 'MA_50', tp_long, plot_on)
            if sell > 0:
                if trade_short == -1:
                    pl_short = 1 + (((initial_price_short - sl_short) / initial_price_short) - 0.0015) * leverage
                    balance = balance * pl_short
                    total_pl = 1 + ((balance - initial_balance) / initial_balance)
                    if buy == 0:
                        open_position = False
                    sell = 0
                    trade_short == 0
                    index = i
                    pause = 1
                    signal_long = 0
                    signal_short = 0
                    if pl_short > 1:
                        short_profit += 1
                    else:
                        short_loss += 1
                    plot.plot_next_120_closes(df, 'close_position', i, look_ahead, 'Close', initial_price_short, tp_short, sl_short, 'MA_20', 'MA_50', sl_short, plot_on)
                elif trade_short == 1:
                    pl_short = 1 + (((initial_price_short - tp_short) / initial_price_short) - 0.0015) * leverage
                    balance = balance * pl_short
                    total_pl = 1 + ((balance - initial_balance) / initial_balance)
                    open_position = False
                    sell = 0
                    short_profit += 1
                    trade_short = 0
                    plot.plot_next_120_closes(df, 'close_position', i, look_ahead, 'Close', initial_price_short, tp_short, sl_short, 'MA_20', 'MA_50', tp_short, plot_on)


        


if __name__ == "__main__":
    risk = 0.01 # Amount of risk taken on per trade
    reward = 1 # Ratio used to calculate take profit levels
    # Set this based on the designated timeframe, if using the 5 minute time frame, setting this to 12 would close the position if the trade was open for 1 hour without reaching the take profit or stop loss level
    # Setting this variable to 0 disables the timeout logic, meaning the trade will remain open until the take profit or stop loss level is reached
    timeout = 0 
    look_ahead = 144 # This is used to plot data, larger numbers plot more data and smaller numbers plot less data
    plot_on = 1 # If you do not want to plot data and simply want to run a backtest, set this to 0
    delay = 0 # The iteration can run quickly, setting a delay allows you to watch the data as the loop executes, set to 0 for no delay
    trailing = 0 # Set this to 1 to enable a trailing stop for closing positions, setting to 0 means the position will close if the take profit or stop loss level is reached
    timeframe = '5m' #Availble timeframes are 1 minute, 5 minute, 15 minute, 1 hour, 4 hour, and 1 day. The dataset holds 1 minute data but this can be aggregated to any timeframe
    df = pd.read_csv('path_to_your_dataset')
    df.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'Trades']
    df = df[['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']]
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
    df.set_index('Timestamp', inplace=True)

    if timeframe == '5m':
        df = df.resample('5T').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
        })

    if timeframe == '15m':
        df = df.resample('15T').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
        })

    if timeframe == '1h':
        df = df.resample('1H').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
        })

    if timeframe == '4h':
        df = df.resample('4H').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
        })

    if timeframe == '1d':
        df = df.resample('1D').agg({
            'Open': 'first',
            'High': 'max',
            'Low': 'min',
            'Close': 'last',
            'Volume': 'sum',
        })

    df.reset_index(inplace=True)
    df = df.dropna()

    # This function calculates the necessary metrics for executing the strategy
    df = prepare_data.prepare_data(df)
    df = df.dropna()


    load_and_test_model(df, risk, reward, timeout, look_ahead, plot_on, delay, trailing)

