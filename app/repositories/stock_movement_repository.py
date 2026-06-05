from typing import Optional

from app.core.database import get_connection
from app.models.stock_movement_model import (
    StockMovementItemModel,
    StockMovementModel,
)


class StockMovementRepository:
    def create_movement(self, movement: StockMovementModel) -> int:
        connection = get_connection()
        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO stock_movements (stock_entry_id, movement_type, quantity, notes)
                VALUES (?, ?, ?, ?)
                """,
                (
                    movement.stock_entry_id,
                    movement.movement_type,
                    movement.quantity,
                    movement.notes,
                ),
            )
            movement_id = int(cursor.lastrowid)

            for item in movement.items:
                cursor.execute(
                    """
                    INSERT INTO stock_movement_items (movement_id, size, gender, quantity)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        movement_id,
                        item.size,
                        item.gender,
                        item.quantity,
                    ),
                )

            connection.commit()
            return movement_id
        finally:
            connection.close()

    def list_movements_by_stock_entry(self, stock_entry_id: int) -> list[StockMovementModel]:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, stock_entry_id, movement_type, quantity, notes, created_at
                FROM stock_movements
                WHERE stock_entry_id = ?
                ORDER BY created_at DESC, id DESC
                """,
                (stock_entry_id,),
            )
            rows = cursor.fetchall()

            movements: list[StockMovementModel] = []
            for row in rows:
                items = self.list_movement_items(row["id"], connection=connection)
                movements.append(
                    StockMovementModel(
                        id=row["id"],
                        stock_entry_id=row["stock_entry_id"],
                        movement_type=row["movement_type"],
                        quantity=row["quantity"],
                        notes=row["notes"],
                        created_at=row["created_at"],
                        items=items,
                    )
                )

            return movements
        finally:
            connection.close()

    def list_movement_items(self, movement_id: int, connection=None) -> list[StockMovementItemModel]:
        owns_connection = connection is None
        if owns_connection:
            connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, movement_id, size, gender, quantity
                FROM stock_movement_items
                WHERE movement_id = ?
                ORDER BY id ASC
                """,
                (movement_id,),
            )
            rows = cursor.fetchall()

            return [
                StockMovementItemModel(
                    id=row["id"],
                    movement_id=row["movement_id"],
                    size=row["size"],
                    gender=row["gender"],
                    quantity=row["quantity"],
                )
                for row in rows
            ]
        finally:
            if owns_connection:
                connection.close()