"""
src/ingestion/topic_admin.py
Day 2: E-commerce event schemas & Kafka producers
Focus: Pydantic schemas for clicks, purchases, searches, product views
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 19:55:07 — feat: add ProductCatalog schema with category and pricing

# 19:55:07 — refactor: extract Kafka config to dataclass

# 20:17:58 — refactor: extract constant in topic_admin
