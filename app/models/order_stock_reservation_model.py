from dataclasses import dataclass
from typing import Optional


@dataclass
class OrderStockReservationModel:
    id: Optional[int] = None

    order_id: int = 0

    stock_entry_id: int = 0
    stock_item_id: int = 0

    quantity: int = 0

    status: str = "RESERVED"

    created_at: Optional[str] = None
    cancelled_at: Optional[str] = None
    withdrawn_at: Optional[str] = None