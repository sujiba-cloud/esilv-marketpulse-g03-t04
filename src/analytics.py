
"""MarketPulse analytics: pure functions for comparison (TD07)."""


def index_by_date(prices):
    """Retourne un dict {date: observation} pour un accès rapide par date."""
    return {row["date"]: row for row in prices} 


def align_series(instrument_prices, benchmark_prices):
    """Garde uniquement les dates présentes dans LES DEUX séries, triées."""
    instrument_by_date = index_by_date(instrument_prices)
    benchmark_by_date = index_by_date(benchmark_prices)

    common_dates = sorted(set(instrument_by_date) & set(benchmark_by_date))

    aligned_instrument = [instrument_by_date[d] for d in common_dates]
    aligned_benchmark = [benchmark_by_date[d] for d in common_dates]

    return aligned_instrument, aligned_benchmark


def calculate_period_return(prices):
    """Rendement total en % entre la première et la dernière clôture."""
    if not prices:
        raise ValueError("Cannot compute return on an empty series")

    first_close = float(prices[0]["close"])
    last_close = float(prices[-1]["close"])

    if first_close == 0.0:
        raise ValueError("First close is zero: return is undefined")

    return ((last_close / first_close) - 1.0) * 100.0

def calculate_base_100(prices):
    """Normalise la série pour que la 1re valeur vaille 100."""
    if not prices:
        raise ValueError("Cannot compute base 100 on an empty series")

    first_close = float(prices[0]["close"])

    if first_close == 0.0:
        raise ValueError("First close is zero: base 100 is undefined")

    result = []
    for row in prices:
        value = (float(row["close"]) / first_close) * 100.0
        result.append({
            "date": row["date"],
            "ticker": row["ticker"],
            "value": value,
        })
    return result 


def calculate_relative_performance(instrument_return, benchmark_return):
    """Surperformance en points de pourcentage."""
    return instrument_return - benchmark_return 