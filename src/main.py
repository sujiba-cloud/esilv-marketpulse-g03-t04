# Anthony, Sujiba, noufra
# Pull request TD10

from pathlib import Path
import csv
import json

from analytics import (
    align_series,
    calculate_period_return,
    calculate_base_100,
    calculate_relative_performance,
)
from providers.yahoo_provider import fetch_yahoo_prices
from providers.bloomberg_provider import fetch_bloomberg_prices, ACCESS_MODE

DATA_DIR = Path("data/sample")

# These values mirror config/settings.yml (human-readable contract).
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"
PROVIDER = "bloomberg"   # "bloomberg", "yahoo" or "csv"
LOOKBACK = "1mo"
INTERVAL = "1d"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def get_first_close(prices):
    return float(prices[0]["close"])


def get_last_close(prices):
    return float(prices[-1]["close"])


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]


def display_market_summary(asset, prices, show_currency=True):
    suffix = f" {asset['currency']}" if show_currency else ""

    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Observations : {len(prices)}")
    print(f"First close  : {get_first_close(prices):.2f}{suffix}")
    print(f"Last close   : {get_last_close(prices):.2f}{suffix}")


def get_provider_label():
    if PROVIDER == "bloomberg":
        return "Bloomberg stage", ACCESS_MODE
    if PROVIDER == "yahoo":
        return "Yahoo Finance", "REMOTE"
    return "CSV", "LOCAL"


def build_market_snapshot():
    """Shared application result used by the terminal (and later by Dash)."""
    instruments = load_instruments()
    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    if PROVIDER == "bloomberg":
        instrument_prices = fetch_bloomberg_prices(instrument["ticker"])
        benchmark_prices = fetch_bloomberg_prices(benchmark["ticker"])
    elif PROVIDER == "yahoo":
        instrument_prices = fetch_yahoo_prices(instrument["ticker"], LOOKBACK, INTERVAL)
        benchmark_prices = fetch_yahoo_prices(benchmark["ticker"], LOOKBACK, INTERVAL)
    else:
        prices = load_prices()
        instrument_prices = filter_prices(prices, instrument["ticker"])
        benchmark_prices = filter_prices(prices, benchmark["ticker"])

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices, benchmark_prices
    )

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative = calculate_relative_performance(instrument_return, benchmark_return)

    provider_label, access_mode = get_provider_label()

    return {
        "provider": provider_label,
        "access_mode": access_mode,
        "lookback": LOOKBACK,
        "interval": INTERVAL,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_prices": instrument_prices,
        "benchmark_prices": benchmark_prices,
        "aligned_sessions": len(aligned_instrument),
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": relative,
        "instrument_base_100": calculate_base_100(aligned_instrument),
        "benchmark_base_100": calculate_base_100(aligned_benchmark),
    }


def main():
    snapshot = build_market_snapshot()

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    inst_ticker = instrument["ticker"]
    bench_ticker = benchmark["ticker"]
    inst_base = snapshot["instrument_base_100"]
    bench_base = snapshot["benchmark_base_100"]

    print("=== MarketPulse ===")
    print()
    print("Provider")
    print(snapshot["provider"])
    print()
    print("Access mode")
    print(snapshot["access_mode"])
    print()
    print("Market configuration")
    print(f"Period   : {LOOKBACK_LABEL}")
    print(f"Interval : {INTERVAL_LABEL}")
    print()
    print("Instrument")
    display_market_summary(instrument, snapshot["instrument_prices"])
    print()
    print("Benchmark")
    display_market_summary(benchmark, snapshot["benchmark_prices"], show_currency=False)
    print()
    print("Comparison (aligned)")
    print(f"Aligned sessions        : {snapshot['aligned_sessions']}")
    print(f"{inst_ticker} period return      : {snapshot['instrument_return']:+.2f}%")
    print(f"{bench_ticker} period return     : {snapshot['benchmark_return']:+.2f}%")
    print(f"Relative performance    : {snapshot['relative_performance']:+.2f} percentage points")
    print()
    print("Base 100")
    print(f"{inst_ticker}   : {inst_base[0]['value']:.2f} -> {inst_base[-1]['value']:.2f}")
    print(f"{bench_ticker}  : {bench_base[0]['value']:.2f} -> {bench_base[-1]['value']:.2f}")


if __name__ == "__main__":
    main()