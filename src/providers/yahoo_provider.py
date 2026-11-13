"""Yahoo Finance provider for MarketPulse.

Pure adapter: fetches raw data through yfinance and converts it into the
canonical observation rows (same shape as prices.csv). It never prints.
"""

import yfinance as yf

# canonical MarketPulse ticker -> Yahoo Finance symbol
# Adding a new instrument is a one-line change.
CANONICAL_TO_YAHOO = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}


def fetch_yahoo_prices(canonical_ticker, lookback="1mo", interval="1d"):
    """Return canonical observation rows for one instrument, sorted by date."""
    if canonical_ticker not in CANONICAL_TO_YAHOO:
        raise ValueError(
            f"Unknown canonical ticker '{canonical_ticker}'. "
            f"Known: {sorted(CANONICAL_TO_YAHOO)}"
        )

    yahoo_symbol = CANONICAL_TO_YAHOO[canonical_ticker]

    raw = yf.Ticker(yahoo_symbol).history(period=lookback, interval=interval)

    if raw is None or raw.empty:
        raise RuntimeError(
            f"Yahoo returned no data for {yahoo_symbol} "
            f"(period={lookback}, interval={interval})"
        )

    raw = raw.dropna(subset=["Open", "High", "Low", "Close"])

    rows = []
    for timestamp, record in raw.iterrows():
        volume = record["Volume"]
        rows.append(
            {
                "date": timestamp.strftime("%Y-%m-%d"),
                "ticker": canonical_ticker,  # canonical, never ^GSPC
                "open": float(record["Open"]),
                "high": float(record["High"]),
                "low": float(record["Low"]),
                "close": float(record["Close"]),
                "volume": int(volume) if volume == volume else 0,
            }
        )

    rows.sort(key=lambda row: row["date"])
    return rows