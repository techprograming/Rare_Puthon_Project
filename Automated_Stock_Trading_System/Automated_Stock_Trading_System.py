import yfinance as yf
import pandas as pd
from alpaca_trade_api import REST
import time

# Alpaca API credentials
API_KEY = 'YOUR_ALPACA_API_KEY'
SECRET_KEY = 'YOUR_ALPACA_SECRET_KEY'
BASE_URL = 'https://paper-api.alpaca.markets'

# Initialize Alpaca API
api = REST(API_KEY, SECRET_KEY, BASE_URL)

# Trading parameters
SYMBOL = 'AAPL'
SHORT_WINDOW = 20
LONG_WINDOW = 50
TRADE_QUANTITY = 1
REFRESH_INTERVAL = 60  # seconds

# Function to fetch historical stock data
def fetch_data(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="3mo")
    return hist

# Function to calculate moving averages and trading signals
def calculate_signals(data):
    data['Short_MA'] = data['Close'].rolling(window=SHORT_WINDOW).mean()
    data['Long_MA'] = data['Close'].rolling(window=LONG_WINDOW).mean()
    data['Signal'] = (data['Short_MA'] > data['Long_MA']).astype(int)
    return data

# Function to check the account and positions
def check_positions(symbol):
    try:
        positions = api.get_position(symbol)
        return int(positions.qty)
    except Exception:
        return 0

# Function to place an order
def place_order(symbol, qty, side):
    try:
        api.submit_order(
            symbol=symbol,
            qty=qty,
            side=side,
            type='market',
            time_in_force='gtc'
        )
        print(f"Order placed: {side} {qty} {symbol}")
    except Exception as e:
        print(f"Error placing order: {e}")

# Main trading logic
def trading_bot():
    print("Starting trading bot...")
    while True:
        print("\nFetching data...")
        data = fetch_data(SYMBOL)
        data = calculate_signals(data)

        # Get the latest signal
        if len(data) > LONG_WINDOW:
            latest_signal = data['Signal'].iloc[-1]
            current_position = check_positions(SYMBOL)
            print(f"Latest Signal: {latest_signal}, Current Position: {current_position}")

            # Buy signal
            if latest_signal == 1 and current_position == 0:
                place_order(SYMBOL, TRADE_QUANTITY, 'buy')

            # Sell signal
            elif latest_signal == 0 and current_position > 0:
                place_order(SYMBOL, TRADE_QUANTITY, 'sell')

        else:
            print("Not enough data to generate signals.")

        print(f"Waiting for {REFRESH_INTERVAL} seconds...")
        time.sleep(REFRESH_INTERVAL)

# Run the bot
if __name__ == "__main__":
    trading_bot()
