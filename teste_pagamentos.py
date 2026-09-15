from app.services.payment_service import PaymentService


ORDER_ID = 20

payment_service = PaymentService()

payments = payment_service.list_payments(ORDER_ID)

print("\n==============================")
print(f"PAGAMENTOS DO PEDIDO #{ORDER_ID}")
print("==============================")

if not payments:
    print("Nenhum pagamento encontrado.")
else:
    for payment in payments:
        print(
            f"ID: {payment.id} | "
            f"Valor: R$ {payment.amount:.2f} | "
            f"Forma: {payment.payment_method} | "
            f"Data: {payment.paid_at or 'Não informada'}"
        )

total = payment_service.get_total_paid(ORDER_ID)

print("==============================")
print(f"TOTAL: R$ {total:.2f}")
print("==============================")