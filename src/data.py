"""Carga y validación de precios de cierre."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping

import numpy as np
import pandas as pd


SPANISH_BANKS: dict[str, str] = {
    "BBVA.MC": "BBVA",
    "SAN.MC": "Santander",
    "CABK.MC": "CaixaBank",
    "SAB.MC": "Sabadell",
    "BKT.MC": "Bankinter",
    "UNI.MC": "Unicaja",
}


def validate_prices(prices: pd.DataFrame) -> pd.DataFrame:
    """Devuelve precios ordenados y comprueba invariantes básicas."""
    if prices.empty:
        raise ValueError("No hay precios disponibles.")
    if prices.index.has_duplicates:
        raise ValueError("El índice contiene fechas duplicadas.")

    clean = prices.copy()
    clean.index = pd.to_datetime(clean.index, utc=True).tz_localize(None)
    clean = clean.sort_index().apply(pd.to_numeric, errors="coerce")
    clean = clean.dropna(how="all")

    if (clean <= 0).any().any():
        raise ValueError("Los precios deben ser positivos.")
    if clean.shape[1] < 2:
        raise ValueError("Se necesitan al menos dos activos para la comparación.")
    return clean


def normalize_yfinance_close(
    downloaded: pd.DataFrame, tickers: list[str]
) -> pd.DataFrame:
    """Normaliza las variantes de columnas devueltas por ``yfinance``."""
    if downloaded.empty:
        raise ValueError("Yahoo Finance no devolvió datos.")

    if isinstance(downloaded.columns, pd.MultiIndex):
        level_0 = downloaded.columns.get_level_values(0)
        level_1 = downloaded.columns.get_level_values(1)
        if "Close" in level_0:
            close = downloaded["Close"]
        elif "Close" in level_1:
            close = downloaded.xs("Close", axis=1, level=1)
        else:
            raise ValueError("La descarga no contiene precios de cierre.")
    else:
        if "Close" not in downloaded.columns or len(tickers) != 1:
            raise ValueError("Formato de descarga de Yahoo Finance no reconocido.")
        close = downloaded[["Close"]].rename(columns={"Close": tickers[0]})

    return validate_prices(close.reindex(columns=tickers))


def download_close_prices(
    start: str = "2017-01-01",
    end: str | None = None,
    banks: Mapping[str, str] = SPANISH_BANKS,
) -> pd.DataFrame:
    """Descarga precios ajustados; requiere conexión a Internet."""
    import yfinance as yf

    tickers = list(banks)
    raw = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
        group_by="column",
    )
    return normalize_yfinance_close(raw, tickers)


def load_prices(path: str | Path) -> pd.DataFrame:
    """Carga un CSV ancho cuya primera columna contiene la fecha."""
    prices = pd.read_csv(path, index_col=0, parse_dates=True)
    return validate_prices(prices)


def generate_sample_prices(periods: int = 1_000, seed: int = 42) -> pd.DataFrame:
    """Genera una muestra sintética y determinista para la demo sin Internet."""
    if periods < 300:
        raise ValueError("La muestra necesita al menos 300 sesiones.")

    rng = np.random.default_rng(seed)
    tickers = list(SPANISH_BANKS)
    dates = pd.bdate_range("2021-01-04", periods=periods)
    market = rng.normal(0.00025, 0.011, size=periods)
    sensitivities = np.array([1.05, 0.95, 0.85, 1.15, 0.75, 1.10])
    drifts = np.array([0.00015, 0.00008, 0.00012, -0.00002, 0.00018, 0.00003])
    idiosyncratic = rng.normal(0, 0.008, size=(periods, len(tickers)))
    returns = market[:, None] * sensitivities + idiosyncratic + drifts

    prices = 10 * np.exp(np.cumsum(returns, axis=0))
    return pd.DataFrame(prices, index=dates, columns=tickers).rename_axis("Date")

