from datetime import datetime

import customtkinter as ctk

from app.core.constants import ORDER_STAGES, PRIORITIES, PRIORITY_COLORS
from app.services.order_service import OrderService
from app.ui.dialogs.order_form_dialog import OrderFormDialog


class OrdersScreen(ctk.CTkFrame):
    def __init__(self, master, on_open_order=None) -> None:
        super().__init__(master)

        self.order_service = OrderService()
        self.on_open_order = on_open_order

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_filters()
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

        buttons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, rowspan=2, padx=16, pady=16, sticky="e")

        self.new_button = ctk.CTkButton(
            buttons_frame,
            text="Novo pedido",
            command=self._open_new_order_dialog,
        )
        self.new_button.grid(row=0, column=0, padx=(0, 8), pady=0)

        self.reload_button = ctk.CTkButton(
            buttons_frame,
            text="Atualizar lista",
            command=self.refresh_orders,
        )
        self.reload_button.grid(row=0, column=1, padx=0, pady=0)

    def _build_filters(self) -> None:
        filters_frame = ctk.CTkFrame(self)
        filters_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        filters_frame.grid_columnconfigure(0, weight=2)
        filters_frame.grid_columnconfigure(1, weight=1)
        filters_frame.grid_columnconfigure(2, weight=1)
        filters_frame.grid_columnconfigure(3, weight=1)
        filters_frame.grid_columnconfigure(4, weight=1)

        self.search_entry = ctk.CTkEntry(
            filters_frame,
            placeholder_text="Buscar por cliente...",
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=8, pady=12)
        self.search_entry.bind("<KeyRelease>", lambda _event: self.refresh_orders())

        self.stage_filter = ctk.CTkOptionMenu(
            filters_frame,
            values=["Todas as etapas"] + ORDER_STAGES,
            command=lambda _value: self.refresh_orders(),
        )
        self.stage_filter.grid(row=0, column=1, sticky="ew", padx=8, pady=12)
        self.stage_filter.set("Todas as etapas")

        self.priority_filter = ctk.CTkOptionMenu(
            filters_frame,
            values=["Todas prioridades"] + PRIORITIES,
            command=lambda _value: self.refresh_orders(),
        )
        self.priority_filter.grid(row=0, column=2, sticky="ew", padx=8, pady=12)
        self.priority_filter.set("Todas prioridades")

        self.stock_filter = ctk.CTkOptionMenu(
            filters_frame,
            values=["Todos", "Estoque baixado", "Sem baixa de estoque"],
            command=lambda _value: self.refresh_orders(),
        )
        self.stock_filter.grid(row=0, column=3, sticky="ew", padx=8, pady=12)
        self.stock_filter.set("Todos")

        self.late_filter = ctk.CTkOptionMenu(
            filters_frame,
            values=["Todos prazos", "Apenas atrasados", "Não atrasados"],
            command=lambda _value: self.refresh_orders(),
        )
        self.late_filter.grid(row=0, column=4, sticky="ew", padx=8, pady=12)
        self.late_filter.set("Todos prazos")

        clear_button = ctk.CTkButton(
            filters_frame,
            text="Limpar filtros",
            command=self._clear_filters,
        )
        clear_button.grid(row=0, column=5, sticky="ew", padx=8, pady=12)

    def _build_list_container(self) -> None:
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=8)
        self.list_frame.grid_columnconfigure(0, weight=1)

    def refresh_orders(self) -> None:
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        orders = self._apply_filters(self.order_service.list_orders())

        if not orders:
            placeholder = ctk.CTkLabel(
                self.list_frame,
                text="Nenhum pedido encontrado com os filtros atuais.",
                font=ctk.CTkFont(size=15),
            )
            placeholder.grid(row=0, column=0, padx=16, pady=16, sticky="w")
            return

        for index, order in enumerate(orders):
            card = self._create_order_card(order)
            card.grid(row=index, column=0, sticky="ew", padx=8, pady=8)

    def _apply_filters(self, orders):
        search = self.search_entry.get().strip().lower()
        stage = self.stage_filter.get()
        priority = self.priority_filter.get()
        stock = self.stock_filter.get()
        late = self.late_filter.get()

        filtered = []

        for order in orders:
            if search:
                client_name = (order.client_name or "").lower()
                if search not in client_name:
                    continue

            if stage != "Todas as etapas":
                if order.current_stage != stage:
                    continue

            if priority != "Todas prioridades":
                if order.priority != priority:
                    continue

            if stock == "Estoque baixado" and not order.stock_withdrawn:
                continue

            if stock == "Sem baixa de estoque" and order.stock_withdrawn:
                continue

            is_late = self._is_order_late(order)

            if late == "Apenas atrasados" and not is_late:
                continue

            if late == "Não atrasados" and is_late:
                continue

            filtered.append(order)

        return filtered

    def _is_order_late(self, order) -> bool:
        if not order.deadline:
            return False

        if order.current_stage == "Retirada":
            return False

        try:
            deadline_date = datetime.strptime(order.deadline, "%Y-%m-%d").date()
        except ValueError:
            return False

        return deadline_date < datetime.now().date()

    def _create_order_card(self, order) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.list_frame)
        frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            frame,
            text=order.client_name or "Sem cliente",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        stock_text = "Estoque baixado" if order.stock_withdrawn else "Sem baixa de estoque"
        late_text = " | ATRASADO" if self._is_order_late(order) else ""

        details = ctk.CTkLabel(
            frame,
            text=(
                f"Modelo: {order.model or 'Não informado'}\n"
                f"Tecido: {order.fabric or 'Não informado'}\n"
                f"Quantidade: {order.quantity or 0}\n"
                f"Prazo: {order.deadline or 'Sem prazo'}{late_text}\n"
                f"Etapa atual: {order.current_stage or 'Recepção'}\n"
                f"{stock_text}"
            ),
            justify="left",
            font=ctk.CTkFont(size=14),
        )
        details.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 12))

        priority = order.priority or "Baixa"
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

        open_button = ctk.CTkButton(
            frame,
            text="Abrir pedido",
            command=lambda oid=order.id: self._open_order(oid),
        )
        open_button.grid(row=1, column=1, padx=16, pady=(0, 12), sticky="e")

        return frame

    def _clear_filters(self) -> None:
        self.search_entry.delete(0, "end")
        self.stage_filter.set("Todas as etapas")
        self.priority_filter.set("Todas prioridades")
        self.stock_filter.set("Todos")
        self.late_filter.set("Todos prazos")
        self.refresh_orders()

    def _open_order(self, order_id: int) -> None:
        if callable(self.on_open_order):
            self.on_open_order(order_id)

    def _open_new_order_dialog(self) -> None:
        OrderFormDialog(self, on_save=self._handle_order_created)

    def _handle_order_created(self, order_id: int) -> None:
        self.refresh_orders()
        if callable(self.on_open_order):
            self.on_open_order(order_id)


