from datetime import datetime
from typing import List

from app.core.database import get_connection
from app.models.payment_model import PaymentModel


class PaymentRepository:

    def create_payment(self, payment: PaymentModel) -> int:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            paid_at = payment.paid_at

            if not paid_at:
                paid_at = datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

            cursor.execute(
                """
                INSERT INTO payments (
                    order_id,
                    amount,
                    payment_method,
                    paid_at,
                    notes
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    payment.order_id,
                    payment.amount,
                    payment.payment_method,
                    paid_at,
                    payment.notes,
                ),
            )

            payment_id = int(cursor.lastrowid)

            connection.commit()

            return payment_id

        finally:
            connection.close()

    def list_payments(self, order_id: int) -> List[PaymentModel]:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT
                    id,
                    order_id,
                    amount,
                    payment_method,
                    paid_at,
                    notes
                FROM payments
                WHERE order_id = ?
                ORDER BY paid_at ASC, id ASC
                """,
                (order_id,),
            )

            rows = cursor.fetchall()

            return [
                PaymentModel(
                    id=row["id"],
                    order_id=row["order_id"],
                    amount=row["amount"],
                    payment_method=row["payment_method"],
                    paid_at=row["paid_at"],
                    notes=row["notes"],
                )
                for row in rows
            ]

        finally:
            connection.close()

    def get_total_paid(self, order_id: int) -> float:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                SELECT COALESCE(SUM(amount), 0)
                FROM payments
                WHERE order_id = ?
                """,
                (order_id,),
            )

            result = cursor.fetchone()

            return float(result[0] or 0)

        finally:
            connection.close()

    def delete_payment(self, payment_id: int) -> None:
        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute(
                """
                DELETE FROM payments
                WHERE id = ?
                """,
                (payment_id,),
            )

            connection.commit()

        finally:
            connection.close()