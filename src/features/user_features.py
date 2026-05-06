"""User behaviour feature engineering for recommendation system."""
from __future__ import annotations
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class RFMScore:
    user_id:   str
    recency:   float   # Days since last purchase (lower = better)
    frequency: float   # Number of purchases in last 90 days
    monetary:  float   # Total spend in last 90 days
    rfm_score: float   # Combined normalised score 0-1

    @property
    def segment(self) -> str:
        if self.rfm_score >= 0.8:
            return "champions"
        elif self.rfm_score >= 0.6:
            return "loyal"
        elif self.rfm_score >= 0.4:
            return "at_risk"
        else:
            return "churned"


@dataclass
class UserFeatureVector:
    user_id:               str
    rfm_score:             float
    rfm_segment:           str
    avg_order_value:       float
    purchase_frequency:    float   # purchases per week
    cart_abandonment_rate: float
    category_diversity:    float   # unique categories / total clicks
    discount_sensitivity:  float   # pct purchases with discount
    session_duration_avg:  float   # minutes
    device_mobile_ratio:   float
    prime_member:          bool
    days_since_last_purchase: float
    preferred_category:    str
    ltv_estimate:          float


class RFMCalculator:
    """Computes Recency-Frequency-Monetary scores for user segmentation."""

    def __init__(self, max_recency_days: int = 90) -> None:
        self.max_recency = max_recency_days

    def compute(self, user_id: str,
                purchase_dates: list[datetime],
                purchase_amounts: list[float]) -> RFMScore:
        if not purchase_dates:
            return RFMScore(user_id=user_id, recency=self.max_recency,
                           frequency=0, monetary=0, rfm_score=0.0)

        now        = datetime.now(timezone.utc)
        last_date  = max(purchase_dates)
        recency    = (now - last_date).days

        cutoff     = now - timedelta(days=self.max_recency)
        recent_idx = [i for i, d in enumerate(purchase_dates) if d >= cutoff]
        frequency  = len(recent_idx)
        monetary   = sum(purchase_amounts[i] for i in recent_idx)

        r_score = 1 - (recency / self.max_recency)
        f_score = min(frequency / 20, 1.0)
        m_score = min(monetary / 5000, 1.0)

        rfm_score = 0.3 * r_score + 0.35 * f_score + 0.35 * m_score

        return RFMScore(
            user_id=user_id,
            recency=recency,
            frequency=frequency,
            monetary=round(monetary, 2),
            rfm_score=round(rfm_score, 4),
        )


class UserFeatureEngine:
    """Computes comprehensive user features for recommendation models."""

    def __init__(self, rfm_calculator: RFMCalculator | None = None) -> None:
        self.rfm = rfm_calculator or RFMCalculator()

    def compute(self, user_id: str, events: list[dict]) -> UserFeatureVector:
        purchases = [e for e in events if e.get("event_type") == "purchase"]
        clicks    = [e for e in events if e.get("event_type") == "click"]
        carts     = [e for e in events if e.get("event_type") == "add_cart"]

        purchase_dates   = [e.get("timestamp", datetime.now(timezone.utc)) for e in purchases]
        purchase_amounts = [e.get("total_amount", 0.0) for e in purchases]

        rfm = self.rfm.compute(user_id, purchase_dates, purchase_amounts)

        n_clicks    = len(clicks)
        n_carts     = len(carts)
        n_purchases = len(purchases)

        cart_abandonment = (n_carts - n_purchases) / max(n_carts, 1)
        categories  = [e.get("category", "unknown") for e in clicks]
        diversity   = len(set(categories)) / max(len(categories), 1)

        discounted  = sum(1 for p in purchases if p.get("discount_pct", 0) > 0)
        disc_sensitivity = discounted / max(n_purchases, 1)

        preferred_cat = max(set(categories), key=categories.count) if categories else "unknown"

        return UserFeatureVector(
            user_id=user_id,
            rfm_score=rfm.rfm_score,
            rfm_segment=rfm.segment,
            avg_order_value=round(rfm.monetary / max(rfm.frequency, 1), 2),
            purchase_frequency=round(rfm.frequency / 13, 4),
            cart_abandonment_rate=round(cart_abandonment, 4),
            category_diversity=round(diversity, 4),
            discount_sensitivity=round(disc_sensitivity, 4),
            session_duration_avg=0.0,
            device_mobile_ratio=0.5,
            prime_member=False,
            days_since_last_purchase=rfm.recency,
            preferred_category=preferred_cat,
            ltv_estimate=round(rfm.monetary * 1.5, 2),
        )

# 20:25:36 — feat: implement user lifetime value (LTV) estimator

# 20:25:36 — test: add RFM calculator tests with known inputs

# 20:25:36 — fix: RFM recency not using correct time reference
