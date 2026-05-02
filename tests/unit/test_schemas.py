"""Unit tests for e-commerce event schemas."""
import uuid
from datetime import datetime, timezone
import pytest
from pydantic import ValidationError
from src.ingestion.schemas import (
    ClickEvent, PurchaseEvent, ProductInfo, UserContext, DeviceType
)


def make_product(**kw) -> dict:
    return dict(product_id="PROD-000001", category="Electronics",
                price=99.99, **kw)


def make_user(**kw) -> dict:
    return dict(user_id="USR-00000001", session_id=str(uuid.uuid4()), **kw)


def test_valid_click_event():
    e = ClickEvent(
        event_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
        user=UserContext(**make_user()),
        product=ProductInfo(**make_product()),
        position=3,
    )
    assert e.position == 3


def test_product_effective_price_with_discount():
    p = ProductInfo(**make_product(discount_pct=0.2))
    assert p.effective_price == pytest.approx(79.99, rel=1e-3)


def test_product_effective_price_no_discount():
    p = ProductInfo(**make_product(discount_pct=0.0))
    assert p.effective_price == 99.99


def test_negative_price_rejected():
    with pytest.raises(ValidationError):
        ProductInfo(**make_product(price=-10.0))


def test_discount_over_100_rejected():
    with pytest.raises(ValidationError):
        ProductInfo(**make_product(discount_pct=1.5))


def test_purchase_event_item_count():
    items = [ProductInfo(**make_product(product_id=f"PROD-{i:06d}")) for i in range(3)]
    e = PurchaseEvent(
        event_id=str(uuid.uuid4()),
        timestamp=datetime.now(timezone.utc),
        user=UserContext(**make_user()),
        items=items,
        order_id="ORD-ABC123",
        total_amount=299.97,
    )
    assert e.item_count == 3

# 19:55:07 — feat: implement Kafka producer with retry and compression
