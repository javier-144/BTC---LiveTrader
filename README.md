# BTC Live Trader

A Python-based live trading bot for BTC/USDT that connects to Binance WebSocket to stream live trade data. The bot simulates a basic portfolio and executes buy/sell orders based on predefined price thresholds.

## Features
- Real-time BTC/USDT price streaming using Binance WebSocket.
- Simulated portfolio management (USD balance and BTC holdings).
- Simple trading logic:
  - Buys BTC when the price drops by a defined percentage.
  - Sells BTC when the price rises by a defined percentage.
- Logs trading activity and maintains price history.

## Requirements
- Python 3.8+
- `websocket-client` library
- `pandas` library
