"""
src/forecasting/forecast_ensemble.py
Day 19: XGBoost demand forecasting with features
Focus: XGBoost tabular forecaster with lag features, promotions, weather
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:46:44 — feat: add cross-product demand spillover features

# 20:46:44 — fix: lag features leaking future demand
