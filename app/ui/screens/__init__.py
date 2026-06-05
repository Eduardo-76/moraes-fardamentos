import customtkinter as ctk

from app.core.constants import PRIORITY_COLORS
from app.services.order_service import OrderService


class OrdersScreen(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.order_service = OrderService()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_list_container()
        self.refresh_orders()

    def _build_header(self) -> None:
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header_frame,
            text="Pedidos",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 4))

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Lista geral de pedidos cadastrados no sistema.",
            font=ctk.CTkFont(size=14),
        )
        subtitle.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 12))

        self.reload_button = ctk.CTkButton(
            header_frame,
            text="Atualizar lista",
            command=self.refresh_orders,
        )
        self.reload_button.grid(row=0, column=1, rowspan=2, padx=16, pady=16)

    def _build_list_container(self) -> None:
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        self.list_frame.grid_columnconfigure(0, weight=1)

    def refresh_orders(self) -> None:
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        orders = self.order_service.list_orders()

        if not orders:
            placeholder = ctk.CTkLabel(
                self.list_frame,
                text="Nenhum pedido encontrado.",
                font=ctk.CTkFont(size=15),
            )
            placeholder.grid(row=0, column=0, padx=16, pady=16, sticky="w")
            return

        for index, order in enumerate(orders):
            card = self._create_order_card(
                client_name=order.client_name or "Sem cliente",
                model=order.model or "Não informado",
                fabric=order.fabric or "Não informado",
                quantity=str(order.quantity or 0),
                deadline=order.deadline or "Sem prazo",
                priority=order.priority or "Baixa",
                stage=order.current_stage or "Recepção",
            )
            card.grid(row=index, column=0, sticky="ew", padx=8, pady=8)

    def _create_order_card(
        self,
        client_name: str,
        model: str,
        fabric: str,
        quantity: str,
        deadline: str,
        priority: str,
        stage: str,
    ) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.list_frame)
        frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            frame,
            text=client_name,
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        details = ctk.CTkLabel(
            frame,
            text=(
                f"Modelo: {model}\n"
                f"Tecido: {fabric}\n"
                f"Quantidade: {quantity}\n"
                f"Prazo: {deadline}\n"
                f"Etapa atual: {stage}"
            ),
            justify="left",
            font=ctk.CTkFont(size=14),
        )
        details.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 12))

        priority_color = PRIORITY_COLORS.get(priority, "#9CA3AF")

        priority_label = ctk.CTkLabel(
            frame,
            text=f"Prioridade: {priority}",
            fg_color=priority_color,
            corner_radius=8,
            padx=10,
            pady=6,
        )
        priority_label.grid(row=0, column=1, padx=16, pady=(16, 8), sticky="e")

        return frame