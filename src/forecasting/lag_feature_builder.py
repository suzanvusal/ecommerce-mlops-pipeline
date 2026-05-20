"""
src/forecasting/lag_feature_builder.py
Day 19: XGBoost demand forecasting with features
Focus: XGBoost tabular forecaster with lag features, promotions, weather
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:46:44 — feat: add forecast uncertainty quantification

# 20:46:44 — refactor: extract lag builder to separate class

# 20:59:51 — fix: handle None edge case in lag_feature_builder
