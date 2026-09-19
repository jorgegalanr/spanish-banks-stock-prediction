import pandas as pd
import pytest

from src.data import generate_sample_prices, normalize_yfinance_close, validate_prices


def test_sample_is_deterministic_and_positive():
    first = generate_sample_prices(periods=320, seed=7)
    second = generate_sample_prices(periods=320, seed=7)

    pd.testing.assert_frame_equal(first, second)
    assert (first > 0).all().all()


def test_normalizes_yfinance_multiindex():
    dates = pd.date_range("2025-01-01", periods=2)
    columns = pd.MultiIndex.from_product([["Close", "Volume"], ["AAA", "BBB"]])
    raw = pd.DataFrame(
        [[10.0, 20.0, 100.0, 200.0], [11.0, 19.0, 110.0, 190.0]],
        index=dates,
        columns=columns,
    )

    close = normalize_yfinance_close(raw, ["AAA", "BBB"])

    assert close.columns.tolist() == ["AAA", "BBB"]
    assert close.iloc[-1].tolist() == [11.0, 19.0]


def test_rejects_non_positive_prices():
    prices = generate_sample_prices(periods=320)
    prices.iloc[2, 1] = 0

    with pytest.raises(ValueError, match="positivos"):
        validate_prices(prices)

