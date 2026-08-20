from dataclasses import dataclass, field
from typing import Optional


@dataclass
class PrintGradeItemModel:
    size: str
    quantity: int


@dataclass
class PrintGradeModel:
    group: str
    order: int
    items: list[PrintGradeItemModel] = field(default_factory=list)


@dataclass
class PrintJobModel:
    order_id: int

    client_name: str
    client_phone: Optional[str] = None
    client_city: Optional[str] = None

    delivery_date: Optional[str] = None

    model: Optional[str] = None
    fabric: Optional[str] = None
    type: Optional[str] = None

    unit_value: float = 0.0
    total_value: float = 0.0

    artwork_file: Optional[str] = None
    template_file: Optional[str] = None

    grades: list[PrintGradeModel] = field(default_factory=list)

    created_at: Optional[str] = None
    printed_at: Optional[str] = None

    observations: Optional[str] = None
    designer: Optional[str] = None
    receptionist: Optional[str] = None

    copies: int = 1