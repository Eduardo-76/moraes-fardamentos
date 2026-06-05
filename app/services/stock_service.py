from typing import List, Optional
from datetime import datetime, timedelta
from app.core.utils import normalize_gender, normalize_int, normalize_size, normalize_text
from app.models.order_model import OrderModel
from app.models.stock_model import StockItemModel, StockModel
from app.repositories.stock_repository import StockRepository
from app.models.order_model import OrderItemModel


class StockService:
    def __init__(self) -> None:
        self.repository = StockRepository()

    def list_upcoming_deadline_orders(self, days: int = 5) -> List[OrderModel]:
        today = datetime.now().date()
        limit_date = today + timedelta(days=days)

        upcoming_orders = []

        for order in self.list_orders():
            if not order.deadline:
                continue

            try:
                deadline_date = datetime.strptime(order.deadline, "%Y-%m-%d").date()
            except ValueError:
                continue

            if today <= deadline_date <= limit_date:
                upcoming_orders.append(order)

        return upcoming_orders

    def list_late_orders(self) -> List[OrderModel]:
        today = datetime.now().date()
        late_orders = []

        for order in self.list_orders():
            if not order.deadline:
                continue

            try:
                deadline_date = datetime.strptime(order.deadline, "%Y-%m-%d").date()
            except ValueError:
                continue

            if deadline_date < today and order.current_stage != "Retirada":
                late_orders.append(order)

        return late_orders

    def list_orders_without_stock_withdrawn(self) -> List[OrderModel]:
        return [
            order for order in self.list_orders()
            if not order.stock_withdrawn
        ]

    def count_orders_in_production(self) -> int:
        return sum(
            1 for order in self.list_orders()
            if order.current_stage not in ["Recepção", "Retirada"]
        )

    def list_stock_entries(self) -> List[StockModel]:
        return self.repository.list_stock_entries()

    def get_stock_entry_by_id(self, stock_id: int) -> Optional[StockModel]:
        return self.repository.get_stock_entry_by_id(stock_id)

    def create_stock_entry(
        self,
        model: Optional[str],
        type: Optional[str],
        color: Optional[str],
        fabric: Optional[str],
        stock_group: Optional[str],
        stock_category: Optional[str],
        reference: Optional[str],
        total_quantity,
        notes: Optional[str],
        items: Optional[list[dict]] = None,
    ) -> int:
        stock_items: list[StockItemModel] = []
        for item in items or []:
            stock_items.append(
                StockItemModel(
                    size=normalize_size(item.get("size")),
                    gender=normalize_gender(item.get("gender")),
                    quantity=normalize_int(str(item.get("quantity")) if item.get("quantity") is not None else None),
                )
            )




        stock = StockModel(
            model=normalize_text(model),
            type=normalize_text(type),
            color=normalize_text(color),
            fabric=normalize_text(fabric),
            stock_group=normalize_text(stock_group),
            stock_category=normalize_text(stock_category),
            reference=normalize_text(reference),
            total_quantity=normalize_int(str(total_quantity) if total_quantity is not None else None),
            notes=normalize_text(notes),
            items=stock_items,
        )
        return self.repository.create_stock_entry(stock)

    def update_stock_entry(
        self,
        stock_id: int,
        model: Optional[str],
        type: Optional[str],
        color: Optional[str],
        fabric: Optional[str],
        stock_group: Optional[str],
        stock_category: Optional[str],
        reference: Optional[str],
        total_quantity,
        notes: Optional[str],
        items: Optional[list[dict]] = None,
    ) -> None:
        stock_items: list[StockItemModel] = []
        for item in items or []:
            stock_items.append(
                StockItemModel(
                    size=normalize_size(item.get("size")),
                    gender=normalize_gender(item.get("gender")),
                    quantity=normalize_int(str(item.get("quantity")) if item.get("quantity") is not None else None),
                )
            )

        stock = StockModel(
            id=stock_id,
            model=normalize_text(model),
            type=normalize_text(type),
            color=normalize_text(color),
            fabric=normalize_text(fabric),
            stock_group=normalize_text(stock_group),
            stock_category=normalize_text(stock_category),
            reference=normalize_text(reference),
            total_quantity=normalize_int(str(total_quantity) if total_quantity is not None else None),
            notes=normalize_text(notes),
            items=stock_items,
        )
        self.repository.update_stock_entry(stock)

    def delete_stock_entry(self, stock_id: int) -> None:
        self.repository.delete_stock_entry(stock_id)

    def create_sample_stock_if_empty(self) -> None:
        if self.list_stock_entries():
            return

        self.create_stock_entry(
            model="Blusas",
            type="Camisa Tradicional",
            color="Branca",
            fabric="Dryfit",
            stock_group="Escolar",
            stock_category="Base",
            reference=None,
            total_quantity=100,
            notes="Base para personalização",
            items=[
                {"size": "M", "gender": "Masculina", "quantity": 50},
                {"size": "M", "gender": "Feminina", "quantity": 50},
            ],
        )

        self.create_stock_entry(
            model="Calça Colégio Estado",
            type="Calça",
            color="Verde",
            fabric="Helanca",
            stock_group="Escolar",
            stock_category="Base",
            reference=None,
            total_quantity=100,
            notes="Pode atender diferentes colégios",
            items=[
                {"size": "M", "gender": "Masculina", "quantity": 25},
                {"size": "G", "gender": "Masculina", "quantity": 25},
                {"size": "M", "gender": "Feminina", "quantity": 25},
                {"size": "G", "gender": "Feminina", "quantity": 25},
            ],
        )

    def find_stock_item(
        self,
        size: str,
        gender: str
    ):

        for stock in self.list_stock_entries():

            for item in stock.items:

                if (
                    item.size == size
                    and item.gender == gender
                ):
                    return stock, item

        return None, None

    def simulate_order_reservation(
        self,
        order_items
    ):

        result = []

        for order_item in order_items:

            stock, stock_item = self.find_stock_item(
                order_item.size,
                order_item.gender
            )

            print(
                "Pedido:",
                order_item.size,
                order_item.gender,
                order_item.quantity
            )

            print(
                "Encontrado:",
                stock_item
            )



            if not stock_item:

                result.append({
                    "size": order_item.size,
                    "gender": order_item.gender,
                    "requested": order_item.quantity,
                    "reserved": 0,
                    "missing": order_item.quantity
                })

                continue

            available = (
                stock_item.quantity
                - stock_item.reserved_quantity
            )

            reserved = min(
                available,
                order_item.quantity
            )

            missing = (
                order_item.quantity
                - reserved
            )

            result.append({
                "size": order_item.size,
                "gender": order_item.gender,
                "requested": order_item.quantity,
                "reserved": reserved,
                "missing": missing
            })

        return result
    
    def reserve_order_stock(
        self,
        order_items
    ):

        result = []

        for order_item in order_items:

            stock, stock_item = self.find_stock_item(
                order_item.size,
                order_item.gender
            )

            if not stock_item:

                result.append({
                    "size": order_item.size,
                    "gender": order_item.gender,
                    "reserved": 0,
                    "missing": order_item.quantity
                })

                continue

            available = (
                stock_item.quantity
                - stock_item.reserved_quantity
            )

            reserved = min(
                available,
                order_item.quantity
            )

            missing = (
                order_item.quantity
                - reserved
            )

            if reserved > 0:

                self.repository.reserve_stock_item(
                    stock_item.id,
                    reserved
                )

            result.append({
                "size": order_item.size,
                "gender": order_item.gender,
                "reserved": reserved,
                "missing": missing
            })

        return result