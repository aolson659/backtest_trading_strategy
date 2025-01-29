'''These functions are used for print statements, showing data associated with the current iteration. It also prints data
on the profitability of the strategy and the profitability of currently open positions.'''

import time

def print_data(df, i, long_profit, long_loss, short_profit, short_loss, total_pl):
    print()
    print('Timestamp:', df['Timestamp'].iloc[i])
    print('Price', df['Close'].iloc[i])
    print('MA 20', df['MA_20'].iloc[i])
    print('MA 50', df['MA_50'].iloc[i])
    print()
    width = 20
    print(f"{'long_profit:':<{width}}{long_profit:.2f}")
    print(f"{'long_loss:':<{width}}{long_loss:.2f}")
    print()
    print(f"{'short_profit:':<{width}}{short_profit:.2f}")
    print(f"{'short_loss:':<{width}}{short_loss:.2f}")
    print()
    print()
    print(f"{'total_pl:':<{width}}{total_pl:.4f}")
    print()
    print()
    if long_profit + long_loss + short_profit + short_loss > 0:
        print(f"{'Total Trades:':<{width}}{long_profit + long_loss + short_profit + short_loss:.4f}")
        print(f"{'Winrate:':<{width}}{(long_profit + short_profit) / (long_profit + long_loss + short_profit + short_loss):.2f}")
    print(f"{'Profit/Loss:':<{width}}{long_profit + short_profit - long_loss - short_loss:.4f}")

def print_long_position(initial_price_long, leverage, tp_long, sl_long, current_price):
    width = 20
    print()
    print(f"{'Long Open':<{width}}{initial_price_long:.2f}")
    print(f"{'leverage':<{width}}{leverage:.2f}")
    current_pl = 1 + ((((current_price - initial_price_long) / initial_price_long) - 0.0015) * leverage)
    print(f"{'Current P/L':<{width}}{current_pl:.4f}")
    print(f"{'Take Profit':<{width}}{tp_long:.2f}")
    print(f"{'Stop Loss':<{width}}{sl_long:.2f}")

def print_short_position(initial_price_short, leverage, tp_short, sl_short, current_price):
    width = 20
    print()
    print(f"{'Short Open':<{width}}{initial_price_short:.2f}")
    print(f"{'Leverage':<{width}}{leverage:.2f}")
    current_pl = 1 + ((((initial_price_short - current_price) / initial_price_short) - 0.0015) * leverage)
    print(f"{'Current P/L':<{width}}{current_pl:.2f}")
    print(f"{'Take Profit':<{width}}{tp_short:.2f}")
    print(f"{'Stop Loss':<{width}}{sl_short:.2f}")