from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field
from typing import Literal


class Event(BaseModel):
    event_id: str
    event_ts: str
    user_id: str
    event_type: Literal["page_view", "add_to_cart", "purchase"]
    session_id: str
    product_id: str | None = None
    price_gbp: float | None = None


def test_event_valid() -> None:
    e = Event(
        event_id=str(uuid4()),
        event_ts=datetime.now(timezone.utc).isoformat(),
        user_id="U-0001",
        event_type="purchase",
        session_id=str(uuid4()),
        product_id="SKU-0001",
        price_gbp=12.34,
    )
    assert e.event_type == "purchase"
