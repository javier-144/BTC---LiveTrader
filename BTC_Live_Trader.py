import websocket
import ssl
import json
import pandas as pd
from datetime import datetime

# Replace these values with your trading parameters
SYMBOL = "BTC/USDT"
INITIAL_BALANCE = 1000  # Example starting balance in USD
TRADE_AMOUNT = 0.001  # Amount of BTC to trade per transaction
data_list = []
threshold = 0.001  # Example threshold for price change

# Simulated portfolio
portfolio = {
    "balance": INITIAL_BALANCE,  # USD balance
    "btc": 0.0  # BTC holdings
}

def place_order(side, amount, price):
    global portfolio

    if side == "buy":
        cost = amount * price
        if portfolio["balance"] >= cost:
            portfolio["balance"] -= cost
            portfolio["btc"] += amount
            print(f"BUY {amount} BTC at {price:.2f} USD. New balance: {portfolio['balance']:.2f} USD, BTC: {portfolio['btc']:.6f}")
        else:
            print("Insufficient USD balance to buy.")

    elif side == "sell":
        if portfolio["btc"] >= amount:
            portfolio["btc"] -= amount
            revenue = amount * price
            portfolio["balance"] += revenue
            print(f"SELL {amount} BTC at {price:.2f} USD. New balance: {portfolio['balance']:.2f} USD, BTC: {portfolio['btc']:.6f}")
        else:
            print("Insufficient BTC holdings to sell.")

def evaluate_trading_logic(latest_price):
    """ Basic logic for demo purposes: buy if price drops, sell if it rises. """
    if len(data_list) < 2:
        return  # Not enough data to evaluate

    last_two_prices = [entry['price'] for entry in data_list[-2:]]
    change = (last_two_prices[1] - last_two_prices[0]) / last_two_prices[0]

    print(f"Price change: {change:.6f}")

    if change <= -threshold:
        # Buy logic
        place_order('buy', amount=TRADE_AMOUNT, price=latest_price)
    elif change >= threshold:
        # Sell logic
        place_order('sell', amount=TRADE_AMOUNT, price=latest_price)

def on_message(ws, message):
    print("Raw message received:", message)  # Debugging raw message
    try:
        message_data = json.loads(message)

        if message_data.get("e") == "aggTrade":
            timestamp = datetime.fromtimestamp(message_data["T"] / 1000)  # Convert to datetime
            price = float(message_data["p"])  # Trade price

            data_list.append({"timestamp": timestamp, "price": price})
            if len(data_list) > 100:
                data_list.pop(0)  # Keep memory usage low

            evaluate_trading_logic(price)

            df = pd.DataFrame(data_list)
            print(df.tail())  # Print the last few rows
        else:
            print("Non-trade message:", message_data)
    except Exception as e:
        print("Error processing message:", e)

def on_error(ws, error):
    print("WebSocket error occurred:", error)

def on_close(ws, close_status_code, close_msg):
    print("WebSocket connection closed. Status code:", close_status_code, "Message:", close_msg)

def on_open(ws):
    print("WebSocket connection opened.")
    subscribe_message = json.dumps({
        "method": "SUBSCRIBE",
        "params": [
            "btcusdt@aggTrade",
        ],
        "id": 1
    })
    ws.send(subscribe_message)
    print("Subscription message sent:", subscribe_message)

if __name__ == "__main__":
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(
        "wss://stream.binance.com:9443/ws",  # Use Global Binance for more liquidity
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})
  

