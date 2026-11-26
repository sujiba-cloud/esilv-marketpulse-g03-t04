"""Bloomberg-stage provider (APPROVED_SAMPLE, not live Bloomberg).

Wrapper keys such as observation_date are teaching keys,
not Bloomberg field mnemonics.
Pure adapter: it never prints.
"""

import json
from pathlib import Path

ACCESS_MODE = "APPROVED_SAMPLE"

SAMPLE_PATH = (
    Path(__file__).resolve().parents[2]
    / "data"
    / "sample"
    / "bloomberg_reference_sample.json"
)

# canonical MarketPulse ticker -> Bloomberg identifier
BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}


def fetch_raw_bloomberg_history(identifier):
    """Raw input boundary (APPROVED_SAMPLE): read the fallback fixture."""
    with open(SAMPLE_PATH, encoding="utf-8") as file:
        sample = json.load(file)

    for series in sample["series"]:
        if series["provider_identifier"] == identifier:
            return series

    raise ValueError(f"Unsupported Bloomberg identifier: {identifier}")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    """Transform a raw series into canonical rows."""
    rows = []
    for observation in raw_data["observations"]:
        rows.append(
            {
                "date": observation["observation_date"],
                "ticker": canonical_ticker,  # canonical, never "SPX Index"
                "open": float(observation["open_value"]),
                "high": float(observation["high_value"]),
                "low": float(observation["low_value"]),
                "close": float(observation["close_value"]),
                "volume": int(observation["volume_value"]),
            }
        )

    rows.sort(key=lambda row: row["date"])
    return rows


def fetch_bloomberg_prices(canonical_ticker):
    """Return canonical observation rows for one instrument, sorted by date."""
    if canonical_ticker not in BLOOMBERG_IDENTIFIERS:
        raise ValueError(
            f"Unknown canonical ticker '{canonical_ticker}'. "
            f"Known: {sorted(BLOOMBERG_IDENTIFIERS)}"
        )

    identifier = BLOOMBERG_IDENTIFIERS[canonical_ticker]
    raw_data = fetch_raw_bloomberg_history(identifier)
    rows = normalize_bloomberg_history(raw_data, canonical_ticker)

    if not rows:
        raise RuntimeError(f"No Bloomberg-stage rows for {identifier}")

    return rows