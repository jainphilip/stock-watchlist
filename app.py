from flask import Flask, render_template, request, redirect, url_for, flash
from utils import load_watchlist, save_watchlist, fetch_stock_data

# Create the Flask application
app = Flask(__name__)
app.secret_key = "ABRACADABRA"


@app.route("/", methods=["GET", "POST"])
def index():
    # Load saved ticker symbols
    tickers = load_watchlist()

    # Handle form submission
    if request.method == "POST":
        ticker = request.form.get("ticker").upper().strip()

        if not ticker:
            flash("Please enter a ticker symbol", "error")
        else:
            data = fetch_stock_data(ticker)

            if data and ticker not in tickers:
                tickers.append(ticker)
                save_watchlist(tickers)
                flash(f"{ticker} added!", "success")

            elif ticker in tickers:
                flash("Ticker already in list", "info")

            else:
                flash("Problem with this ticker symbol", "error")

        return redirect(url_for("index"))

    # Fetch stock data for all saved tickers
    stocks_data = []

    for ticker in tickers:
        data = fetch_stock_data(ticker)
        if data:
            stocks_data.append(data)

    return render_template("index.html", stocks=stocks_data)


@app.route("/remove/<ticker>")
def remove_ticker(ticker):
    tickers = load_watchlist()

    if ticker in tickers:
        tickers.remove(ticker)
        save_watchlist(tickers)
        flash(f"{ticker} removed", "success")

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)