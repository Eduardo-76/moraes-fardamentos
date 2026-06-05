from typing import List, Optional
from datetime import datetime, timedelta
from app.core.constants import ORDER_STAGES
from app.models.order_model import OrderItemModel, OrderModel
from app.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self) -> None:
        self.repository = OrderRepository()

    def create_order(
        self,
        client_name: Optional[str],
        client_phone: Optional[str],
        client_city: Optional[str],
        model: Optional[str],
        fabric: Optional[str],
        order_type: Optional[str],
        quantity: Optional[int],
        deadline: Optional[str],
        priority: Optional[str],
        total_value: Optional[float],
        notes: Optional[str],
        items: Optional[list[dict]] = None,
        audio_id: Optional[int] = None,
    ) -> int:
        client_id = self.repository.create_client_if_needed(
            client_name=client_name,
            phone=client_phone,
            city=client_city,
        )
        order_items: list[OrderItemModel] = []
        for item in items or []:
            order_items.append(
                OrderItemModel(
                    size=item.get("size"),
                    gender=item.get("gender"),
                    quantity=item.get("quantity"),
                )
            )

        order = OrderModel(
            client_id=client_id,
            client_name=client_name,
            model=model,
            fabric=fabric,
            type=order_type,
            quantity=quantity,
            deadline=deadline,
            priority=priority,
            total_value=total_value,
            notes=notes,
            current_stage="Recepção",
            items=order_items,
            audio_id=audio_id,
        )

        return self.repository.create_order(order)

    def list_orders(self) -> List[OrderModel]:
        return self.repository.list_orders()

    def mark_stock_withdrawn(self, order_id: int) -> None:
        self.repository.mark_stock_withdrawn(order_id)

    def get_order_by_id(self, order_id: int) -> Optional[OrderModel]:
        return self.repository.get_order_by_id(order_id)

    def list_order_stages(self, order_id: int) -> list[dict]:
        return self.repository.list_order_stages(order_id)

    def move_to_next_stage(self, order_id: int) -> None:
        order = self.get_order_by_id(order_id)
        if not order or not order.current_stage:
            return

        if order.current_stage not in ORDER_STAGES:
            return

        current_index = ORDER_STAGES.index(order.current_stage)
        if current_index >= len(ORDER_STAGES) - 1:
            return

        new_stage = ORDER_STAGES[current_index + 1]
        self.repository.update_order_stage(order_id, new_stage)

    def move_to_previous_stage(self, order_id: int) -> None:
        order = self.get_order_by_id(order_id)
        if not order or not order.current_stage:
            return

        if order.current_stage not in ORDER_STAGES:
            return

        current_index = ORDER_STAGES.index(order.current_stage)
        if current_index <= 0:
            return

        new_stage = ORDER_STAGES[current_index - 1]
        self.repository.update_order_stage(order_id, new_stage)

    def save_stage_notes(self, order_id: int, stage_name: str, notes: str) -> None:
        self.repository.update_stage_notes(order_id, stage_name, notes)

    def generate_stage_message(self, order_id: int, sector: str) -> str:
        order = self.get_order_by_id(order_id)
        if not order:
            return "Pedido não encontrado."

        items_text = self._build_items_text(order)

        base = (
            f"Cliente: {order.client_name or 'Não informado'}\n"
            f"Modelo: {order.model or 'Não informado'}\n"
            f"Tipo: {order.type or 'Não informado'}\n"
            f"Tecido: {order.fabric or 'Não informado'}\n"
            f"Quantidade total: {order.quantity or 0}\n"
            f"{items_text}\n"
            f"Prazo: {order.deadline or 'Não informado'}\n"
            f"Etapa atual: {order.current_stage or 'Recepção'}"
        )

        templates = {
            "Recepção": (
                f"{base}\n\n"
                "Verificar pagamento de 50%, confirmação de arte e modelo antes de seguir."
            ),
            "Design": (
                f"{base}\n\n"
                "Verificar arte, ajustes pendentes e exportação do material."
            ),
            "Impressão": (
                f"{base}\n\n"
                "Verificar impressão e retirada do material impresso."
            ),
            "Estamparia": (
                f"{base}\n\n"
                "Pedido pronto para estamparia/serigrafia/DTF. Conferir material e iniciar produção."
            ),
            "Costura": (
                f"{base}\n\n"
                "Encaminhar para costura e conferir possíveis faltas na peça."
            ),
            "Cliente": (
                f"Olá, {order.client_name or 'cliente'}! "
                f"Seu pedido de {order.quantity or 0} peça(s) está em andamento. "
                f"Prazo atual: {order.deadline or 'não informado'}."
            ),
        }

        return templates.get(sector, base)

    def build_order_command_text(self, order_id: int) -> str:
        order = self.get_order_by_id(order_id)
        if not order:
            return "Pedido não encontrado."

        items_text = self._build_items_text(order)

        return (
            f"Cliente: {order.client_name or 'Não informado'}\n"
            f"Origem: {'Áudio' if order.audio_id else 'Manual'}\n"
            f"Contato: {order.client_phone or 'Não informado'}\n"
            f"Cidade: {order.client_city or 'Não informado'}\n"
            f"Modelo: {order.model or 'Não informado'}\n"
            f"Tipo: {order.type or 'Não informado'}\n"
            f"Tecido: {order.fabric or 'Não informado'}\n\n"
            f"Quantidade total: {order.quantity or 0}\n"
            f"{items_text}\n\n"
            f"Prazo: {order.deadline or 'Não informado'}\n"
            f"Prioridade: {order.priority or 'Não informado'}\n"
            f"Etapa atual: {order.current_stage or 'Recepção'}\n"
            f"Estoque baixado: {'Sim' if order.stock_withdrawn else 'Não'}\n"
            f"Observação: {order.notes or 'Nenhuma'}"
        )

    def _build_items_text(self, order: OrderModel) -> str:
        if not order.items:
            return "- Sem detalhamento de tamanhos"

        lines = []
        for item in order.items:
            quantity = item.quantity or 0
            size = item.size or "Sem tamanho"
            gender = item.gender or "Sem categoria"
            lines.append(f"- {quantity} {size} - {gender}")

        return "\n".join(lines)

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



    def create_sample_orders_if_empty(self) -> None:
        existing_orders = self.list_orders()
        if existing_orders:
            return

        self.create_order(
            client_name="João Silva",
            client_phone="86999990000",
            client_city="Piracuruca",
            audio_id=None,
            model="Gola Polo",
            fabric="PP",
            order_type="Estampada Toda",
            quantity=30,
            deadline="2026-04-25",
            priority="Alta",
            total_value=900.0,
            notes="Pedido de teste inicial",
            items=[
                {"size": "M", "gender": "Masculina", "quantity": 10},
                {"size": "GG", "gender": "Masculina", "quantity": 10},
                {"size": "M", "gender": "Feminina", "quantity": 5},
                {"size": "G", "gender": "Infantil", "quantity": 5},
            ],
        )

        self.create_order(
            client_name="Escola Municipal Sol Nascente",
            client_phone="8633334444",
            client_city="Piripiri",
            model="Camisa Escolar",
            fabric="Dry Fit",
            order_type="Frente e costas",
            quantity=120,
            deadline="2026-04-27",
            priority="Prioridade Máxima",
            total_value=4200.0,
            notes="Entrega parcial pode ser necessária",
            items=[
                {"size": "PP", "gender": "Infantil", "quantity": 20},
                {"size": "P", "gender": "Infantil", "quantity": 30},
                {"size": "M", "gender": "Infantil", "quantity": 35},
                {"size": "G", "gender": "Infantil", "quantity": 35},
            ],
            audio_id=None,
        )

    def update_order(
        self,
        order_id: int,
        client_name: Optional[str],
        client_phone: Optional[str],
        client_city: Optional[str],
        model: Optional[str],
        fabric: Optional[str],
        order_type: Optional[str],
        quantity: int,
        deadline: Optional[str],
        priority: Optional[str],
        total_value: Optional[float],
        notes: Optional[str],
        items: Optional[list[dict]] = None,
        audio_id: Optional[int] = None,
    ) -> None:
        client_id = self.repository.create_client_if_needed(
            client_name=client_name,
            phone=client_phone,
            city=client_city,
        )

        order_items: list[OrderItemModel] = []
        for item in items or []:
            order_items.append(
                OrderItemModel(
                    size=item.get("size"),
                    gender=item.get("gender"),
                    quantity=item.get("quantity"),
                )
            )

        order = OrderModel(
            client_id=client_id,
            audio_id=audio_id if isinstance(audio_id, int) and audio_id > 0 else None,
            client_name=client_name,
            client_phone=client_phone,
            client_city=client_city,
            model=model,
            fabric=fabric,
            type=order_type,
            quantity=quantity,
            deadline=deadline,
            priority=priority,
            total_value=total_value,
            notes=notes,
            current_stage="Recepção",
            items=order_items,
        )

        self.repository.update_order(order)