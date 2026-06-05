from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StockMovementItemModel:
    id: Optional[int] = None
    movement_id: Optional[int] = None
    size: Optional[str] = None
    gender: Optional[str] = None
    quantity: int = 0


@dataclass
class StockMovementModel:
    id: Optional[int] = None
    stock_entry_id: Optional[int] = None
    movement_type: Optional[str] = None
    quantity: int = 0
    notes: Optional[str] = None
    created_at: Optional[str] = None
    items: list[StockMovementItemModel] = field(default_factory=list)