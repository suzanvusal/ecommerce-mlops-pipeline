"""
tests/unit/test_consumer.py
Day 5: Kafka consumer & event validation pipeline
Focus: Event consumer, validation, DLQ routing, session tracking
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:09:39 — refactor: rename variable for clarity in test_consumer
