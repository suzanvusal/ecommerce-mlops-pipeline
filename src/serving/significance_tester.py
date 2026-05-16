"""
src/serving/significance_tester.py
Day 16: A/B testing framework for recommendations
Focus: Traffic splitting, experiment logging, statistical significance testing
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:02:24 — feat: add experiment audit log
