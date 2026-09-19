"""Ejecuta la demostración reproducible o un análisis con datos actuales."""

from __future__ import annotations

import argparse
from pathlib import Path

from src.backtest import run_backtest
from src.data import download_close_prices, load_prices
from src.reporting import save_outputs
from src.signals import build_strategy_weights


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", choices=["sample", "yahoo"], default="sample")
    parser.add_argument("--input", default="data/sample_prices.csv")
    parser.add_argument("--start", default="2017-01-01")
    parser.add_argument("--end", default=None)
    parser.add_argument("--top-n", type=int, default=2)
    parser.add_argument("--cost-bps", type=float, default=10.0)
    parser.add_argument("--test-size", type=float, default=0.30)
    parser.add_argument("--output-dir", default="reports/generated")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.source == "sample":
        prices = load_prices(args.input)
        source_label = "muestra sintética versionada"
    else:
        prices = download_close_prices(start=args.start, end=args.end)
        source_label = "Yahoo Finance"

    scores, weights = build_strategy_weights(prices, top_n=args.top_n)
    daily, metrics = run_backtest(
        prices, weights, cost_bps=args.cost_bps, test_size=args.test_size
    )
    latest_scores = scores.dropna(how="all").iloc[-1]
    save_outputs(daily, metrics, latest_scores, Path(args.output_dir))

    print(f"Fuente: {source_label}")
    print(f"Sesiones: {len(prices):,} | Test: {daily.index.min().date()} — {daily.index.max().date()}")
    print(f"Coste por rotación: {args.cost_bps:.1f} pb")
    print("\nMétricas fuera de muestra:")
    print(metrics.round(4).to_string())
    print("\nScore más reciente (heurístico, no recomendación):")
    print(latest_scores.sort_values(ascending=False).round(4).to_string())
    print(f"\nResultados guardados en {args.output_dir}/")


if __name__ == "__main__":
    main()
