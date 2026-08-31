from typing import List, Optional

from PIL.Image import item

from app.core.database import get_connection
from app.models.stock_model import StockItemModel, StockModel


class StockRepository:
    def list_stock_entries(self) -> List[StockModel]:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    id,
                    model,
                    type,
                    color,
                    fabric,
                    stock_group,
                    stock_category,
                    reference,
                    total_quantity,
                    reserved_quantity,
                    notes,
                    created_at
                FROM stock_entries
                ORDER BY created_at DESC, id DESC
                """
            )
            rows = cursor.fetchall()

            entries: list[StockModel] = []
            for row in rows:
                items = self.list_stock_items(row["id"], connection=connection)
                entries.append(
                    StockModel(
                        id=row["id"],
                        model=row["model"],
                        type=row["type"],
                        color=row["color"],
                        fabric=row["fabric"],
                        stock_group=row["stock_group"],
                        stock_category=row["stock_category"],
                        reference=row["reference"],
                        total_quantity=row["total_quantity"],
                        reserved_quantity=row["reserved_quantity"],
                        notes=row["notes"],
                        created_at=row["created_at"],
                        items=items,
                    )
                )

            return entries
        finally:
            connection.close()

    def get_stock_entry_by_id(self, stock_id: int) -> Optional[StockModel]:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    id,
                    model,
                    type,
                    color,
                    fabric,
                    stock_group,
                    stock_category,
                    reference,
                    total_quantity,
                    reserved_quantity,
                    notes,
                    created_at
                FROM stock_entries
                WHERE id = ?
                """,
                (stock_id,),
            )
            row = cursor.fetchone()

            if not row:
                return None

            items = self.list_stock_items(stock_id, connection=connection)

            return StockModel(
                id=row["id"],
                model=row["model"],
                type=row["type"],
                color=row["color"],
                fabric=row["fabric"],
                stock_group=row["stock_group"],
                stock_category=row["stock_category"],
                reference=row["reference"],
                total_quantity=row["total_quantity"],
                reserved_quantity=row["reserved_quantity"],
                notes=row["notes"],
                created_at=row["created_at"],
                items=items,
            )
        finally:
            connection.close()

    def create_stock_entry(self, stock: StockModel) -> int:
        connection = get_connection()
        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO stock_entries (
                    model,
                    type,
                    color,
                    fabric,
                    stock_group,
                    stock_category,
                    reference,
                    total_quantity,
                    reserved_quantity,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    stock.model,
                    stock.type,
                    stock.color,
                    stock.fabric,
                    stock.stock_group,
                    stock.stock_category,
                    stock.reference,
                    stock.total_quantity,
                    stock.reserved_quantity,
                    stock.notes,
                ),
            )
            stock_id = int(cursor.lastrowid)

            for item in stock.items:
                cursor.execute(
                    """
                    INSERT INTO stock_entry_items (stock_entry_id, size, gender, quantity,reserved_quantity)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        stock_id,
                        item.size,
                        item.gender,
                        item.quantity,
                        item.reserved_quantity,
                    ),
                )

            connection.commit()
            return stock_id
        finally:
            connection.close()

    def update_stock_entry(self, stock: StockModel) -> None:
        if not stock.id:
            return

        connection = get_connection()
        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE stock_entries
                SET
                    model = ?,
                    type = ?,
                    color = ?,
                    fabric = ?,
                    stock_group = ?,
                    stock_category = ?,
                    reference = ?,
                    total_quantity = ?,
                    reserved_quantity = ?,
                    notes = ?
                WHERE id = ?
                """,
                (
                    stock.model,
                    stock.type,
                    stock.color,
                    stock.fabric,
                    stock.stock_group,
                    stock.stock_category,
                    stock.reference,
                    stock.total_quantity,
                    stock.reserved_quantity,
                    stock.notes,
                    stock.id,
                ),
            )

            cursor.execute(
                "DELETE FROM stock_entry_items WHERE stock_entry_id = ?",
                (stock.id,),
            )

            for item in stock.items:
                cursor.execute(
                    """
                    INSERT INTO stock_entry_items (stock_entry_id, size, gender, quantity, reserved_quantity)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (
                        stock.id,
                        item.size,
                        item.gender,
                        item.quantity,
                        item.reserved_quantity,
                    ),
                )

            connection.commit()
        finally:
            connection.close()

    def delete_stock_entry(self, stock_id: int) -> None:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM stock_entries WHERE id = ?", (stock_id,))
            connection.commit()
        finally:
            connection.close()

    def list_stock_items(self, stock_id: int, connection=None) -> list[StockItemModel]:
        owns_connection = connection is None
        if owns_connection:
            connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, stock_entry_id, size, gender, quantity, reserved_quantity
                FROM stock_entry_items
                WHERE stock_entry_id = ?
                ORDER BY id ASC
                """,
                (stock_id,),
            )
            rows = cursor.fetchall()

            return [
                StockItemModel(
                    id=item["id"],
                    stock_entry_id=item["stock_entry_id"],
                    size=item["size"],
                    gender=item["gender"],
                    quantity=item["quantity"],
                    reserved_quantity=item["reserved_quantity"],
                )
                for item in rows
            ]
        finally:
            if owns_connection:
                connection.close()

    def reserve_stock(
        self,
        stock_id: int,
        quantity: int
    ):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                UPDATE stock_entries
                SET reserved_quantity = reserved_quantity + ?
                WHERE id = ?
            """, (
                quantity,
                stock_id
            ))

            connection.commit()

        finally:
            connection.close()

    def release_stock(
        self,
        stock_id: int,
        quantity: int
    ):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                UPDATE stock_entries
                SET reserved_quantity = reserved_quantity - ?
                WHERE id = ?
            """, (
                quantity,
                stock_id
            ))

            connection.commit()

        finally:
            connection.close()

    def reserve_stock_item(
        self,
        item_id: int,
        quantity: int
    ):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                UPDATE stock_entry_items
                SET reserved_quantity =
                    reserved_quantity + ?
                WHERE id = ?
            """, (
                quantity,
                item_id
            ))

            connection.commit()

        finally:
            connection.close()

    def unreserve_stock_item(
        self,
        item_id: int,
        quantity: int
    ):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                UPDATE stock_entry_items
                SET reserved_quantity =
                    reserved_quantity - ?
                WHERE id = ?
            """, (
                quantity,
                item_id
            ))

            connection.commit()

        finally:
            connection.close()

    def withdraw_stock_item(
        self,
        item_id: int,
        quantity: int
    ):
        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE stock_entry_items
                SET
                    quantity = quantity - ?,
                    reserved_quantity = reserved_quantity - ?
                WHERE id = ?
                """,
                (
                    quantity,
                    quantity,
                    item_id
                )
            )

            connection.commit()

        finally:
            connection.close()


    def release_stock_item(
        self,
        item_id: int,
        quantity: int
    ):

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute("""
                UPDATE stock_entry_items
                SET reserved_quantity =
                    reserved_quantity - ?
                WHERE id = ?
            """, (
                quantity,
                item_id
            ))

            connection.commit()

        finally:
            connection.close()

    def get_stock_item_by_id(
        self,
        item_id: int
    ):
        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    stock_entry_id,
                    size,
                    gender,
                    quantity,
                    reserved_quantity
                FROM stock_entry_items
                WHERE id = ?
                """,
                (item_id,)
            )

            row = cursor.fetchone()

            if not row:
                return None

            return StockItemModel(
                id=row["id"],
                stock_entry_id=row["stock_entry_id"],
                size=row["size"],
                gender=row["gender"],
                quantity=row["quantity"],
                reserved_quantity=row["reserved_quantity"],
            )

        finally:
            connection.close()

    def withdraw_stock_item_direct(
        self,
        item_id: int,
        quantity: int,
    ) -> None:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE stock_entry_items
                SET quantity = quantity - ?
                WHERE id = ?
                AND quantity >= ?
                """,
                (
                    quantity,
                    item_id,
                    quantity,
                ),
            )

            if cursor.rowcount == 0:
                raise ValueError(
                    "Quantidade insuficiente ou item de estoque não encontrado."
                )

            connection.commit()

        finally:
            connection.close()