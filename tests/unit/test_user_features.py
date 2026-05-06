"""
tests/unit/test_user_features.py
Day 6: User behaviour feature engineering
Focus: Session features, click-through rates, purchase propensity, recency
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:25:36 — feat: implement device type preference features

# 20:25:37 — fix: LTV estimator crashing on users with single purchase
