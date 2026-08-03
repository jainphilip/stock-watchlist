import json
import yfinance as yf

WATCHLIST_FILE = "watchlist.json"


def save_watchlist(tickers):
    """Save the watchlist to a JSON file."""
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(tickers, f)


def load_watchlist():
    """Load the watchlist from the JSON file."""
    try:
        with open(WATCHLIST_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def fetch_stock_data(ticker_symbol):
    """Fetch stock information from Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker_symbol)

        #Currency Symbol
        currency = stock.info.get("currency", "USD")

        if currency == "INR":
            symbol = "₹"
        elif currency == "USD":
            symbol = "$"
        else:
            symbol = currency + " "

        data = stock.history(period="1d")

        if not data.empty:
            # Get the latest row of stock data
            row = data.iloc[-1]

            # Current closing price
            price = row["Close"]

            # Previous day's closing price
            prev_close = stock.info.get("previousClose", price)

            # Calculate price change
            change = price - prev_close

            # Calculate percentage change
            change_pct = (
                (change / prev_close) * 100
                if prev_close != 0
                else 0
            )

            return {
                "ticker": ticker_symbol,
                "currency_symbol": symbol,
                "price": f"{symbol}{price:.2f}",
                "datetime": row.name.strftime("%Y-%m-%d %H:%M:%S"),
                "change": change,
                "change_percentage": change_pct,
                "high": f"{symbol}{row['High']:.2f}",
                "low": f"{symbol}{row['Low']:.2f}",
                "volume": f"{int(row['Volume']):,}",
            }

    except Exception:
        return None

    return None