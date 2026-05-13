"""
src/recommendations/implicit_feedback.py
Day 12: Collaborative filtering with ALS
Focus: Alternating Least Squares, implicit feedback, top-K recommendations
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:47:39 — fix: handle None edge case in implicit_feedback
