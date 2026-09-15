from dataclasses import dataclass
from typing import Optional


@dataclass
class PaymentModel:
    id: Optional[int] = None
    order_id: int = 0
    amount: float = 0.0
    payment_method: str = ""
    paid_at: Optional[str] = None
    notes: Optional[str] = None