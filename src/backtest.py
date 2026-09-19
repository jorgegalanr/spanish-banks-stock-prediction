"""Motor de backtesting y métricas de riesgo/rentabilidad."""

from __future__ import annotations

import numpy as np
import pandas as pd


def performance_metrics(returns: pd.Series) -> dict[str, float]:
    """Calcula métricas anualizadas sobre una serie de rentabilidades netas."""
    clean = returns.dropna()
    if clean.empty:
        raise ValueError("No hay rentabilidades para evaluar.")

    equity = (1 + clean).cumprod()
    total_return = float(equity.iloc[-1] - 1)
    years = len(clean) / 252
    cagr = float(equity.iloc[-1] ** (1 / years) - 1) if years > 0 else np.nan
    volatility = float(clean.std(ddof=1) * np.sqrt(252))
    sharpe = (
        float(clean.mean() / clean.std(ddof=1) * np.sqrt(252))
        if clean.std(ddof=1) > 0
        else np.nan
    )
    drawdown = equity.div(equity.cummax()).sub(1)

    return {
        "total_return": total_return,
        "cagr": cagr,
        "annual_volatility": volatility,
        "sharpe_0rf": sharpe,
        "max_drawdown": float(drawdown.min()),
    }


def run_backtest(
    prices: pd.DataFrame,
    weights: pd.DataFrame,
    cost_bps: float = 10.0,
    test_size: float = 0.30,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Compara la estrategia con una cartera equiponderada en el tramo final."""
    if not 0 < test_size < 1:
        raise ValueError("test_size debe estar entre 0 y 1.")
    if cost_bps < 0:
        raise ValueError("Los costes no pueden ser negativos.")

    asset_returns = prices.pct_change(fill_method=None)
    aligned_weights = weights.reindex_like(prices).fillna(0.0)
    gross = (aligned_weights * asset_returns).sum(axis=1)
    turnover = aligned_weights.diff().abs().sum(axis=1).fillna(0.0)
    costs = turnover * cost_bps / 10_000
    strategy = gross - costs
    split = max(int(len(prices) * (1 - test_size)), 1)
    test_start = prices.index[split]

    # Baseline pasivo: invertir el mismo capital en cada activo al cierre previo
    # al test y mantener las participaciones, sin rebalanceos posteriores.
    base_prices = prices.iloc[split - 1]
    benchmark_equity = prices.loc[test_start:].div(base_prices).mean(axis=1)
    benchmark = benchmark_equity.pct_change(fill_method=None)
    benchmark.iloc[0] = benchmark_equity.iloc[0] - 1

    daily = pd.DataFrame(
        {
            "strategy": strategy,
            "benchmark_equal_weight": benchmark,
            "turnover": turnover,
            "cost": costs,
        }
    ).loc[test_start:]
    daily = daily.dropna(subset=["strategy", "benchmark_equal_weight"])
    daily["strategy_equity"] = (1 + daily["strategy"]).cumprod()
    daily["benchmark_equity"] = (1 + daily["benchmark_equal_weight"]).cumprod()

    metrics = pd.DataFrame(
        {
            "strategy": performance_metrics(daily["strategy"]),
            "benchmark_equal_weight": performance_metrics(
                daily["benchmark_equal_weight"]
            ),
        }
    ).T
    metrics["average_daily_turnover"] = [float(daily["turnover"].mean()), 0.0]
    metrics.index.name = "portfolio"
    return daily, metrics
