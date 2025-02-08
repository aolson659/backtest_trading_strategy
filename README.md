# backtest_trading_strategy

## Description
backtest_trading_strategy was built to test trading strategies on historical data. It does this by calculating the metrics used in the strategy, iterating through the dataframe, determining when to open long or short positions, closing the positions for a profit or loss, and keeping metrics on the overall profitability of the strategy.

# Table of Contents
- [Installation](#installation)
- [Usage](#running-the-program)
- [Features](#features)
- [Contact](#contact)

## Installation

### Prerequisites
- Python 3.8 or higher
- pandas==1.1.3
- matplotlib==3.3.2 

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/aolson659/backtest_trading_strategy.git

2. **Navigate to project directory**:
   cd backtest_trading_strategy

3. **Install required python libraries**:
   pip install -r requirements.txt

### Running the program
The program is set up to run, however you need to make sure the correct directory is called for your dataset. Within the program there are many customizable features. These exist to allow the user to develop their own strategy. The strategy present in main.py is not profitable, and if you run the program, you will see that. There is currently a 0.15% fee associated for each trade, this will depend on what exchange you plan on running your strategy on.

### Features
There are many features that can be customized throughout the program. The dataset provided is 1 minute historical BTC data. This can be aggregated into higher timeframes and this is highlighted in main.py. Other features that are customizable include:
- risk per position
- risk/reward ratio
- trailing stop vs traditional stop loss and take profit
- plotting data to visualize the strategy
- stop loss and take profit levels
- trailing stop adjustment levels

### Contact
For collaboration, troubleshooting, and potential job offers, you can reach me at aolsondm@gmail.com

