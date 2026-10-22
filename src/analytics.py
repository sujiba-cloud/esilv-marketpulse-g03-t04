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
    raise NotImplementedError 

def calculate_base_100(prices):
    raise NotImplementedError 


def calculate_relative_performance(instrument_return, benchmark_return):
    raise NotImplementedError 