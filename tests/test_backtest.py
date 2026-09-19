from src.backtest import run_backtest
from src.data import generate_sample_prices
from src.signals import build_strategy_weights


def test_transaction_costs_cannot_improve_strategy_return():
    prices = generate_sample_prices(periods=600)
    _, weights = build_strategy_weights(prices)

    without_costs, _ = run_backtest(prices, weights, cost_bps=0)
    with_costs, metrics = run_backtest(prices, weights, cost_bps=15)

    assert with_costs["strategy"].sum() <= without_costs["strategy"].sum()
    assert set(metrics.index) == {"strategy", "benchmark_equal_weight"}
    assert "max_drawdown" in metrics.columns


def test_backtest_only_reports_final_temporal_segment():
    prices = generate_sample_prices(periods=600)
    _, weights = build_strategy_weights(prices)
    daily, _ = run_backtest(prices, weights, test_size=0.25)

    assert daily.index.min() == prices.index[450]
    assert len(daily) == 150

