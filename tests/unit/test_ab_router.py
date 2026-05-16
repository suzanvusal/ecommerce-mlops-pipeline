"""
tests/unit/test_ab_router.py
Day 16: A/B testing framework for recommendations
Focus: Traffic splitting, experiment logging, statistical significance testing
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:02:24 — fix: experiment logger dropping events under high load

# 20:02:24 — style: reorder imports in test_ab_router
