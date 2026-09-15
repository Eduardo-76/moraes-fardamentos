from typing import List

from app.models.payment_model import PaymentModel
from app.repositories.payment_repository import PaymentRepository


class PaymentService:
    PAYMENT_METHODS = (
        "Pix",
        "Dinheiro",
        "Cartão",
    )

    PAYMENT_STATUS_PENDING = "Pendente"
    PAYMENT_STATUS_PARTIAL = "Parcial"
    PAYMENT_STATUS_PAID = "Pago"

    def __init__(self) -> None:
        self.repository = PaymentRepository()

    def register_payment(
        self,
        order_id: int,
        amount: float,
        payment_method: str,
        total_value: float,
        notes: str | None = None,
    ) -> int:
        if order_id <= 0:
            raise ValueError("Pedido inválido.")

        if total_value < 0:
            raise ValueError(
                "O valor final do pedido não pode ser negativo."
            )

        if amount <= 0:
            raise ValueError(
                "O valor do pagamento deve ser maior que zero."
            )

        if payment_method not in self.PAYMENT_METHODS:
            raise ValueError(
                "Forma de pagamento inválida."
            )

        total_paid = self.get_total_paid(order_id)

        remaining = total_value - total_paid

        if remaining <= 0:
            raise ValueError(
                "Este pedido já está totalmente pago."
            )

        if amount > remaining:
            raise ValueError(
                f"O pagamento não pode ser maior que o valor restante "
                f"de R$ {remaining:.2f}."
            )

        payment = PaymentModel(
            order_id=order_id,
            amount=amount,
            payment_method=payment_method,
            notes=notes,
        )

        return self.repository.create_payment(payment)

    def list_payments(
        self,
        order_id: int,
    ) -> List[PaymentModel]:
        return self.repository.list_payments(order_id)

    def get_total_paid(
        self,
        order_id: int,
    ) -> float:
        return self.repository.get_total_paid(order_id)

    def get_remaining_amount(
        self,
        order_id: int,
        total_value: float,
    ) -> float:
        total_paid = self.get_total_paid(order_id)

        remaining = total_value - total_paid

        if remaining < 0.01:
            return 0.0

        return remaining

    def get_payment_status(
        self,
        order_id: int,
        total_value: float,
    ) -> str:
        total_paid = self.get_total_paid(order_id)

        if total_paid <= 0:
            return self.PAYMENT_STATUS_PENDING

        if total_paid < total_value:
            return self.PAYMENT_STATUS_PARTIAL

        return self.PAYMENT_STATUS_PAID