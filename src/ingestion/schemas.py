"""Pydantic schemas for e-commerce event streaming."""
from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class EventType(str, Enum):
    CLICK    = "click"
    PURCHASE = "purchase"
    SEARCH   = "search"
    VIEW     = "view"
    ADD_CART = "add_cart"
    REMOVE_CART = "remove_cart"
    WISHLIST = "wishlist"


class DeviceType(str, Enum):
    MOBILE  = "mobile"
    DESKTOP = "desktop"
    TABLET  = "tablet"
    APP     = "app"


class ProductInfo(BaseModel):
    product_id:   str
    category:     str
    subcategory:  Optional[str] = None
    brand:        Optional[str] = None
    price:        float = Field(gt=0)
    discount_pct: float = Field(default=0.0, ge=0.0, le=1.0)

    @property
    def effective_price(self) -> float:
        return round(self.price * (1 - self.discount_pct), 2)


class UserContext(BaseModel):
    user_id:      str
    session_id:   str
    device_type:  DeviceType = DeviceType.DESKTOP
    country:      str = "US"
    is_logged_in: bool = True
    is_prime:     bool = False


class ClickEvent(BaseModel):
    event_id:    str
    event_type:  EventType = EventType.CLICK
    timestamp:   datetime
    user:        UserContext
    product:     ProductInfo
    position:    int = Field(ge=0, description="Position in recommendation list")
    source:      str = "homepage"
    rec_model:   Optional[str] = None

    def to_kafka_dict(self) -> dict:
        return self.model_dump(mode="json")


class PurchaseEvent(BaseModel):
    event_id:      str
    event_type:    EventType = EventType.PURCHASE
    timestamp:     datetime
    user:          UserContext
    items:         list[ProductInfo]
    order_id:      str
    total_amount:  float = Field(gt=0)
    payment_method:str = "card"

    @field_validator("total_amount")
    @classmethod
    def amount_matches_items(cls, v: float, info) -> float:
        return round(v, 2)

    @property
    def item_count(self) -> int:
        return len(self.items)

    def to_kafka_dict(self) -> dict:
        return self.model_dump(mode="json")


class SearchEvent(BaseModel):
    event_id:       str
    event_type:     EventType = EventType.SEARCH
    timestamp:      datetime
    user:           UserContext
    query:          str
    results_count:  int = 0
    clicked_product:Optional[str] = None

    def to_kafka_dict(self) -> dict:
        return self.model_dump(mode="json")

# 19:55:07 — feat: implement realistic e-commerce event simulator

# 19:55:07 — feat: add Black Friday surge simulation mode

# 19:55:07 — fix: simulator not generating realistic purchase funnel rate

# 19:55:07 — style: reorder imports in schemas
