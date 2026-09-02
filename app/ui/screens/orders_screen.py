from datetime import datetime

import customtkinter as ctk
from tkinter import messagebox

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
        header_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=8,
            pady=8,
        )

        header_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header_frame,
            text="Pedidos",
            font=ctk.CTkFont(
                size=28,
                weight="bold",
            ),
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=16,
            pady=(16, 4),
        )

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Lista geral de pedidos cadastrados no sistema.",
            font=ctk.CTkFont(size=14),
        )

        subtitle.grid(
            row=1,
            column=0,
            sticky="w",
            padx=16,
            pady=(0, 12),
        )

        buttons_frame = ctk.CTkFrame(
            header_frame,
            fg_color="transparent",
        )

        buttons_frame.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=16,
            pady=16,
            sticky="e",
        )

        self.new_button = ctk.CTkButton(
            buttons_frame,
            text="Novo pedido",
            command=self._open_new_order_dialog,
        )

        self.new_button.grid(
            row=0,
            column=0,
            padx=(0, 8),
        )

        self.reload_button = ctk.CTkButton(
            buttons_frame,
            text="Atualizar lista",
            command=self.refresh_orders,
        )

        self.reload_button.grid(
            row=0,
            column=1,
        )

    def _build_filters(self) -> None:
        filters_frame = ctk.CTkFrame(self)

        filters_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=8,
            pady=(0, 8),
        )

        # =====================================================
        # LINHA PRINCIPAL DOS FILTROS
        # =====================================================

        filters_frame.grid_columnconfigure(0, weight=2)
        filters_frame.grid_columnconfigure(1, weight=1)
        filters_frame.grid_columnconfigure(2, weight=1)
        filters_frame.grid_columnconfigure(3, weight=1)
        filters_frame.grid_columnconfigure(4, weight=1)
        filters_frame.grid_columnconfigure(5, weight=1)

        self.search_entry = ctk.CTkEntry(
            filters_frame,
            placeholder_text="Buscar por cliente...",
        )

        self.search_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=8,
            pady=12,
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda _event: self.refresh_orders(),
        )

        self.stage_filter = ctk.CTkOptionMenu(
            filters_frame,
            values=["Todas as etapas"] + ORDER_STAGES,
            command=lambda _value: self.refresh_orders(),
        )

        self.stage_filter.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=8,
            pady=12,
        )

        self.stage_filter.set("Todas as etapas")

        self.priority_filter = ctk.CTkOptionMenu(
            filters_frame,
            values=["Todas prioridades"] + PRIORITIES,
            command=lambda _value: self.refresh_orders(),
        )

        self.priority_filter.grid(
            row=0,
            column=2,
            sticky="ew",
            padx=8,
            pady=12,
        )

        self.priority_filter.set("Todas prioridades")

        self.stock_filter = ctk.CTkOptionMenu(
            filters_frame,
            values=[
                "Todos",
                "Estoque baixado",
                "Sem baixa de estoque",
            ],
            command=lambda _value: self.refresh_orders(),
        )

        self.stock_filter.grid(
            row=0,
            column=3,
            sticky="ew",
            padx=8,
            pady=12,
        )

        self.stock_filter.set("Todos")

        self.late_filter = ctk.CTkOptionMenu(
            filters_frame,
            values=[
                "Todos prazos",
                "Apenas atrasados",
                "Não atrasados",
            ],
            command=lambda _value: self.refresh_orders(),
        )

        self.late_filter.grid(
            row=0,
            column=4,
            sticky="ew",
            padx=8,
            pady=12,
        )

        self.late_filter.set("Todos prazos")

        clear_button = ctk.CTkButton(
            filters_frame,
            text="Limpar filtros",
            command=self._clear_filters,
        )

        clear_button.grid(
            row=0,
            column=5,
            sticky="ew",
            padx=8,
            pady=12,
        )

        # =====================================================
        # FILTRO POR PERÍODO
        # =====================================================

        period_frame = ctk.CTkFrame(
            filters_frame,
            fg_color="transparent",
        )

        period_frame.grid(
            row=1,
            column=0,
            columnspan=6,
            sticky="ew",
            padx=8,
            pady=(0, 10),
        )

        period_frame.grid_columnconfigure(1, weight=1)
        period_frame.grid_columnconfigure(3, weight=1)

        start_label = ctk.CTkLabel(
            period_frame,
            text="Data inicial:",
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
        )

        start_label.grid(
            row=0,
            column=0,
            padx=(4, 6),
            pady=4,
        )

        self.start_date_entry = ctk.CTkEntry(
            period_frame,
            placeholder_text="DD/MM/AAAA",
        )

        self.start_date_entry.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(0, 16),
            pady=4,
        )

        end_label = ctk.CTkLabel(
            period_frame,
            text="Data final:",
            font=ctk.CTkFont(
                size=13,
                weight="bold",
            ),
        )

        end_label.grid(
            row=0,
            column=2,
            padx=(4, 6),
            pady=4,
        )

        self.end_date_entry = ctk.CTkEntry(
            period_frame,
            placeholder_text="DD/MM/AAAA",
        )

        self.end_date_entry.grid(
            row=0,
            column=3,
            sticky="ew",
            padx=(0, 16),
            pady=4,
        )

        self.today_var = ctk.BooleanVar(value=False)

        self.today_checkbox = ctk.CTkCheckBox(
            period_frame,
            text="Até hoje",
            variable=self.today_var,
            command=self._toggle_until_today,
        )

        self.today_checkbox.grid(
            row=0,
            column=4,
            padx=(0, 12),
            pady=4,
        )

        apply_period_button = ctk.CTkButton(
            period_frame,
            text="Aplicar período",
            command=self._apply_period_filter,
            width=130,
        )

        apply_period_button.grid(
            row=0,
            column=5,
            padx=(0, 4),
            pady=4,
        )

        # Enter também aplica o período.
        self.start_date_entry.bind(
            "<Return>",
            lambda _event: self._apply_period_filter(),
        )

        self.end_date_entry.bind(
            "<Return>",
            lambda _event: self._apply_period_filter(),
        )

    def _build_list_container(self) -> None:
        self.list_frame = ctk.CTkScrollableFrame(self)

        self.list_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=8,
            pady=8,
        )

        self.list_frame.grid_columnconfigure(
            0,
            weight=1,
        )

    # =========================================================
    # FILTRO POR PERÍODO
    # =========================================================

    def _parse_date(self, value: str):
        value = value.strip()

        if not value:
            return None

        try:
            return datetime.strptime(
                value,
                "%d/%m/%Y",
            ).date()

        except ValueError:
            raise ValueError(
                f"Informe uma data válida no formato DD/MM/AAAA.\n\n"
                f"Valor informado: {value}"
            )

    def _get_period_dates(self):
        start_text = self.start_date_entry.get().strip()
        end_text = self.end_date_entry.get().strip()

        # Se "Até hoje" estiver marcado, a data final é sempre hoje.
        if self.today_var.get():
            end_date = datetime.now().date()

            # Atualiza visualmente o campo.
            self.end_date_entry.delete(0, "end")
            self.end_date_entry.insert(
                0,
                end_date.strftime("%d/%m/%Y"),
            )
        else:
            end_date = self._parse_date(end_text)

        start_date = self._parse_date(start_text)

        if start_date and end_date:
            if start_date > end_date:
                raise ValueError(
                    "A data inicial não pode ser maior "
                    "que a data final."
                )

        return start_date, end_date

    def _apply_period_filter(self) -> None:
        try:
            self._get_period_dates()

        except ValueError as error:
            messagebox.showerror(
                "Data inválida",
                str(error),
                parent=self,
            )
            return

        self.refresh_orders()

    def _toggle_until_today(self) -> None:
        if self.today_var.get():
            today = datetime.now().date()

            self.end_date_entry.delete(
                0,
                "end",
            )

            self.end_date_entry.insert(
                0,
                today.strftime("%d/%m/%Y"),
            )

        self._apply_period_filter()

    # =========================================================
    # PEDIDOS
    # =========================================================

    def refresh_orders(self) -> None:
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        orders = self._apply_filters(
            self.order_service.list_orders()
        )

        if not orders:
            placeholder = ctk.CTkLabel(
                self.list_frame,
                text="Nenhum pedido encontrado com os filtros atuais.",
                font=ctk.CTkFont(size=15),
            )

            placeholder.grid(
                row=0,
                column=0,
                padx=16,
                pady=16,
                sticky="w",
            )

            return

        for index, order in enumerate(orders):
            card = self._create_order_card(order)

            card.grid(
                row=index,
                column=0,
                sticky="ew",
                padx=8,
                pady=8,
            )

    def _apply_filters(self, orders):
        search = self.search_entry.get().strip().lower()
        stage = self.stage_filter.get()
        priority = self.priority_filter.get()
        stock = self.stock_filter.get()
        late = self.late_filter.get()

        # -----------------------------------------------------
        # PERÍODO
        # -----------------------------------------------------

        try:
            start_date, end_date = self._get_period_dates()

        except ValueError:
            # Não interrompe a tela enquanto o usuário ainda
            # estiver digitando uma data.
            start_date = None
            end_date = None

        filtered = []

        for order in orders:

            # -------------------------------------------------
            # CLIENTE
            # -------------------------------------------------

            if search:
                client_name = (
                    order.client_name or ""
                ).lower()

                if search not in client_name:
                    continue

            # -------------------------------------------------
            # ETAPA
            # -------------------------------------------------

            if stage != "Todas as etapas":
                if order.current_stage != stage:
                    continue

            # -------------------------------------------------
            # PRIORIDADE
            # -------------------------------------------------

            if priority != "Todas prioridades":
                if order.priority != priority:
                    continue

            # -------------------------------------------------
            # ESTOQUE
            # -------------------------------------------------

            if (
                stock == "Estoque baixado"
                and not order.stock_withdrawn
            ):
                continue

            if (
                stock == "Sem baixa de estoque"
                and order.stock_withdrawn
            ):
                continue

            # -------------------------------------------------
            # ATRASO
            # -------------------------------------------------

            is_late = self._is_order_late(order)

            if (
                late == "Apenas atrasados"
                and not is_late
            ):
                continue

            if (
                late == "Não atrasados"
                and is_late
            ):
                continue

            # -------------------------------------------------
            # PERÍODO DO PRAZO
            # -------------------------------------------------

            if start_date or end_date:

                if not order.deadline:
                    continue

                try:
                    order_date = datetime.strptime(
                        order.deadline,
                        "%Y-%m-%d",
                    ).date()

                except ValueError:
                    continue

                if start_date and order_date < start_date:
                    continue

                if end_date and order_date > end_date:
                    continue

            filtered.append(order)

        return filtered

    def _is_order_late(self, order) -> bool:
        if not order.deadline:
            return False

        if order.current_stage == "Retirada":
            return False

        try:
            deadline_date = datetime.strptime(
                order.deadline,
                "%Y-%m-%d",
            ).date()

        except ValueError:
            return False

        return deadline_date < datetime.now().date()

    def _create_order_card(self, order) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.list_frame)

        frame.grid_columnconfigure(
            0,
            weight=1,
        )

        title = ctk.CTkLabel(
            frame,
            text=order.client_name or "Sem cliente",
            font=ctk.CTkFont(
                size=20,
                weight="bold",
            ),
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=16,
            pady=(16, 8),
        )

        stock_text = (
            "Estoque baixado"
            if order.stock_withdrawn
            else "Sem baixa de estoque"
        )

        late_text = (
            " | ATRASADO"
            if self._is_order_late(order)
            else ""
        )

        details = ctk.CTkLabel(
            frame,
            text=(
                f"Modelo: {order.model or 'Não informado'}\n"
                f"Tecido: {order.fabric or 'Não informado'}\n"
                f"Quantidade: {order.quantity or 0}\n"
                f"Prazo: {order.deadline or 'Sem prazo'}"
                f"{late_text}\n"
                f"Etapa atual: "
                f"{order.current_stage or 'Recepção'}\n"
                f"{stock_text}"
            ),
            justify="left",
            font=ctk.CTkFont(size=14),
        )

        details.grid(
            row=1,
            column=0,
            sticky="w",
            padx=16,
            pady=(0, 12),
        )

        priority = order.priority or "Baixa"

        priority_color = PRIORITY_COLORS.get(
            priority,
            "#9CA3AF",
        )

        priority_label = ctk.CTkLabel(
            frame,
            text=f"Prioridade: {priority}",
            fg_color=priority_color,
            corner_radius=8,
            padx=10,
            pady=6,
        )

        priority_label.grid(
            row=0,
            column=1,
            padx=16,
            pady=(16, 8),
            sticky="e",
        )

        open_button = ctk.CTkButton(
            frame,
            text="Abrir pedido",
            command=lambda oid=order.id: self._open_order(oid),
        )

        open_button.grid(
            row=1,
            column=1,
            padx=16,
            pady=(0, 12),
            sticky="e",
        )

        return frame

    # =========================================================
    # LIMPAR FILTROS
    # =========================================================

    def _clear_filters(self) -> None:
        self.search_entry.delete(
            0,
            "end",
        )

        self.stage_filter.set(
            "Todas as etapas"
        )

        self.priority_filter.set(
            "Todas prioridades"
        )

        self.stock_filter.set(
            "Todos"
        )

        self.late_filter.set(
            "Todos prazos"
        )

        self.start_date_entry.delete(
            0,
            "end",
        )

        self.end_date_entry.delete(
            0,
            "end",
        )

        self.today_var.set(False)

        self.refresh_orders()

    # =========================================================
    # NAVEGAÇÃO
    # =========================================================

    def _open_order(self, order_id: int) -> None:
        if callable(self.on_open_order):
            self.on_open_order(order_id)

    def _open_new_order_dialog(self) -> None:
        OrderFormDialog(
            self,
            on_save=self._handle_order_created,
        )

    def _handle_order_created(self, order_id: int) -> None:
        self.refresh_orders()

        if callable(self.on_open_order):
            self.on_open_order(order_id)