"""Persistencia de resultados y visualizaciones."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def save_outputs(
    daily: pd.DataFrame,
    metrics: pd.DataFrame,
    latest_scores: pd.Series,
    output_dir: str | Path,
) -> None:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    daily.to_csv(output / "backtest_daily.csv", index_label="Date")
    metrics.to_csv(output / "backtest_metrics.csv")
    latest_scores.rename("score").sort_values(ascending=False).to_csv(
        output / "latest_scores.csv", index_label="ticker"
    )

    fig, ax = plt.subplots(figsize=(10, 5.5))
    daily[["strategy_equity", "benchmark_equity"]].rename(
        columns={
            "strategy_equity": "Estrategia técnica",
            "benchmark_equity": "Equiponderada",
        }
    ).plot(ax=ax, linewidth=2)
    ax.set_title("Backtest fuera de muestra — crecimiento de 1 €")
    ax.set_xlabel("Fecha")
    ax.set_ylabel("Capital acumulado")
    ax.grid(alpha=0.25)
    fig.tight_layout()
    fig.savefig(output / "equity_curve.png", dpi=160)
    plt.close(fig)

