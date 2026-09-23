import customtkinter as ctk
from datetime import datetime

from app.services.order_service import OrderService


class WithdrawalsScreen(ctk.CTkFrame):
    def __init__(self, master, on_open_order=None):
        super().__init__(master)

        self.on_open_order = on_open_order
        self.order_service = OrderService()

        self._build_ui()
        self._refresh_withdrawals()

    # ============================================================
    # UI
    # ============================================================

    def _build_ui(self):
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --------------------------------------------------------
        # Cabeçalho
        # --------------------------------------------------------

        header = ctk.CTkFrame(self)
        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=8,
            pady=(0, 8),
        )

        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Retiradas",
            font=ctk.CTkFont(size=26, weight="bold"),
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=16,
            pady=(12, 2),
        )

        ctk.CTkLabel(
            header,
            text="Histórico de pedidos que chegaram à etapa de retirada.",
            font=ctk.CTkFont(size=14),
        ).grid(
            row=1,
            column=0,
            sticky="w",
            padx=16,
            pady=(0, 12),
        )

        # --------------------------------------------------------
        # Filtros
        # --------------------------------------------------------

        filters = ctk.CTkFrame(self)
        filters.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=8,
            pady=(0, 8),
        )

        filters.grid_columnconfigure(0, weight=1)
        filters.grid_columnconfigure(1, weight=1)
        filters.grid_columnconfigure(2, weight=0)
        filters.grid_columnconfigure(3, weight=1)
        filters.grid_columnconfigure(4, weight=1)
        filters.grid_columnconfigure(5, weight=1)

        # Data inicial
        ctk.CTkLabel(
            filters,
            text="Data inicial",
            font=ctk.CTkFont(weight="bold"),
        ).grid(
            row=0,
            column=0,
            sticky="w",
            padx=(10, 6),
            pady=(8, 2),
        )

        self.start_date_entry = ctk.CTkEntry(
            filters,
            placeholder_text="DD/MM/AAAA",
            height=32,
        )
        self.start_date_entry.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(10, 6),
            pady=(0, 10),
        )

        # Data final
        ctk.CTkLabel(
            filters,
            text="Data final",
            font=ctk.CTkFont(weight="bold"),
        ).grid(
            row=0,
            column=1,
            sticky="w",
            padx=6,
            pady=(8, 2),
        )

        self.end_date_entry = ctk.CTkEntry(
            filters,
            placeholder_text="DD/MM/AAAA",
            height=32,
        )
        self.end_date_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=6,
            pady=(0, 10),
        )

        # Até hoje
        self.until_today_var = ctk.BooleanVar(value=False)

        self.until_today_check = ctk.CTkCheckBox(
            filters,
            text="Até hoje",
            variable=self.until_today_var,
            command=self._toggle_until_today,
        )
        self.until_today_check.grid(
            row=1,
            column=2,
            padx=8,
            pady=(0, 10),
        )

        # Status
        ctk.CTkLabel(
            filters,
            text="Status",
            font=ctk.CTkFont(weight="bold"),
        ).grid(
            row=0,
            column=3,
            sticky="w",
            padx=6,
            pady=(8, 2),
        )

        self.status_combo = ctk.CTkComboBox(
            filters,
            values=[
                "Todos",
                "Retirada",
            ],
            height=32,
        )
        self.status_combo.set("Todos")
        self.status_combo.grid(
            row=1,
            column=3,
            sticky="ew",
            padx=6,
            pady=(0, 10),
        )

        # Aplicar
        self.apply_button = ctk.CTkButton(
            filters,
            text="Aplicar filtros",
            height=32,
            command=self._apply_filters,
        )
        self.apply_button.grid(
            row=1,
            column=4,
            sticky="ew",
            padx=6,
            pady=(0, 10),
        )

        # Limpar
        self.clear_button = ctk.CTkButton(
            filters,
            text="Limpar filtros",
            height=32,
            command=self._clear_filters,
        )
        self.clear_button.grid(
            row=1,
            column=5,
            sticky="ew",
            padx=(6, 10),
            pady=(0, 10),
        )

        # --------------------------------------------------------
        # Área principal
        # --------------------------------------------------------

        content = ctk.CTkFrame(self)
        content.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=8,
            pady=(0, 8),
        )

        content.grid_rowconfigure(1, weight=1)
        content.grid_columnconfigure(0, weight=1)

        # --------------------------------------------------------
        # Resumo
        # --------------------------------------------------------

        self.summary_frame = ctk.CTkFrame(content)
        self.summary_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=0,
            pady=(0, 8),
        )

        self.summary_frame.grid_columnconfigure(0, weight=1)
        self.summary_frame.grid_columnconfigure(1, weight=1)
        self.summary_frame.grid_columnconfigure(2, weight=1)

        self.orders_total_label = ctk.CTkLabel(
            self.summary_frame,
            text="Pedidos que chegaram à Retirada: 0",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.orders_total_label.grid(
            row=0,
            column=0,
            padx=8,
            pady=12,
        )

        self.quantity_total_label = ctk.CTkLabel(
            self.summary_frame,
            text="Total de peças: 0",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.quantity_total_label.grid(
            row=0,
            column=1,
            padx=8,
            pady=12,
        )

        self.value_total_label = ctk.CTkLabel(
            self.summary_frame,
            text="Valor total: R$ 0,00",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.value_total_label.grid(
            row=0,
            column=2,
            padx=8,
            pady=12,
        )

        # --------------------------------------------------------
        # Lista
        # --------------------------------------------------------

        self.withdrawals_list = ctk.CTkScrollableFrame(content)
        self.withdrawals_list.grid(
            row=1,
            column=0,
            sticky="nsew",
        )

        self.withdrawals_list.grid_columnconfigure(0, weight=1)

    # ============================================================
    # Datas
    # ============================================================

    def _parse_date(self, value):
        value = value.strip()

        if not value:
            return None

        try:
            return datetime.strptime(
                value,
                "%d/%m/%Y",
            ).date()

        except ValueError:
            return "invalid"

    def _get_period_dates(self):
        start_value = self._parse_date(
            self.start_date_entry.get()
        )

        end_value = self._parse_date(
            self.end_date_entry.get()
        )

        if start_value == "invalid":
            raise ValueError(
                "A data inicial é inválida. "
                "Use o formato DD/MM/AAAA."
            )

        if end_value == "invalid":
            raise ValueError(
                "A data final é inválida. "
                "Use o formato DD/MM/AAAA."
            )

        if self.until_today_var.get():
            end_value = datetime.now().date()

        if start_value and end_value:
            if start_value > end_value:
                raise ValueError(
                    "A data inicial não pode ser maior "
                    "que a data final."
                )

        return start_value, end_value

    # ============================================================
    # Filtros
    # ============================================================

    def _apply_filters(self):
        try:
            self._get_period_dates()

        except ValueError as exc:
            self._show_error(
                "Filtro inválido",
                str(exc),
            )
            return

        self._refresh_withdrawals()

    def _toggle_until_today(self):
        if self.until_today_var.get():
            self.end_date_entry.delete(0, "end")
            self.end_date_entry.insert(
                0,
                datetime.now().strftime("%d/%m/%Y"),
            )

            self.end_date_entry.configure(
                state="disabled"
            )

        else:
            self.end_date_entry.configure(
                state="normal"
            )

    def _clear_filters(self):
        self.start_date_entry.delete(0, "end")
        self.end_date_entry.configure(state="normal")
        self.end_date_entry.delete(0, "end")

        self.until_today_var.set(False)

        self.status_combo.set("Todos")

        self._refresh_withdrawals()

    # ============================================================
    # Dados
    # ============================================================

    def _get_withdrawals(self):
        orders = self.order_service.list_orders()

        start_date, end_date = self._get_period_dates()
        selected_status = self.status_combo.get()

        withdrawals = []

        for order in orders:
            if not order.withdrawn_at:
                continue

            # ----------------------------------------------------
            # Data da chegada à Retirada
            # ----------------------------------------------------

            try:
                withdrawn_datetime = datetime.strptime(
                    order.withdrawn_at,
                    "%Y-%m-%d %H:%M:%S",
                )

                withdrawn_date = withdrawn_datetime.date()

            except (ValueError, TypeError):
                continue

            if start_date and withdrawn_date < start_date:
                continue

            if end_date and withdrawn_date > end_date:
                continue

            # ----------------------------------------------------
            # Status atual
            # ----------------------------------------------------

            if selected_status == "Retirada":
                if order.current_stage != "Retirada":
                    continue

            withdrawals.append(order)

        withdrawals.sort(
            key=lambda order: order.withdrawn_at or "",
            reverse=True,
        )

        return withdrawals

    # ============================================================
    # Atualização
    # ============================================================

    def _refresh_withdrawals(self):
        for widget in self.withdrawals_list.winfo_children():
            widget.destroy()

        try:
            withdrawals = self._get_withdrawals()

        except ValueError as exc:
            self._show_error(
                "Filtro inválido",
                str(exc),
            )
            return

        total_orders = len(withdrawals)

        total_quantity = sum(
            (order.quantity or 0)
            for order in withdrawals
        )

        total_value = sum(
            float(order.total_value or 0)
            for order in withdrawals
        )

        self.orders_total_label.configure(
            text=(
                "Pedidos que chegaram à Retirada: "
                f"{total_orders}"
            )
        )

        self.quantity_total_label.configure(
            text=f"Total de peças: {total_quantity}"
        )

        self.value_total_label.configure(
            text=f"Valor total: {self._format_money(total_value)}"
        )

        if not withdrawals:
            ctk.CTkLabel(
                self.withdrawals_list,
                text="Nenhum pedido encontrado.",
                font=ctk.CTkFont(size=15),
            ).grid(
                row=0,
                column=0,
                padx=20,
                pady=30,
            )
            return

        for row, order in enumerate(withdrawals):
            self._create_withdrawal_card(
                order,
                row,
            )

    # ============================================================
    # Cards
    # ============================================================

    def _create_withdrawal_card(self, order, row):
        card = ctk.CTkFrame(
            self.withdrawals_list,
        )

        card.grid(
            row=row,
            column=0,
            sticky="ew",
            padx=4,
            pady=(0, 8),
        )

        card.grid_columnconfigure(0, weight=1)
        card.grid_columnconfigure(1, weight=0)

        # --------------------------------------------------------
        # Informações
        # --------------------------------------------------------

        info_frame = ctk.CTkFrame(
            card,
            fg_color="transparent",
        )
        info_frame.grid(
            row=0,
            column=0,
            sticky="w",
            padx=14,
            pady=12,
        )

        customer_name = getattr(
            order,
            "client_name",
            None,
        ) or "Cliente não informado"

        withdrawn_at = self._format_withdrawn_at(
            order.withdrawn_at
        )

        model = getattr(
            order,
            "model",
            None,
        ) or "Não informado"

        quantity = order.quantity or 0

        total_value = float(
            order.total_value or 0
        )

        ctk.CTkLabel(
            info_frame,
            text=customer_name,
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
        ).pack(anchor="w")

        ctk.CTkLabel(
            info_frame,
            text=f"Pedido: #{order.id}",
        ).pack(anchor="w")

        ctk.CTkLabel(
            info_frame,
            text=f"Retirada: {withdrawn_at}",
        ).pack(anchor="w")

        ctk.CTkLabel(
            info_frame,
            text=f"Modelo: {model}",
        ).pack(anchor="w")

        ctk.CTkLabel(
            info_frame,
            text=f"Quantidade: {quantity} peças",
        ).pack(anchor="w")

        ctk.CTkLabel(
            info_frame,
            text=f"Valor: {self._format_money(total_value)}",
        ).pack(anchor="w")

        # --------------------------------------------------------
        # Status
        # --------------------------------------------------------

        status = order.current_stage or "Não informado"

        status_label = ctk.CTkLabel(
            card,
            text=status,
            width=110,
            height=30,
            corner_radius=8,
            fg_color=("gray75", "gray25"),
        )

        status_label.grid(
            row=0,
            column=1,
            padx=14,
            pady=12,
            sticky="n",
        )

        # --------------------------------------------------------
        # Clique no card para abrir os detalhes do pedido
        # --------------------------------------------------------

        self._bind_card_click(
            card,
            order.id,
        )

    def _bind_card_click(self, widget, order_id):
        if not callable(self.on_open_order):
            return

        widget.configure(cursor="hand2")
        widget.bind(
            "<Button-1>",
            lambda event, oid=order_id: self._open_order(oid),
        )

        for child in widget.winfo_children():
            self._bind_card_click(child, order_id)

    def _open_order(self, order_id):
        if callable(self.on_open_order):
            self.on_open_order(order_id)

    # ============================================================
    # Formatação
    # ============================================================

    def _format_withdrawn_at(self, value):
        if not value:
            return "Não informado"

        try:
            dt = datetime.strptime(
                value,
                "%Y-%m-%d %H:%M:%S",
            )

            return dt.strftime(
                "%d/%m/%Y às %H:%M"
            )

        except (ValueError, TypeError):
            return value

    def _format_money(self, value):
        return (
            f"R$ {value:,.2f}"
            .replace(",", "X")
            .replace(".", ",")
            .replace("X", ".")
        )

    # ============================================================
    # Mensagens
    # ============================================================

    def _show_error(self, title, message):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        dialog.geometry("420x180")
        dialog.resizable(False, False)

        dialog.transient(self.winfo_toplevel())
        dialog.grab_set()

        ctk.CTkLabel(
            dialog,
            text=title,
            font=ctk.CTkFont(
                size=18,
                weight="bold",
            ),
        ).pack(
            padx=20,
            pady=(20, 10),
        )

        ctk.CTkLabel(
            dialog,
            text=message,
            wraplength=360,
        ).pack(
            padx=20,
            pady=10,
        )

        ctk.CTkButton(
            dialog,
            text="OK",
            width=100,
            command=dialog.destroy,
        ).pack(
            pady=(5, 20),
        )