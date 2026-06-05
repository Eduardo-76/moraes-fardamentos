from dataclasses import dataclass, field
from typing import Optional


@dataclass
class StockItemModel:
    id: Optional[int] = None
    stock_entry_id: Optional[int] = None

    size: Optional[str] = None
    gender: Optional[str] = None

    quantity: int = 0

    # NOVO
    reserved_quantity: int = 0

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity


@dataclass
class StockModel:
    id: Optional[int] = None
    model: Optional[str] = None
    type: Optional[str] = None
    color: Optional[str] = None
    fabric: Optional[str] = None
    stock_group: Optional[str] = None
    stock_category: Optional[str] = None
    reference: Optional[str] = None

    total_quantity: int = 0

    # 🔥 NOVO
    reserved_quantity: int = 0

    notes: Optional[str] = None
    created_at: Optional[str] = None

    items: list[StockItemModel] = field(default_factory=list)

    # 🔥 NOVO
    @property
    def available_quantity(self):
        return self.total_quantity - self.reserved_quantity