# 📈 Spanish Banks Stock Analysis & Prediction

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.0-green.svg)](https://pandas.pydata.org/)
[![yfinance](https://img.shields.io/badge/yfinance-Finance-orange.svg)](https://pypi.org/project/yfinance/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-Viz-purple.svg)](https://matplotlib.org/)

**Análisis técnico completo + scoring (0-10) + recomendaciones de inversión** para bancos españoles del IBEX (BBVA, Santander, CaixaBank, Sabadell, Bankinter, Unicaja). Datos reales desde 2010 vía **Yahoo Finance**.

## 🎯 Objetivos del Proyecto

- Recopilar datos históricos de **6 bancos españoles** (2010–presente)
- Calcular **7 factores técnicos** (rentabilidad, VaR, RSI, momentum, volatilidad...)
- Generar **scoring integral ponderado** (0-10) por banco
- Proporcionar **recomendaciones accionables** (compra/venta/mantener)
- Crear **portfolio óptimo** basado en scores y diversificación
- **Formateo europeo** (punto miles, coma decimal) para reporting

## 📊 Datos y Cobertura

**Bancos analizados:** BBVA.MC, SAN.MC, CABK.MC, SAB.MC, BKT.MC, UNI.MC
- **Período:** 2010–2026 (~3,800 días de cotización)
- **Frecuencia:** Diaria (Open, High, Low, Close, Volume)
- **Fuente:** Yahoo Finance (`yfinance`)

## 🔬 Metodología / Factores del Scoring

| Factor | Peso | Métrica | Interpretación |
|--------|------|---------|----------------|
| **Rentabilidad** | **25%** | Anualizada | Retorno histórico |
| **Riesgo (VaR)** | **20%** | Percentil 95% | Pérdida potencial |
| **Momentum** | **15%** | RSI(14) + Mom(20) | Fuerza reciente |
| **Tendencia** | **15%** | SMA20 vs SMA50 | Dirección técnica |
| **Volatilidad** | **10%** | 30 días anualizada | Estabilidad |
| **Drawdown** | **10%** | % desde máximo | Recuperación |
| **Diversificación** | **5%** | Correlación | Reducción riesgo |

## 📈 Resultados Típicos (Ejemplo 2025)

🏆 RANKING POR SCORE (0-10):

BBVA.MC → 8.7 ⭐ COMPRA FUERTE

SAN.MC → 7.9 ⭐ COMPRA

BKT.MC → 7.2 MANTENER

CABK.MC → 6.1 MANTENER

UNI.MC → 5.4 ⚠️ VENDER

SAB.MC → 4.2 ❌ VENTA FUERTE

text

**Portfolio sugerido (100€):**
BBVA: 35€ | SAN: 30€ | BKT: 20€ | CABK: 15€
VaR 95% portfolio: -2.8% (vs -4.1% individual)

text

## 🛠️ Tech Stack Completo

Data: yfinance, pandas, numpy
Technical Analysis: TA-Lib (RSI, SMA, momentum)
Visualization: matplotlib, seaborn
Scoring: Custom weighted algorithm
Output: Formateo español (1.234,56 €)

text

## 🚀 Instalación y Uso

```bash
git clone https://github.com/jorgegalanr/spanish-banks-stock-prediction.git
cd spanish-banks-stock-prediction
pip install -r requirements.txt
python main.py --period 5y  # 5 años de datos
# o
jupyter notebook analysis.ipynb
Comandos rápidos:

bash
python scorer.py          # Scoring actual
python portfolio.py       # Portfolio óptimo
python quick_reco.py      # Recomendaciones día a día
📁 Estructura del Proyecto
text
├── data/
│   ├── historical/       # Datos cacheados
│   └── current.csv       # Última actualización
├── notebooks/
│   └── full_analysis.ipynb
├── src/
│   ├── data_fetcher.py
│   ├── technical_indicators.py
│   ├── scoring_engine.py
│   └── portfolio_optimizer.py
├── figures/
│   ├── ranking_heatmap.png
│   └── portfolio_alloc.png
├── main.py
├── requirements.txt
└── README.md
🎯 Aplicaciones Reales
text
💼 Gestión de Cartera Personal
🏦 Análisis rápido para brokers minoristas
📊 Reporting interno de fondos
🎓 Material didáctico Finanzas Cuantitativas
⚠️ Disclaimer: Proyecto educativo. No constituye asesoramiento financiero.

👤 Autor
Jorge Galán Rodríguez
💼 linkedin.com/in/jorgegalanrodriguez
🐱 https://github.com/jorgegalanr
jorgegalanrodriguez@gmail.com


