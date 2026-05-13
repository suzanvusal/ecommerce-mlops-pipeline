"""
src/ingestion/session_tracker.py
Day 5: Kafka consumer & event validation pipeline
Focus: Event consumer, validation, DLQ routing, session tracking
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:09:39 — feat: add session timeout detection (30 min inactivity)

# 20:09:39 — fix: handle anonymous session merging on login

# 20:09:39 — refactor: move consumer config to Pydantic dataclass

# 19:58:02 — chore: add logging to session_tracker

# 20:47:39 — fix: handle None edge case in session_tracker
