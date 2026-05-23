"""
src/forecasting/forecast_store.py
Day 18: Demand forecasting with Prophet
Focus: Facebook Prophet for time-series demand forecasting, seasonality
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:26:17 — fix: Prophet crashing on products with fewer than 30 data po

# 20:07:21 — style: run black formatter on forecast_store
