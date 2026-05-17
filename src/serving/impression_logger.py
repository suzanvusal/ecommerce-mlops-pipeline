"""
src/serving/impression_logger.py
Day 17: Recommendation logging & feedback collection
Focus: Impression logging, click tracking, purchase attribution, feedback loop
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:04:46 — feat: add long-term impact tracker (7-day, 30-day LTV)

# 20:04:47 — perf: batch impression log writes every 200ms
