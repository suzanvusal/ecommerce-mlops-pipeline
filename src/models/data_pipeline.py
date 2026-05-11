"""
src/models/data_pipeline.py
Day 11: MLflow experiment tracking & training data pipeline
Focus: MLflow setup, interaction matrix, train/val/test split
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:47:42 — refactor: separate matrix building from feature extraction
