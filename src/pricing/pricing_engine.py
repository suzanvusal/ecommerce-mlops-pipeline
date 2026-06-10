"""Dynamic pricing engine with demand-based optimisation."""
from __future__ import annotations
import logging
import math
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class PricingConstraints:
    min_margin_pct:     float = 0.15
    max_price_change:   float = 0.20
    min_price:          float = 0.01
    max_price_multiple: float = 5.0


@dataclass
class PriceRecommendation:
    product_id:     str
    current_price:  float
    recommended_price: float
    price_change_pct:  float
    expected_demand_change: float
    expected_revenue_change:float
    reasoning:      str


@dataclass
class ElasticityEstimate:
    product_id:  str
    elasticity:  float   # Price elasticity of demand (typically negative)
    confidence:  float


class PriceElasticityModel:
    """Estimates price elasticity from historical price/demand data."""

    def estimate(self, price_history: list[float],
                 demand_history: list[float]) -> ElasticityEstimate:
        if len(price_history) < 5:
            return ElasticityEstimate("unknown", -1.5, 0.3)

        import numpy as np
        log_prices  = np.log(np.array(price_history) + 1e-8)
        log_demands = np.log(np.array(demand_history) + 1e-8)

        # OLS regression on log-log transformation
        X = np.column_stack([np.ones(len(log_prices)), log_prices])
        try:
            beta = np.linalg.lstsq(X, log_demands, rcond=None)[0]
            elasticity = float(beta[1])
            r_squared  = float(np.corrcoef(log_prices, log_demands)[0, 1] ** 2)
        except Exception:
            elasticity = -1.5
            r_squared  = 0.3

        return ElasticityEstimate(
            product_id="",
            elasticity=max(-5.0, min(0.0, elasticity)),
            confidence=round(r_squared, 4),
        )


class DynamicPricingEngine:
    """Demand-driven dynamic pricing with margin and change constraints."""

    def __init__(self, constraints: PricingConstraints | None = None) -> None:
        self.constraints = constraints or PricingConstraints()
        self._elasticity_model = PriceElasticityModel()

    def recommend_price(self, product_id: str,
                        current_price: float,
                        cost_price: float,
                        demand_forecast: float,
                        elasticity: float = -1.5,
                        competitor_price: Optional[float] = None) -> PriceRecommendation:
        c = self.constraints
        min_price = cost_price * (1 + c.min_margin_pct)
        max_change = current_price * c.max_price_change

        # Target: maximise revenue = price × demand
        # At optimum: 1 + 1/elasticity = 0 (Lerner condition)
        # Simplified: if demand is high, nudge price up slightly
        if demand_forecast > 100:
            target = current_price * 1.05
        elif demand_forecast < 30:
            target = current_price * 0.95
        else:
            target = current_price

        # Competitor adjustment
        if competitor_price:
            if competitor_price < current_price * 0.9:
                target = min(target, competitor_price * 1.02)

        # Apply constraints
        target = max(min_price, target)
        target = max(current_price - max_change, min(current_price + max_change, target))
        target = max(c.min_price, target)
        target = round(target, 2)

        pct_change     = (target - current_price) / current_price
        demand_change  = pct_change * elasticity
        revenue_change = pct_change + demand_change

        return PriceRecommendation(
            product_id=product_id,
            current_price=current_price,
            recommended_price=target,
            price_change_pct=round(pct_change, 4),
            expected_demand_change=round(demand_change, 4),
            expected_revenue_change=round(revenue_change, 4),
            reasoning=(
                f"Demand forecast={demand_forecast:.0f}. "
                f"Elasticity={elasticity:.2f}. "
                f"Min price (margin): ${min_price:.2f}."
            ),
        )

# 20:59:51 — refactor: separate pricing rules from optimisation

# 21:25:34 — test: add assertion for return type in pricing_engine
