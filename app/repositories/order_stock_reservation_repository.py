from app.core.database import get_connection
from app.models.order_stock_reservation_model import (
    OrderStockReservationModel,
)

class OrderStockReservationRepository:
    def create_reservation(
        self,
        reservation: OrderStockReservationModel
    ):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO order_stock_reservations (
                order_id,
                stock_entry_id,
                stock_item_id,
                quantity,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                reservation.order_id,
                reservation.stock_entry_id,
                reservation.stock_item_id,
                reservation.quantity,
                reservation.status
            )
        )
        conn.commit()
        cursor.close()
        conn.close()

            
    def list_by_order(
        self,
        order_id: int
    ):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT *
            FROM order_stock_reservations
            WHERE order_id = ?
            ORDER BY id ASC
            """,
            (order_id,)
        )
        reservations = cursor.fetchall()
        cursor.close()
        conn.close()
        return reservations

    def list_by_stock(
        self,
        stock_entry_id: int
    ):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                r.*,
                c.name AS client_name,
                sei.size,
                sei.gender
            FROM order_stock_reservations r

            INNER JOIN orders o
                ON o.id = r.order_id

            INNER JOIN clients c
                ON c.id = o.client_id

            INNER JOIN stock_entry_items sei
                ON sei.id = r.stock_item_id

            WHERE r.stock_entry_id = ?
            AND r.status = 'RESERVED'

            ORDER BY r.id ASC
            """,
            (stock_entry_id,)
        )

        reservations = cursor.fetchall()

        cursor.close()
        conn.close()

        return reservations
    
    def cancel_reservation(
        self,
        reservation_id: int
    ):
        conn = get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE order_stock_reservations
                SET
                    status = 'CANCELLED',
                    cancelled_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (reservation_id,)
            )

            conn.commit()

        finally:
            conn.close()


    def get_by_id(
        self,
        reservation_id: int
    ):
        conn = get_connection()

        try:

            conn.row_factory = lambda cursor, row: {
                col[0]: row[idx]
                for idx, col in enumerate(cursor.description)
            }

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM order_stock_reservations
                WHERE id = ?
                """,
                (reservation_id,)
            )

            return cursor.fetchone()

        finally:
            conn.close()

    def has_active_reservations(
        self,
        order_id: int
    ):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM order_stock_reservations
            WHERE order_id = ?
            AND status = 'RESERVED'
            """,
            (order_id,)
        )

        count = cursor.fetchone()[0]

        cursor.close()
        conn.close()

        return count > 0
    
    def list_active_by_order(
        self,
        order_id: int
    ):
        conn = get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT *
                FROM order_stock_reservations
                WHERE order_id = ?
                AND status = 'RESERVED'
                """,
                (order_id,)
            )

            return cursor.fetchall()

        finally:
            conn.close()

    def withdraw_reservation(
        self,
        reservation_id: int
    ):
        conn = get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                UPDATE order_stock_reservations
                SET
                    status = 'WITHDRAWN',
                    withdrawn_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (reservation_id,)
            )

            conn.commit()

        finally:
            conn.close()

