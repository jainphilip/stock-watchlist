from flask import Flask, flash, redirect, render_template, request, url_for
from utils import (
    fetch_stock_data,
    load_watchlists,
    create_watchlist,
    delete_watchlist,
    add_stock_to_watchlist,
    remove_stock_from_watchlist,
)

app = Flask(__name__)
app.secret_key = "supersecretkey"


@app.route("/")
def index():
    """Home page: redirect straight to the first available watchlist."""
    watchlists = load_watchlists()
    first_group = next(iter(watchlists), None)

    if first_group is None:
        # No watchlists exist at all (edge case) — send them to create one.
        return render_template("index.html", stocks=[], watchlists={}, current_group=None)

    return redirect(url_for("view_watchlist", group=first_group))


@app.route("/watchlist/<group>", methods=["GET", "POST"])
def view_watchlist(group):
    """Show one watchlist's stocks (GET) or add a ticker to it (POST)."""
    watchlists = load_watchlists()

    if group not in watchlists:
        flash(f"Watchlist '{group}' not found.", "error")
        return redirect(url_for("index"))

    if request.method == "POST":
        ticker = request.form.get("ticker", "").upper().strip()

        if not ticker:
            flash("Please enter a ticker symbol.", "error")
        else:
            data = fetch_stock_data(ticker)
            if data:
                success, message = add_stock_to_watchlist(group, ticker)
                flash(message, "success" if success else "info")
            else:
                flash(f"Problem fetching data for symbol '{ticker}'.", "error")

        return redirect(url_for("view_watchlist", group=group))

    # GET: build the live price table for every ticker in this group only.
    stocks_data = []
    for ticker in watchlists[group]:
        data = fetch_stock_data(ticker)
        if data:
            stocks_data.append(data)

    return render_template(
        "index.html",
        stocks=stocks_data,
        watchlists=watchlists,
        current_group=group,
    )


@app.route("/create_watchlist", methods=["POST"])
def create_watchlist_route():
    """Create a new empty watchlist group from the sidebar form."""
    name = request.form.get("name", "").strip()
    success, message = create_watchlist(name)
    flash(message, "success" if success else "error")

    if success:
        return redirect(url_for("view_watchlist", group=name))
    return redirect(url_for("index"))


@app.route("/delete_watchlist/<group>")
def delete_watchlist_route(group):
    """Delete an entire watchlist group, then land on whatever remains."""
    success, message = delete_watchlist(group)
    flash(message, "success" if success else "error")

    remaining = load_watchlists()
    fallback = next(iter(remaining), None)
    if fallback:
        return redirect(url_for("view_watchlist", group=fallback))
    return redirect(url_for("index"))


@app.route("/add_stock/<group>", methods=["POST"])
def add_stock_route(group):
    """Add a ticker to a specific group (used if you post from elsewhere,
    e.g. a per-row 'add to this list' control instead of the top form)."""
    ticker = request.form.get("ticker", "").upper().strip()

    if not ticker:
        flash("Please enter a ticker symbol.", "error")
    else:
        data = fetch_stock_data(ticker)
        if data:
            success, message = add_stock_to_watchlist(group, ticker)
            flash(message, "success" if success else "info")
        else:
            flash(f"Problem fetching data for symbol '{ticker}'.", "error")

    return redirect(url_for("view_watchlist", group=group))


@app.route("/remove_stock/<group>/<ticker>")
def remove_stock_route(group, ticker):
    """Remove a ticker from one specific group."""
    success, message = remove_stock_from_watchlist(group, ticker)
    flash(message, "success" if success else "error")
    return redirect(url_for("view_watchlist", group=group))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)