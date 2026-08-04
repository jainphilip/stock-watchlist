import json
import yfinance as yf

WATCHLIST_FILE = "watchlist.json"

# Used only the very first time the app runs and no file exists yet.
DEFAULT_WATCHLISTS = {
    "Default": ["AAPL", "NVDA", "GOOGL", "MSFT", "AMZN", "TSLA", "AMD", "INTC", "JPM"]
}

# ---------------------------------------------------------------------------
# Core read / write
# ---------------------------------------------------------------------------

def save_watchlists(watchlists):
    """Persists the full watchlists dict back to JSON."""
    with open(WATCHLIST_FILE, "w") as f:
        json.dump(watchlists, f, indent=2)


def load_watchlists():
    """Loads the full watchlists dict: {group_name: [tickers]}.

    Falls back to DEFAULT_WATCHLISTS if the file doesn't exist yet, or is
    corrupt/empty, so the app never crashes on first run.
    """
    try:
        with open(WATCHLIST_FILE, "r") as f:
            data = json.load(f)
            # Guard against an old-style flat list from before this change.
            if isinstance(data, list):
                return {"Default": data}
            return data
        
    except (FileNotFoundError, json.JSONDecodeError):
        return DEFAULT_WATCHLISTS.copy()


# ---------------------------------------------------------------------------
# Group (watchlist) management
# ---------------------------------------------------------------------------

def create_watchlist(name):
    """Creates a new, empty watchlist group. Returns (success, message)."""
    watchlists = load_watchlists()

    if not name:
        return False, "Watchlist name cannot be empty."
    if name in watchlists:
        return False, f"Watchlist '{name}' already exists."

    watchlists[name] = []
    save_watchlists(watchlists)
    return True, f"Watchlist '{name}' created."


def delete_watchlist(name):
    """Deletes an entire watchlist group. Returns (success, message)."""
    watchlists = load_watchlists()

    if name not in watchlists:
        return False, f"Watchlist '{name}' not found."
    if len(watchlists) == 1:
        return False, "You can't delete your only remaining watchlist."

    del watchlists[name]
    save_watchlists(watchlists)
    return True, f"Watchlist '{name}' deleted."

# ---------------------------------------------------------------------------
# Stock (ticker) management within a group
# ---------------------------------------------------------------------------

def add_stock_to_watchlist(group, ticker):
    """Adds a ticker to a specific group. Returns (success, message)."""
    watchlists = load_watchlists()

    if group not in watchlists:
        return False, f"Watchlist '{group}' not found."
    if ticker in watchlists[group]:
        return False, f"{ticker} is already in '{group}'."

    watchlists[group].append(ticker)
    save_watchlists(watchlists)
    return True, f"{ticker} added to '{group}'."


def remove_stock_from_watchlist(group, ticker):
    """Removes a ticker from a specific group. Returns (success, message)."""
    watchlists = load_watchlists()

    if group in watchlists and ticker in watchlists[group]:
        watchlists[group].remove(ticker)
        save_watchlists(watchlists)
        return True, f"{ticker} removed from '{group}'."

    return False, f"{ticker} was not found in '{group}'."


# ---------------------------------------------------------------------------
# Market data
# ---------------------------------------------------------------------------

def fetch_stock_data(ticker):
    """Fetch stock information from Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d")

        #Currency Symbol
        currency = stock.info.get("currency", "USD")

        if currency == "INR":
            symbol = "₹"
        elif currency == "USD":
            symbol = "$"
        elif currency == "EUR":
            symbol = "€"
        elif currency == "GBP":
            symbol = "£"
        elif currency == "JPY":
            symbol = "¥"
        elif currency == "CNY":
            symbol = "¥"
        else:
            symbol = currency + " "


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

            # Format for display
            change_str = f"{change:.2f}"
            change_whole, change_decimal = change_str.split(".")

            change_pct_str = f"{change_pct:.2f}"
            pct_whole, pct_decimal = change_pct_str.split(".")

            return {
                "ticker": ticker,
                "currency_symbol": symbol,
                "price": f"{symbol}{price:.2f}",
                "datetime": row.name.strftime("%Y-%m-%d %H:%M:%S"),
                "change": change,
                "change_percentage": change_pct,

                "change_whole": change_whole,
                "change_decimal": change_decimal,

                "pct_whole": pct_whole,
                "pct_decimal": pct_decimal,

                "high": f"{symbol}{row['High']:.2f}",
                "low": f"{symbol}{row['Low']:.2f}",
                "volume": f"{int(row['Volume']):,}",
            }

    except Exception:
        return None

    return None