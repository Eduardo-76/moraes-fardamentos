from typing import List, Optional
from datetime import datetime, timedelta
from app.core.utils import normalize_gender, normalize_int, normalize_size, normalize_text
from app.models.order_model import OrderModel
from app.models.stock_model import StockItemModel, StockModel
from app.repositories.stock_repository import StockRepository
from app.models.order_model import OrderItemModel
from app.repositories.order_stock_reservation_repository import (
    OrderStockReservationRepository
)

from app.models.order_stock_reservation_model import (
    OrderStockReservationModel
)
from app.repositories.order_repository import (
    OrderRepository
)

from app.models.stock_movement_model import (
    StockMovementModel,
    StockMovementItemModel,
)
from app.repositories.stock_movement_repository import (
    StockMovementRepository,
)

from app.core.utils import normalize_gender, normalize_size


class StockService:
    def __init__(self) -> None:
        self.repository = StockRepository()
        self.stock_movement_repository = StockMovementRepository()
        self.order_stock_reservation_repository = (
            OrderStockReservationRepository()
        )

        self.order_repository = OrderRepository()

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
        model: str,
        fabric: str,
        size: str,
        gender: str
    ):

        for stock in self.list_stock_entries():

            print("-----------------------")
            print("PEDIDO")
            print("Modelo:", model)
            print("Tecido:", fabric)

            print()

            print("ESTOQUE")
            print("Modelo:", stock.model)
            print("Tecido:", stock.fabric)


            # Produto correto
            if stock.model != model:
                continue

            # Tecido correto
            if stock.fabric != fabric:
                continue

            # Agora procura o tamanho
            for item in stock.items:

                print(
                    item.size,
                    item.gender
                )


                if (
                    item.size == size
                    and item.gender == gender
                ):
                    return stock, item

        return None, None
    
    def simulate_order_reservation(
        self,
        order
    ):

        print(order)
        print(order.items)
        print(len(order.items))

        result = []

        for order_item in order.items:

            stock, stock_item = self.find_stock_item(
                model=order.model,
                fabric=order.fabric,
                size=order_item.size,
                gender=order_item.gender
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
        order,
        stock_entry_id
    ):

        stock = self.get_stock_entry_by_id(
            stock_entry_id
        )

        if not stock:
            raise Exception(
                "Estoque selecionado não encontrado."
            )

        result = []

        for order_item in order.items:

            stock_item = None

            for item in stock.items:

                if (
                    normalize_size(item.size) == normalize_size(order_item.size)
                    and normalize_gender(item.gender) == normalize_gender(order_item.gender)
                ):
                    stock_item = item
                    break

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

            reservation = OrderStockReservationModel(
                order_id=order.id,
                stock_entry_id=stock.id,
                stock_item_id=stock_item.id,
                quantity=reserved,
                status="RESERVED"
            )

            self.order_stock_reservation_repository.create_reservation(
                reservation
            )

            result.append({
                "size": order_item.size,
                "gender": order_item.gender,
                "reserved": reserved,
                "missing": missing
            })

        return result

    def list_active_by_order(
        self,
        order_id: int
    ):
        return (
            self.order_stock_reservation_repository
            .list_active_by_order(order_id)
        )
    
    def cancel_reservation(
        self,
        reservation_id: int
    ):

        reservation = (
            self.order_stock_reservation_repository.get_by_id(
                reservation_id
            )
        )

        if not reservation:
            raise Exception(
                "Reserva não encontrada"
            )

        if reservation["status"] != "RESERVED":
            raise Exception(
                "Esta reserva não está mais ativa"
            )

        order_id = reservation["order_id"]

        self.repository.unreserve_stock_item(
            reservation["stock_item_id"],
            reservation["quantity"]
        )

        self.order_stock_reservation_repository.cancel_reservation(
            reservation_id
        )

        has_active = (
            self.order_stock_reservation_repository
            .has_active_reservations(order_id)
        )


        has_active = (
            self.order_stock_reservation_repository
            .has_active_reservations(order_id)
        )

        if not has_active:
            
            self.order_repository.unmark_stock_reserved(
                order_id
            )

    def withdraw_order_stock(
        self,
        order_id: int
    ):

        reservations = (
            self.order_stock_reservation_repository
            .list_active_by_order(order_id)
        )

        if not reservations:
            raise Exception(
                "Este pedido não possui reservas ativas"
            )

        movement_items = []
        total_quantity = 0

        for reservation in reservations:

            stock_item = self.repository.get_stock_item_by_id(
                reservation["stock_item_id"]
            )

            movement_items.append(
                StockMovementItemModel(
                    size=stock_item.size,
                    gender=stock_item.gender,
                    quantity=reservation["quantity"]
                )
            )

            total_quantity += reservation["quantity"]

        movement = StockMovementModel(
            stock_entry_id=reservations[0]["stock_entry_id"],
            movement_type="Saída",
            quantity=total_quantity,
            notes=f"Baixa vinculada ao pedido #{order_id}",
            items=movement_items,
        )
        print("CRIANDO MOVIMENTACAO")
        self.stock_movement_repository.create_movement(
            movement
        )
        print("MOVIMENTACAO CRIADA")

        for reservation in reservations:

            print(
                "BAIXANDO:",
                reservation["stock_item_id"],
                reservation["quantity"]
            )

            self.repository.withdraw_stock_item(
                reservation["stock_item_id"],
                reservation["quantity"]
            )

            self.order_stock_reservation_repository.withdraw_reservation(
                reservation["id"]
            )

        self.order_repository.mark_stock_withdrawn(
            order_id
        )

        self.order_repository.unmark_stock_reserved(
            order_id
        )

    def withdraw_stock_item_direct(
        self,
        item_id: int,
        quantity: int,
    ) -> None:

        if quantity <= 0:
            raise ValueError(
                "A quantidade da baixa deve ser maior que zero."
            )

        stock_item = self.repository.get_stock_item_by_id(item_id)

        if not stock_item:
            raise ValueError(
                f"Item de estoque #{item_id} não encontrado."
            )

        if stock_item.quantity < quantity:
            raise ValueError(
                f"Estoque insuficiente para "
                f"{stock_item.size} - {stock_item.gender}. "
                f"Disponível: {stock_item.quantity}. "
                f"Solicitado: {quantity}."
            )

        self.repository.withdraw_stock_item_direct(
            item_id,
            quantity,
        )