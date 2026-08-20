import customtkinter as ctk
from app.ui.components.order_card import OrderCard
from app.services.order_service import OrderService
from tkinter import messagebox



class OrderManagementScreen(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        # ==========================
        # Serviços
        # ==========================
        self.order_service = OrderService()

        # ==========================
        # Estado
        # ==========================
        self.selected_order = None
        self.order_cards = []

        # ==========================
        # Variáveis
        # ==========================
        self.search_var = ctk.StringVar()
        self.search_var.trace_add(
            "write",
            lambda *args: self._filter_orders()
        )

        # ==========================
        # Widgets
        # ==========================
        self.title_label = None
        self.search_entry = None
        self.orders_frame = None
        self.selected_label = None
        self.cancel_button = None
        self.delete_button = None

        # ==========================
        # Interface
        # ==========================
        self._build_layout()

        # ==========================
        # Dados
        # ==========================
        self._load_orders()

    # =====================================================
    # Layout
    # =====================================================

    def _build_layout(self):

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._build_header()
        self._build_search()
        self._build_content()
        self._build_footer()

    def _build_header(self):

        self.title_label = ctk.CTkLabel(
            self,
            text="Gerenciar Pedidos",
            font=("Segoe UI", 22, "bold")
        )

        self.title_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20, 10),
            sticky="w"
        )

    def _build_search(self):

        self.search_entry = ctk.CTkEntry(
            self,
            textvariable=self.search_var,
            placeholder_text="Pesquisar pedido..."
        )

        self.search_entry.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 15),
            sticky="ew"
        )

    def _build_content(self):

        self.orders_frame = ctk.CTkScrollableFrame(self)

        self.orders_frame.grid(
            row=2,
            column=0,
            padx=20,
            pady=0,
            sticky="nsew"
        )

    def _build_footer(self):

        footer = ctk.CTkFrame(self, fg_color="transparent")

        footer.grid(
            row=3,
            column=0,
            padx=20,
            pady=20,
            sticky="ew"
        )

        footer.grid_columnconfigure(0, weight=1)

        self.selected_label = ctk.CTkLabel(
            footer,
            text="Pedido selecionado: Nenhum"
        )

        self.selected_label.grid(
            row=0,
            column=0,
            sticky="w"
        )

        self.cancel_button = ctk.CTkButton(
            footer,
            text="Cancelar",
            command=self._clear_selection
        )

        self.cancel_button.grid(
            row=0,
            column=1,
            padx=(10, 10)
        )

        self.refresh_button = ctk.CTkButton(
            footer,
            text="🔄 Atualizar",
            command=self._refresh
        )

        self.refresh_button.grid(
            row=0,
            column=2,
            padx=(0, 10)
        )
       
        self.delete_button = ctk.CTkButton(
            footer,
            text="🗑 Excluir Pedido",
            state="disabled",
            command=self._delete_selected_order
        )

        self.delete_button.grid(
            row=0,
            column=3
        )

    # =====================================================
    # Dados
    # =====================================================

    def _clear_orders(self):

        for card in self.order_cards:
            card.destroy()

        self.order_cards.clear()

        self.selected_order = None

        if self.selected_label:
            self.selected_label.configure(
                text="Pedido selecionado: Nenhum"
            )

        if self.delete_button:
            self.delete_button.configure(
                state="disabled"
            )

    def _load_orders(self):

        self._clear_orders()

        orders = self.order_service.list_orders()

        for order in orders:
            self._create_order_card(order)

    def _create_order_card(self, order):

        card = OrderCard(
            master=self.orders_frame,
            order_id=order.id,
            client=order.client_name or "Não informado",
            product_name=order.model or "Não informado",
            stage=order.current_stage or "Recepção",
            created_at=order.deadline or "-",
            command=self._on_card_selected
        )

        card.pack(
            fill="x",
            padx=10,
            pady=5
        )

        self.order_cards.append(card)

    def _on_card_selected(self, card):

        # Remove a seleção anterior
        for order_card in self.order_cards:
            order_card.deselect()

        # Seleciona o novo card
        card.select()

        # Guarda o selecionado
        self.selected_order = card

        # Atualiza o texto
        if self.selected_label:
            self.selected_label.configure(
                text=f"Pedido selecionado: #{card.id}"
            )

        # Habilita o botão excluir
        if self.delete_button:
            self.delete_button.configure(
            state="normal"
        )

    # =====================================================
    # Pesquisa
    # =====================================================

    def _filter_orders(self):

        text = self.search_var.get().strip().lower()

        self._clear_orders()

        orders = self.order_service.list_orders()

        if not text:

            for order in orders:
                self._create_order_card(order)

            return

        for order in orders:

            values = [
                str(order.id),
                str(order.client_name or ""),
                str(order.model or ""),
                str(order.current_stage or ""),
                str(order.deadline or "")
            ]

            if any(text in value.lower() for value in values):
                self._create_order_card(order)

    # =====================================================
    # Seleção
    # =====================================================

    def _clear_selection(self):

        self.search_var.set("")

        for card in self.order_cards:
            card.deselect()

        self.selected_order = None

        if self.selected_label:
            self.selected_label.configure(
                text="Pedido selecionado: Nenhum"
            )

        if self.delete_button:
            self.delete_button.configure(
                state="disabled"
            )

        self.search_var.set("")

    # =====================================================
    # Exclusão
    # =====================================================

    def _delete_selected_order(self):

        if self.selected_order is None:
            return

        confirm = messagebox.askyesno(
            "Excluir Pedido",
            (
                f"Deseja realmente excluir o pedido "
                f"#{self.selected_order.id}?\n\n"
                "Esta ação não poderá ser desfeita."
            )
        )

        if not confirm:
            return

        try:

            self.order_service.delete_order(
                self.selected_order.id
            )

            messagebox.showinfo(
                "Sucesso",
                "Pedido excluído com sucesso."
            )

            self._load_orders()

        except Exception as exc:

            messagebox.showerror(
                "Erro",
                str(exc)
            )


    def _refresh(self):

        self.search_var.set("")
        self._load_orders()            