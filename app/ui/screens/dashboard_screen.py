import customtkinter as ctk

from app.services.order_service import OrderService


class DashboardScreen(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.order_service = OrderService()

        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.orders = self.order_service.list_orders()
        self.upcoming_orders = self.order_service.list_upcoming_deadline_orders(days=5)
        self.late_orders = self.order_service.list_late_orders()
        self.orders_without_stock = self.order_service.list_orders_without_stock_withdrawn()

        self._build_header()
        self._build_cards()
        self._build_deadline_list()

    def _build_header(self) -> None:
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, columnspan=4, sticky="ew", padx=8, pady=8)
        header_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header_frame,
            text="Dashboard",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 4))

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Visão geral dos pedidos, prazos e pendências operacionais.",
            font=ctk.CTkFont(size=14),
        )
        subtitle.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 16))

    def _build_cards(self) -> None:
        cards = [
            {
                "title": "Pedidos cadastrados",
                "value": str(len(self.orders)),
                "description": "Total de pedidos no sistema.",
            },
            {
                "title": "Próximos 5 dias",
                "value": str(len(self.upcoming_orders)),
                "description": "Pedidos com prazo próximo.",
            },
            {
                "title": "Sem baixa de estoque",
                "value": str(len(self.orders_without_stock)),
                "description": "Pedidos ainda sem baixa.",
            },
            {
                "title": "Atrasados",
                "value": str(len(self.late_orders)),
                "description": "Pedidos com prazo vencido.",
            },
        ]

        for index, card in enumerate(cards):
            info_card = self._create_info_card(
                title=card["title"],
                value=card["value"],
                description=card["description"],
            )
            info_card.grid(row=1, column=index, sticky="nsew", padx=8, pady=8)

    def _build_deadline_list(self) -> None:
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=8, pady=8)
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            list_frame,
            text="Pedidos com prazo nos próximos 5 dias",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        scroll = ctk.CTkScrollableFrame(list_frame)
        scroll.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        scroll.grid_columnconfigure(0, weight=1)

        if not self.upcoming_orders:
            label = ctk.CTkLabel(
                scroll,
                text="Nenhum pedido com prazo nos próximos 5 dias.",
                font=ctk.CTkFont(size=14),
            )
            label.grid(row=0, column=0, sticky="w", padx=12, pady=12)
            return

        for index, order in enumerate(self.upcoming_orders):
            row = self._create_order_row(scroll, order)
            row.grid(row=index, column=0, sticky="ew", padx=8, pady=6)

    def _create_order_row(self, master, order) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(master)
        frame.grid_columnconfigure(0, weight=1)

        stock_text = "Estoque baixado" if order.stock_withdrawn else "Sem baixa de estoque"

        title = ctk.CTkLabel(
            frame,
            text=order.client_name or "Sem cliente",
            font=ctk.CTkFont(size=17, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=14, pady=(12, 4))

        details = ctk.CTkLabel(
            frame,
            text=(
                f"Prazo: {order.deadline or 'Sem prazo'} | "
                f"Etapa: {order.current_stage or 'Recepção'} | "
                f"{stock_text}"
            ),
            font=ctk.CTkFont(size=13),
        )
        details.grid(row=1, column=0, sticky="w", padx=14, pady=(0, 12))

        priority = ctk.CTkLabel(
            frame,
            text=order.priority or "Sem prioridade",
            fg_color=self._get_priority_color(order.priority),
            corner_radius=8,
            padx=10,
            pady=5,
        )
        priority.grid(row=0, column=1, rowspan=2, padx=14, pady=12, sticky="e")

        return frame

    def _create_info_card(self, title: str, value: str, description: str) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self)
        frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=15, weight="bold"),
        )
        title_label.grid(row=0, column=0, sticky="w", padx=14, pady=(14, 6))

        value_label = ctk.CTkLabel(
            frame,
            text=value,
            font=ctk.CTkFont(size=32, weight="bold"),
        )
        value_label.grid(row=1, column=0, sticky="w", padx=14, pady=2)

        description_label = ctk.CTkLabel(
            frame,
            text=description,
            justify="left",
            font=ctk.CTkFont(size=12),
        )
        description_label.grid(row=2, column=0, sticky="w", padx=14, pady=(4, 14))

        return frame

    def _get_priority_color(self, priority: str | None) -> str:
        colors = {
            "Baixa": "#9CA3AF",
            "Média": "#60A5FA",
            "Alta": "#F97316",
            "Prioridade Máxima": "#EF4444",
        }
        return colors.get(priority or "", "#9CA3AF")