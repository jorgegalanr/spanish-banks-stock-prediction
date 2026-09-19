"""Indicadores causales y construcción de posiciones."""

from __future__ import annotations

import numpy as np
import pandas as pd


def compute_features(prices: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Calcula factores usando exclusivamente información disponible en cada fecha."""
    returns = prices.pct_change(fill_method=None)
    momentum = prices.pct_change(63, fill_method=None)
    sma_200 = prices.rolling(200, min_periods=200).mean()
    trend = prices.div(sma_200).sub(1)
    volatility = returns.rolling(63, min_periods=63).std() * np.sqrt(252)
    rolling_peak = prices.rolling(252, min_periods=63).max()
    drawdown = prices.div(rolling_peak).sub(1)

    momentum_rank = momentum.rank(axis=1, pct=True)
    trend_rank = trend.rank(axis=1, pct=True)
    low_volatility_rank = volatility.rank(axis=1, pct=True, ascending=False)
    drawdown_rank = drawdown.rank(axis=1, pct=True)

    score = (
        0.35 * momentum_rank
        + 0.30 * trend_rank
        + 0.20 * low_volatility_rank
        + 0.15 * drawdown_rank
    )
    score = score.where(prices > sma_200)

    return {
        "returns": returns,
        "momentum_63": momentum,
        "sma_200": sma_200,
        "trend": trend,
        "volatility_63": volatility,
        "drawdown_252": drawdown,
        "score": score,
    }


def build_strategy_weights(
    prices: pd.DataFrame, top_n: int = 2
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Selecciona los mejores activos y retrasa un día la posición ejecutable."""
    if top_n < 1 or top_n > prices.shape[1]:
        raise ValueError("top_n debe estar entre 1 y el número de activos.")

    score = compute_features(prices)["score"]
    ranks = score.rank(axis=1, ascending=False, method="first")
    selected = ranks.le(top_n) & score.notna()
    counts = selected.sum(axis=1).replace(0, np.nan)
    target = selected.div(counts, axis=0).fillna(0.0)

    # La señal calculada al cierre de t solo puede aplicarse al retorno de t+1.
    executable = target.shift(1).fillna(0.0)
    return score, executable

