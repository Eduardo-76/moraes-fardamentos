from app.core.utils import normalize_gender, normalize_int, normalize_size, normalize_text
from app.models.stock_movement_model import (
    StockMovementItemModel,
    StockMovementModel,
)
from app.repositories.stock_movement_repository import StockMovementRepository
from app.services.stock_service import StockService


class StockMovementService:
    def __init__(self) -> None:
        self.repository = StockMovementRepository()
        self.stock_service = StockService()

    def create_movement(
        self,
        stock_entry_id: int,
        movement_type: str,
        notes: str | None,
        items: list[dict],
    ) -> int:
        stock = self.stock_service.get_stock_entry_by_id(stock_entry_id)
        if not stock:
            raise ValueError("Estoque não encontrado.")

        normalized_items: list[StockMovementItemModel] = []
        total_quantity = 0

        existing_map = {}
        for item in stock.items:
            key = (normalize_size(item.size), normalize_gender(item.gender))
            existing_map[key] = item.quantity

        updated_map = existing_map.copy()

        for raw in items:
            size = normalize_size(raw.get("size"))
            gender = normalize_gender(raw.get("gender"))
            quantity = normalize_int(str(raw.get("quantity")) if raw.get("quantity") is not None else None)

            if not size and not gender and quantity == 0:
                continue

            if quantity <= 0:
                continue

            normalized_items.append(
                StockMovementItemModel(
                    size=size,
                    gender=gender,
                    quantity=quantity,
                )
            )

            total_quantity += quantity

            key = (size, gender)
            current = updated_map.get(key, 0)

            if movement_type == "Entrada":
                updated_map[key] = current + quantity
            elif movement_type == "Saída":
                new_value = current - quantity
                if new_value < 0:
                    raise ValueError(f"Saída inválida para {size} - {gender}. Quantidade insuficiente.")
                updated_map[key] = new_value
            else:
                raise ValueError("Tipo de movimentação inválido.")

        if total_quantity <= 0:
            raise ValueError("Informe pelo menos uma quantidade válida.")

        updated_items = []
        for (size, gender), quantity in updated_map.items():
            if quantity > 0:
                updated_items.append(
                    {
                        "size": size,
                        "gender": gender,
                        "quantity": quantity,
                    }
                )

        if movement_type == "Entrada":
            new_total = stock.total_quantity + total_quantity
        else:
            new_total = stock.total_quantity - total_quantity
            if new_total < 0:
                raise ValueError("Saída inválida. Quantidade total insuficiente.")

        movement = StockMovementModel(
            stock_entry_id=stock_entry_id,
            movement_type=movement_type,
            quantity=total_quantity,
            notes=normalize_text(notes),
            items=normalized_items,
        )

        movement_id = self.repository.create_movement(movement)

        self.stock_service.update_stock_entry(
            stock_id=stock.id,
            model=stock.model,
            type=stock.type,
            color=stock.color,
            fabric=stock.fabric,
            stock_group=stock.stock_group,
            stock_category=stock.stock_category,
            reference=stock.reference,
            total_quantity=new_total,
            notes=stock.notes,
            items=updated_items,
        )

        return movement_id

    def convert_base_to_finished(
        self,
        source_stock_id: int,
        target_model: str | None,
        target_type: str | None,
        target_color: str | None,
        target_fabric: str | None,
        target_group: str | None,
        target_reference: str | None,
        notes: str | None,
        items: list[dict],
    ) -> int:
        source_stock = self.stock_service.get_stock_entry_by_id(source_stock_id)
        if not source_stock:
            raise ValueError("Estoque base não encontrado.")

        if source_stock.stock_category != "Base":
            raise ValueError("A conversão deve partir de um estoque marcado como Base.")

        total_quantity = 0
        converted_items = []

        for raw in items:
            size = normalize_size(raw.get("size"))
            gender = normalize_gender(raw.get("gender"))
            quantity = normalize_int(str(raw.get("quantity")) if raw.get("quantity") is not None else None)

            if not size and not gender and quantity == 0:
                continue

            if quantity <= 0:
                continue

            total_quantity += quantity
            converted_items.append(
                {
                    "size": size,
                    "gender": gender,
                    "quantity": quantity,
                }
            )

        if total_quantity <= 0:
            raise ValueError("Informe pelo menos uma quantidade válida para converter.")

        self.create_movement(
            stock_entry_id=source_stock_id,
            movement_type="Saída",
            notes=f"Conversão para finalizado. {normalize_text(notes) or ''}".strip(),
            items=converted_items,
        )

        finished_stock_id = self.stock_service.create_stock_entry(
            model=target_model or source_stock.model,
            type=target_type or source_stock.type,
            color=target_color or source_stock.color,
            fabric=target_fabric or source_stock.fabric,
            stock_group=target_group or source_stock.stock_group,
            stock_category="Finalizado",
            reference=target_reference,
            total_quantity=total_quantity,
            notes=notes,
            items=converted_items,
        )

        return finished_stock_id

    def list_movements_by_stock_entry(self, stock_entry_id: int) -> list[StockMovementModel]:
        return self.repository.list_movements_by_stock_entry(stock_entry_id)