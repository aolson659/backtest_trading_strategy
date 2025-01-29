'''The function for plotting data will plot data in two different ways. It will plot data for opening a position and 
adjusting profit/stop levels when trailing stop logic is enabled.

It will also plot data when a position is closed, showing the price at which the position was opened and the price at which
the position was closed.'''

import matplotlib.pyplot as plt

def plot_next_120_closes(df, id, index, look_ahead, price, initial_price, tp, sl, ma_20, ma_50, close, plot_on):
    if plot_on == 0:
        return # Bypasses the function when the user does not want data plots to be shown
    plt.figure(figsize=(10, 6))
    timespan = df['Timestamp'].iloc[index - int(look_ahead*2):index+int(look_ahead*2)]
    
    plt.plot(timespan, df[price].iloc[index-int(look_ahead*2):index+int(look_ahead*2)], label='Price')

    # Define lines for both open and close positions
    initial_price_line = [initial_price] * len(timespan)
    tp_line = [tp] * len(timespan)
    sl_line = [sl] * len(timespan)

    plt.plot(timespan, initial_price_line, 'b--', label='Initial Price')

    if id == 'open_position':
        plt.plot(timespan, df[ma_20].iloc[index-int(look_ahead*2):index+int(look_ahead*2)], color='yellow', label='MA 20')
        plt.plot(timespan, df[ma_50].iloc[index-int(look_ahead*2):index+int(look_ahead*2)], color='red', label='MA 50')
        plt.plot(timespan, tp_line, 'g--', label='Take Profit')
        plt.plot(timespan, sl_line, 'r--', label='Stop Loss')
        plt.axvspan(df['Timestamp'].iloc[index-5], df['Timestamp'].iloc[index+5], color='black', alpha=0.3, label='Highlight Area')

    if id == 'close_position':
        close_line = [close] * len(timespan)
        plt.plot(timespan, df[ma_20].iloc[index-int(look_ahead*2):index+int(look_ahead*2)], color='yellow', label='MA 20')
        plt.plot(timespan, df[ma_50].iloc[index-int(look_ahead*2):index+int(look_ahead*2)], color='red', label='MA 50')
        plt.plot(timespan, close_line, 'r--', label='Close Price')

    plt.xlabel('Timestamp')
    plt.ylabel('Close')
    plt.title('Plot')
    plt.legend()
    plt.grid(True)
    plt.xlim(timespan.iloc[0], timespan.iloc[-1])
    plt.show()
