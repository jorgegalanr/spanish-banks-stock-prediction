# spanish-banks-stock-prediction
Evolution and prediction of Spanish banks' stock prices (2010–present). Includes data collection with Yahoo Finance, exploratory analysis, visualizations, and deep learning forecasting.

# 📈 Scoring & Recomendador de Bancos Españoles (IBEX)

> **Proyecto:** `ml_prediccion_accion` · **Tecnologías:** Python, pandas, NumPy, matplotlib, Jupyter

Un sistema reproducible de **análisis técnico**, **scoring integral** (0–10) y **recomendaciones de compra/venta** para bancos españoles (BBVA, Santander, CaixaBank, Sabadell, Bankinter, Unicaja). Incluye funciones para **formateo europeo** (punto de miles y coma decimal), ranking, cartera ejemplo y resumen de rebalanceo.

## 📝 Descripción

Este repositorio implementa un **pipeline de análisis** de precios históricos para bancos españoles, calculando factores como **rentabilidad anualizada, VaR (95%), RSI, momentum, medias móviles, volatilidad** y **drawdown**. Cada banco recibe un **score ponderado** y se generan **recomendaciones** (compra fuerte, compra, mantener, vender, venta fuerte), además de una **sugerencia de portfolio** y un módulo de **recomendaciones rápidas** pensado para el día a día.

> ⚠️ **Disclaimer:** con fines educativos. No constituye asesoramiento financiero.

---

## ✨ Características

* **Scoring integral (0–10)** con pesos configurables por factor.
* **Ranking** por score final y **TOP 3** sugerido.
* **Señales de venta** con razones (RSI, momentum, drawdown, score bajo).
* **Módulo de recomendaciones rápidas** con cartera ejemplo (100 acciones/banco) y cálculo de **pérdida potencial (VaR 95%)**.
* **Formateo europeo**: números con **punto de miles** y **coma decimal** en todos los outputs.
* Código listo para **Jupyter Notebook** y fácil de portar a script.

---

## 📊 Datos y Tickers

Por defecto se trabaja con datos de mercado histórico (por ejemplo, desde Yahoo Finance) para los siguientes tickers de las entidades analizadas:

* **BBVA** → `BBVA.MC`
* **Santander** → `SAN.MC`
* **CaixaBank** → `CABK.MC`
* **Sabadell** → `SAB.MC`
* **Bankinter** → `BKT.MC`
* **Unicaja** → `UNI.MC`

> Puedes adaptar fácilmente el rango temporal, la frecuencia o las fuentes de datos.

---

## 🧩 Arquitectura / Metodología

**Factores (y pesos por defecto):**

1. **Rentabilidad histórica (25%)** – anualizada a partir de precios.
2. **Riesgo (VaR 95%) (20%)** – percentil 5 de rentabilidades diarias.
3. **Momentum actual (15%)** – RSI(14) y momentum 20 días.
4. **Tendencia técnica (15%)** – cruce precio, SMA20 y SMA50.
5. **Volatilidad reciente (10%)** – 30 días anualizada.
6. **Drawdown actual (10%)** – descenso desde máximo reciente.
7. **Correlación/Diversificación (5%)** – penalización simple por similitud.


