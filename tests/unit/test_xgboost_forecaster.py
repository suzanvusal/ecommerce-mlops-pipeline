"""
tests/unit/test_xgboost_forecaster.py
Day 19: XGBoost demand forecasting with features
Focus: XGBoost tabular forecaster with lag features, promotions, weather
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:46:44 — fix: ensemble weights not optimised per category
