"""
src/monitoring/performance_monitor.py
Day 23: Evidently drift detection
Focus: User behaviour drift, product popularity drift, model performance monitoring
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:07:21 — fix: reference builder including holiday periods causing fal
