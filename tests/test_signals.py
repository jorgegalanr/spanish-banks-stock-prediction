import pandas as pd

from src.data import generate_sample_prices
from src.signals import build_strategy_weights


def test_weights_are_long_only_and_sum_to_one_when_invested():
    prices = generate_sample_prices(periods=500)
    _, weights = build_strategy_weights(prices, top_n=2)
    invested = weights.sum(axis=1) > 0

    assert (weights >= 0).all().all()
    assert (weights.sum(axis=1)[invested] == 1).all()
    assert (weights.astype(bool).sum(axis=1) <= 2).all()


def test_future_price_changes_do_not_modify_past_weights():
    prices = generate_sample_prices(periods=520)
    cutoff = prices.index[430]
    altered = prices.copy()
    altered.loc[altered.index > cutoff, "BBVA.MC"] *= 4

    _, original_weights = build_strategy_weights(prices, top_n=2)
    _, altered_weights = build_strategy_weights(altered, top_n=2)

    pd.testing.assert_frame_equal(
        original_weights.loc[:cutoff], altered_weights.loc[:cutoff]
    )

