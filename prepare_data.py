'''This function is used to modify the dataframe to include metrics that are used in the designated strategy. The strategy
in main.py is simple and for demonstration purposes. This is where you would calculated additional metrics when developing
your own strategy.'''

def prepare_data(df):
    df['MA_20'] = df['Close'].rolling(window=20).mean()
    df['MA_50'] = df['Close'].rolling(window=60).mean()

    df = df.dropna()

    return df