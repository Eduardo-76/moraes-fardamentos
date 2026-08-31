from datetime import datetime
from typing import List, Optional

from app.core.constants import ORDER_STAGES
from app.core.database import get_connection
from app.models.order_model import OrderItemModel, OrderModel


class OrderRepository:
    def create_order(self, order: OrderModel) -> int:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                INSERT INTO orders (
                    client_id,
                    audio_id,
                    model,
                    fabric,
                    type,
                    quantity,
                    deadline,
                    priority,
                    total_value,
                    paid,
                    stock_reserved,
                    notes,
                    current_stage,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    order.client_id,
                    order.audio_id if order.audio_id else None,
                    order.model,
                    order.fabric,
                    order.type,
                    order.quantity,
                    order.deadline,
                    order.priority,
                    order.total_value,
                    order.paid,
                    order.stock_reserved,
                    order.notes,
                    order.current_stage,
                    order.status,
                ),
            )

            order_id = int(cursor.lastrowid)

            for item in order.items:
                cursor.execute(
                    """
                    INSERT INTO order_items (order_id, size, gender, quantity)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        order_id,
                        item.size,
                        item.gender,
                        item.quantity,
                    ),
                )

            for stage_name in ORDER_STAGES:
                cursor.execute(
                    """
                    INSERT INTO order_stages (order_id, stage_name, status)
                    VALUES (?, ?, ?)
                    """,
                    (
                        order_id,
                        stage_name,
                        "Concluído" if stage_name == "Recepção" else "Em espera",
                    ),
                )

            connection.commit()
            return order_id
        finally:
            connection.close()

    def mark_stock_withdrawn(self, order_id: int) -> None:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE orders
                SET
                    stock_withdrawn = 1,
                    withdrawn_at = ?
                WHERE id = ?
                """,
                (
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    order_id,
                ),
            )

            connection.commit()

        finally:
            connection.close()


    def update_order(self, order: OrderModel) -> None:
        if not order.id:
            return

        connection = get_connection()
        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE orders
                SET
                    client_id = ?,
                    audio_id = ?,
                    model = ?,
                    fabric = ?,
                    type = ?,
                    quantity = ?,
                    deadline = ?,
                    priority = ?,
                    total_value = ?,
                    paid = ?,
                    stock_reserved = ?,
                    notes = ?
                WHERE id = ?
                """,
                (
                    order.client_id,
                    order.audio_id if order.audio_id else None,
                    order.model,
                    order.fabric,
                    order.type,
                    order.quantity,
                    order.deadline,
                    order.priority,
                    order.total_value,
                    order.paid,
                    order.stock_reserved,
                    order.notes,
                    order.id,
                ),
            )
            
            cursor.execute(
                "DELETE FROM order_items WHERE order_id = ?",
                (order.id,),
            )

            for item in order.items:
                cursor.execute(
                    """
                    INSERT INTO order_items (order_id, size, gender, quantity)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        order.id,
                        item.size,
                        item.gender,
                        item.quantity,
                    ),
                )

            connection.commit()
        finally:
            connection.close()


    def list_orders(self) -> List[OrderModel]:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT
                    o.id,
                    o.client_id,
                    o.audio_id,
                    o.status,
                    c.name AS client_name,
                    c.phone AS client_phone,
                    c.city AS client_city,
                    o.model,
                    o.fabric,
                    o.type,
                    o.quantity,
                    o.deadline,
                    o.priority,
                    o.total_value,
                    o.paid,
                    o.stock_reserved,
                    o.stock_withdrawn,
                    o.withdrawn_at,
                    o.notes,
                    o.current_stage,
                    o.created_at
                FROM orders o
                LEFT JOIN clients c ON c.id = o.client_id
                ORDER BY o.created_at DESC, o.id DESC
                """
            )
            rows = cursor.fetchall()

            return [
                OrderModel(
                    id=row["id"],
                    audio_id=row["audio_id"],
                    client_id=row["client_id"],
                    client_name=row["client_name"],
                    model=row["model"],
                    fabric=row["fabric"],
                    type=row["type"],
                    stock_reserved=row["stock_reserved"],
                    stock_withdrawn=row["stock_withdrawn"],
                    quantity=row["quantity"],
                    deadline=row["deadline"],
                    priority=row["priority"],
                    total_value=row["total_value"],
                    paid=row["paid"],
                    notes=row["notes"],
                    current_stage=row["current_stage"],
                    status=row["status"],
                    created_at=row["created_at"],
                    withdrawn_at=row["withdrawn_at"],
                )
                for row in rows
            ]
        finally:
            connection.close()

    def get_order_by_id(self, order_id: int) -> Optional[OrderModel]:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    o.id,
                    o.client_id,
                    o.audio_id,
                    c.name AS client_name,
                    c.phone AS client_phone,
                    c.city AS client_city,
                    o.model,
                    o.fabric,
                    o.type,
                    o.stock_reserved,
                    o.stock_withdrawn,
                    o.withdrawn_at,
                    o.quantity,
                    o.deadline,
                    o.priority,
                    o.total_value,
                    o.paid,
                    o.status,
                    o.notes,
                    o.current_stage,
                    o.created_at
                FROM orders o
                LEFT JOIN clients c ON c.id = o.client_id
                WHERE o.id = ?
                """,
                (order_id,),
            )

            row = cursor.fetchone()

            if not row:
                return None

            items = self.list_order_items(
                order_id,
                connection=connection
            )

            return OrderModel(
                id=row["id"],
                audio_id=row["audio_id"] if row["audio_id"] else None,
                client_id=row["client_id"],
                client_name=row["client_name"],
                client_phone=row["client_phone"],
                client_city=row["client_city"],
                model=row["model"],
                stock_reserved=row["stock_reserved"],
                stock_withdrawn=row["stock_withdrawn"],
                withdrawn_at=row["withdrawn_at"],
                fabric=row["fabric"],
                type=row["type"],
                quantity=row["quantity"],
                deadline=row["deadline"],
                priority=row["priority"],
                total_value=row["total_value"],
                paid=row["paid"],
                notes=row["notes"],
                current_stage=row["current_stage"],
                status=row["status"],
                created_at=row["created_at"],
                items=items,
            )

        finally:
            connection.close()

    def list_order_items(
        self,
        order_id: int,
        connection=None,
    ) -> list[OrderItemModel]:
        owns_connection = connection is None
        if owns_connection:
            connection = get_connection()

        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, order_id, size, gender, quantity
                FROM order_items
                WHERE order_id = ?
                ORDER BY id ASC
                """,
                (order_id,),
            )
            rows = cursor.fetchall()

            return [
                OrderItemModel(
                    id=row["id"],
                    order_id=row["order_id"],
                    size=row["size"],
                    gender=row["gender"],
                    quantity=row["quantity"],
                )
                for row in rows
            ]
        finally:
            if owns_connection:
                connection.close()

    def create_client_if_needed(
        self,
        client_name: Optional[str],
        phone: Optional[str] = None,
        city: Optional[str] = None,
    ) -> Optional[int]:
        if not client_name:
            return None

        connection = get_connection()
        try:
            cursor = connection.cursor()

            cursor.execute(
                "SELECT id, phone, city FROM clients WHERE name = ? LIMIT 1",
                (client_name.strip(),),
            )
            existing = cursor.fetchone()

            if existing:
                client_id = int(existing["id"])

                cursor.execute(
                    """
                    UPDATE clients
                    SET phone = COALESCE(NULLIF(?, ''), phone),
                        city = COALESCE(NULLIF(?, ''), city)
                    WHERE id = ?
                    """,
                    (
                        phone.strip() if phone else "",
                        city.strip() if city else "",
                        client_id,
                    ),
                )
                connection.commit()
                return client_id

            cursor.execute(
                """
                INSERT INTO clients (name, phone, city)
                VALUES (?, ?, ?)
                """,
                (
                    client_name.strip(),
                    phone.strip() if phone else None,
                    city.strip() if city else None,
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)
        finally:
            connection.close()


    def list_order_stages(self, order_id: int) -> list[dict]:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                SELECT id, stage_name, status, notes, responsible, started_at, finished_at
                FROM order_stages
                WHERE order_id = ?
                ORDER BY id ASC
                """,
                (order_id,),
            )
            rows = cursor.fetchall()

            return [
                {
                    "id": row["id"],
                    "stage_name": row["stage_name"],
                    "status": row["status"],
                    "notes": row["notes"],
                    "responsible": row["responsible"],
                    "started_at": row["started_at"],
                    "finished_at": row["finished_at"],
                }
                for row in rows
            ]
        finally:
            connection.close()

    def update_order_stage(self, order_id: int, new_stage: str) -> None:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE orders
                SET current_stage = ?
                WHERE id = ?
                """,
                (new_stage, order_id),
            )

            # Etapas anteriores à atual ficam concluídas.
            current_index = ORDER_STAGES.index(new_stage)

            for index, stage_name in enumerate(ORDER_STAGES):

                if index < current_index:
                    status = "Concluído"

                elif index == current_index:
                    status = "Em produção"

                else:
                    status = "Em espera"

                cursor.execute(
                    """
                    UPDATE order_stages
                    SET status = ?
                    WHERE order_id = ?
                    AND stage_name = ?
                    """,
                    (
                        status,
                        order_id,
                        stage_name,
                    ),
                )

            connection.commit()

        finally:
            connection.close()

    def update_stage_notes(self, order_id: int, stage_name: str, notes: str) -> None:
        connection = get_connection()
        try:
            cursor = connection.cursor()
            cursor.execute(
                """
                UPDATE order_stages
                SET notes = ?
                WHERE order_id = ? AND stage_name = ?
                """,
                (notes, order_id, stage_name),
            )
            connection.commit()
        finally:
            connection.close()

    def mark_stock_reserved(
        self,
        order_id: int
    ):
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE orders
                SET stock_reserved = 1
                WHERE id = ?
                """,
                (order_id,)
            )

            connection.commit()

        finally:
            connection.close()

    def unmark_stock_reserved(
        self,
        order_id: int
    ):
        
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE orders
                SET stock_reserved = 0
                WHERE id = ?
                """,
                (order_id,)
            )

            connection.commit()

        finally:
            connection.close()

    def update_status(
        self,
        order_id: int,
        status: str
    ):
        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                UPDATE orders
                SET status = ?
                WHERE id = ?
                """,
                (
                    status,
                    order_id
                )
            )

            connection.commit()

        finally:
            connection.close()

    def create_status_history(
        self,
        order_id: int,
        old_status: str | None,
        new_status: str,
        notes: str | None = None
    ):
        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                """
                INSERT INTO order_status_history (
                    order_id,
                    old_status,
                    new_status,
                    notes
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    order_id,
                    old_status,
                    new_status,
                    notes
                )
            )

            connection.commit()

        finally:
            connection.close()

    def delete_order(self, order_id: int) -> None:

        connection = get_connection()

        try:

            cursor = connection.cursor()

            cursor.execute(
                "DELETE FROM order_items WHERE order_id = ?",
                (order_id,)
            )

            cursor.execute(
                "DELETE FROM order_stages WHERE order_id = ?",
                (order_id,)
            )

            cursor.execute(
                "DELETE FROM attachments WHERE order_id = ?",
                (order_id,)
            )

            cursor.execute(
                "DELETE FROM generated_messages WHERE order_id = ?",
                (order_id,)
            )

            cursor.execute(
                "DELETE FROM order_status_history WHERE order_id = ?",
                (order_id,)
            )

            cursor.execute(
                "DELETE FROM order_stock_reservations WHERE order_id = ?",
                (order_id,)
            )

            cursor.execute(
                "DELETE FROM orders WHERE id = ?",
                (order_id,)
            )

            connection.commit()

        finally:
            connection.close()

    def update_stage(
        self,
        order_id: int,
        stage: str
    ) -> None:

        if stage not in ORDER_STAGES:
            raise ValueError(
                "Etapa de produção inválida."
            )

        self.update_order_stage(
            order_id,
            stage,
        )