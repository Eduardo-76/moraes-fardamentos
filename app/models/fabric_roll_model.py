from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class FabricRollLocation:
    location_name: str
    quantity: int


@dataclass
class FabricRollModel:
    id: Optional[int] = None
    name: str = ""
    total_quantity: int = 0
    reserved_quantity: int = 0
    locations: list[FabricRollLocation] = field(default_factory=list)

    @property
    def available_quantity(self):
        return self.total_quantity - self.reserved_quantity