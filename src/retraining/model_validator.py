"""
src/retraining/model_validator.py
Day 25: Model validation & canary deployment
Focus: Offline and online validation, champion/challenger, canary with business metrics
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:23:32 — refactor: decouple validation from MLflow registration

# 20:23:32 — docs: add model governance policy

# 21:10:01 — refactor: extract constant in model_validator
