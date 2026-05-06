"""
src/ingestion/validator.py
Day 5: Kafka consumer & event validation pipeline
Focus: Event consumer, validation, DLQ routing, session tracking
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:09:39 — test: add consumer integration test

# 20:25:37 — docs: fix typo in validator
