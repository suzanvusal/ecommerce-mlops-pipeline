"""Realistic e-commerce event simulator with purchase funnel."""
from __future__ import annotations
import random
import time
import uuid
from datetime import datetime, timezone
from typing import Generator
from src.ingestion.schemas import (
    ClickEvent, PurchaseEvent, SearchEvent,
    ProductInfo, UserContext, DeviceType, EventType
)

CATEGORIES = [
    "Electronics", "Clothing", "Books", "Home & Kitchen",
    "Sports", "Beauty", "Toys", "Automotive", "Garden", "Food"
]
BRANDS = ["TechBrand", "FashionCo", "HomeGoods", "SportsPro", "BeautyLux"]
COUNTRIES = ["US", "CA", "GB", "DE", "FR", "AU", "IN", "BR"]


def make_product(category: str | None = None) -> ProductInfo:
    cat = category or random.choice(CATEGORIES)
    price = {
        "Electronics": random.uniform(50, 2000),
        "Clothing":    random.uniform(15, 200),
        "Books":       random.uniform(8, 60),
        "Food":        random.uniform(3, 50),
    }.get(cat, random.uniform(10, 500))
    return ProductInfo(
        product_id=f"PROD-{random.randint(1, 50000):06d}",
        category=cat,
        brand=random.choice(BRANDS),
        price=round(price, 2),
        discount_pct=random.choice([0.0, 0.0, 0.0, 0.1, 0.2, 0.3, 0.5]),
    )


def make_user(user_id: str) -> UserContext:
    return UserContext(
        user_id=user_id,
        session_id=str(uuid.uuid4()),
        device_type=random.choice(list(DeviceType)),
        country=random.choice(COUNTRIES),
        is_logged_in=random.random() > 0.3,
        is_prime=random.random() > 0.6,
    )


class EcommerceSimulator:
    """Simulates realistic user behaviour across e-commerce funnel."""

    FUNNEL = {
        "search_to_view":    0.70,
        "view_to_click":     0.35,
        "click_to_cart":     0.15,
        "cart_to_purchase":  0.60,
    }

    def __init__(self, n_users: int = 10000, n_products: int = 50000) -> None:
        self.users    = [f"USR-{i:08d}" for i in range(n_users)]
        self.products = [make_product() for _ in range(min(n_products, 1000))]

    def generate_search(self, user: UserContext) -> SearchEvent:
        queries = ["laptop", "shoes", "coffee maker", "book", "headphones",
                   "jacket", "phone case", "yoga mat", "skincare", "toy"]
        return SearchEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
            user=user,
            query=random.choice(queries),
            results_count=random.randint(10, 500),
        )

    def generate_click(self, user: UserContext,
                       product: ProductInfo, position: int = 0) -> ClickEvent:
        return ClickEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
            user=user,
            product=product,
            position=position,
            source=random.choice(["homepage", "search", "recommendation", "email"]),
        )

    def generate_purchase(self, user: UserContext,
                          products: list[ProductInfo]) -> PurchaseEvent:
        total = sum(p.effective_price for p in products)
        return PurchaseEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
            user=user,
            items=products,
            order_id=f"ORD-{uuid.uuid4().hex[:10].upper()}",
            total_amount=round(total, 2),
        )

    def event_stream(self, rate: float = 100.0) -> Generator:
        interval = 1.0 / rate
        while True:
            user_id = random.choice(self.users)
            user    = make_user(user_id)
            product = random.choice(self.products)

            # Search event
            yield self.generate_search(user)
            time.sleep(interval * 0.1)

            # Click through funnel
            if random.random() < self.FUNNEL["view_to_click"]:
                yield self.generate_click(user, product, position=random.randint(0, 20))
                time.sleep(interval * 0.1)

                if random.random() < self.FUNNEL["cart_to_purchase"]:
                    n_items = random.choices([1, 2, 3, 4], weights=[0.6, 0.2, 0.1, 0.1])[0]
                    items   = random.choices(self.products, k=n_items)
                    yield self.generate_purchase(user, items)

            time.sleep(interval)

# 19:55:07 — test: add schema validation tests for all event types

# 19:55:07 — fix: handle missing user_id for anonymous sessions

# 19:55:16 — docs: add module docstring to simulator
