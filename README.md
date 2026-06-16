# 🏆 2026 World Cup Predictive Analytics Hub

An end-to-end data science and predictive machine learning dashboard built to simulate, visualize, and forecast the knockout progression of the 2026 FIFA World Cup. 

This repository spans the entire data pipeline workflow—including historical data alignment, feature engineering, local validation baseline training using cross-validated **LightGBM** models, and deployment via an interactive, high-fidelity **Streamlit** web user interface.

---

## 🚀 Key Features

* **Algorithmic Predictive Engine:** Utilizes optimized LightGBM models trained on engineered historical football features (team form, attacking velocity, and defensive metrics) to calculate dynamic matchup distributions.
* **Full 16-Team Knockout Bracket:** A completely responsive, custom CSS-rendered tournament tree that visually maps progression pathways straight from the Round of 16 to the final podium card—eliminating broken text-based lines for non-tech fans and football enthusiasts.
* **Live Match Playground Simulator:** An interactive simulation matrix in the sidebar allowing users to match any two teams head-to-head, inject custom tournament volatility (variance sliders), and model unexpected underdog upsets on the fly.
* **Dynamic Plotly Analytics:** Integrated charting interfaces visualizing relative strengths by graphing Attacking Velocity against Defensive Stability ratings across qualified nations.

---

## 📁 Project Architecture & Workspace

The project is structured across modular tracking notebooks and a central application script:

* `01_data_alignment.ipynb` — Handles primary ingestion, structural dataframe cleaning, and initial structural alignment.
* `02_historical_feature_store.ipynb` — Builds historical feature aggregations, tournament depth variables, and team strength indicators.
* `03_local_validation_and_baseline (1).ipynb` — Sets up model stratification, cross-validation tuning loops, and baseline evaluation splits.
* `app.py` — The production script containing the backend mathematical simulation logic and the custom-styled frontend layout UI.
* `data/` — Secure project folder housing historical dataset parameters (matches, penalty kicks, goals, team appearances, and groups).

---

## 🛠️ Local Installation & Setup Guide

To run this predictive engine dashboard locally on your workstation, follow the installation steps below:

### 1. Clone the Repository
```bash
git clone [https://github.com/MouroshK/World_cup_2026.git](https://github.com/MouroshK/World_cup_2026.git)
cd World_cup_2026
