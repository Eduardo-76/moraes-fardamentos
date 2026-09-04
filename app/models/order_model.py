from dataclasses import dataclass, field
from typing import Optional

from more_itertools import one


@dataclass
class OrderItemModel:
    id: Optional[int] = None
    order_id: Optional[int] = None
    size: Optional[str] = None
    gender: Optional[str] = None
    quantity: Optional[int] = None


@dataclass
class OrderModel:

    id: Optional[int] = None
    client_id: Optional[int] = None
    client_name: Optional[str] = None
    client_phone: Optional[str] = None
    client_city: Optional[str] = None
    model: Optional[str] = None
    fabric: Optional[str] = None
    type: Optional[str] = None
    quantity: Optional[int] = None
    deadline: Optional[str] = None
    priority: Optional[str] = None
    unit_value: float = 0.0
    total_value: float = 0.0
    paid: int = 0
    stock_reserved: int = 0
    stock_withdrawn: int = 0
    withdrawn_at: Optional[str] = None
    notes: Optional[str] = None
    current_stage: str = "Recepção"
    status: str = "Em espera"
    created_at: Optional[str] = None
    items: list[OrderItemModel] = field(default_factory=list)
    audio_id: Optional[int] = None