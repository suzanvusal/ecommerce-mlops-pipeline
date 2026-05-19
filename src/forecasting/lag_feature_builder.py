"""
src/forecasting/lag_feature_builder.py
Day 19: XGBoost demand forecasting with features
Focus: XGBoost tabular forecaster with lag features, promotions, weather
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:46:44 — feat: add forecast uncertainty quantification
