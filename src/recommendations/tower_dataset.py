"""
src/recommendations/tower_dataset.py
Day 13: Two-Tower deep learning model
Focus: PyTorch two-tower model, user/item towers, contrastive learning
"""
from __future__ import annotations
import logging

logger = logging.getLogger(__name__)

# 20:52:12 — fix: correct off-by-one in tower_dataset
