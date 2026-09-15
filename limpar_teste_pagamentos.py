from app.repositories.payment_repository import PaymentRepository


payment_repository = PaymentRepository()

payment_ids = [1, 2, 3]

for payment_id in payment_ids:
    payment_repository.delete_payment(payment_id)
    print(f"Pagamento #{payment_id} removido.")

print("\nPagamentos de teste removidos.")