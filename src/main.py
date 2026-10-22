#Anthony, Sujiba, noufra
# 49.5%, 50%, 0.5%
#Pull request TD5


from pathlib import Path
import csv
import json

from analytics import (
    align_series,
    calculate_period_return,
    calculate_base_100,
    calculate_relative_performance,
)

DATA_DIR = Path("data/sample")

# Thes starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)
   


def load_prices():
    with open(DATA_DIR / "prices.csv",
              encoding="utf-8") as file:
        return list(csv.DictReader(file))



def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]

def get_first_close(prices):
    return float(prices[0]["close"])


def get_last_close(prices):
    return float(prices[-1]["close"])

def display_market_summary(asset, prices, show_currency=True):
    first_close = get_first_close(prices)
    last_close = get_last_close(prices)

    suffix = f" {asset['currency']}" if show_currency else ""

    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Observations : {len(prices)}")
    print(f"First close  : {first_close:.2f}{suffix}")
    print(f"Last close   : {last_close:.2f}{suffix}")


def main():
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

        # --- Comparaison instrument vs benchmark ---
    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices, benchmark_prices
    )

    instrument_ticker = aligned_instrument[0]["ticker"]
    benchmark_ticker = aligned_benchmark[0]["ticker"]

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative = calculate_relative_performance(instrument_return, benchmark_return)

    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    print()
    print("Comparison (aligned)")
    print(f"Aligned sessions        : {len(aligned_instrument)}")
    print(f"{instrument_ticker} period return      : {instrument_return:+.2f}%")
    print(f"{benchmark_ticker} period return     : {benchmark_return:+.2f}%")
    print(f"Relative performance    : {relative:+.2f} percentage points")
    print()
    print("Base 100")
    print(
        f"{instrument_ticker}   : {instrument_base_100[0]['value']:.2f}"
        f" -> {instrument_base_100[-1]['value']:.2f}"
    )
    print(
        f"{benchmark_ticker}  : {benchmark_base_100[0]['value']:.2f}"
        f" -> {benchmark_base_100[-1]['value']:.2f}"
    )

    print("=== MarketPulse ===")
    print()
    print("Market configuration")
    print(f"Period   : {LOOKBACK_LABEL}")
    print(f"Interval : {INTERVAL_LABEL}")
    print()
    print("Instrument")
    display_market_summary(instrument, instrument_prices)
    print()
    print("Benchmark")
    display_market_summary(benchmark, benchmark_prices, show_currency=False)


if __name__ == "__main__":
    main()

def get_first_date(prices):
    return prices[0]["date"]

def gest_last_date(prices):
    return prices[-1]["date"]
