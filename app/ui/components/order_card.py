import customtkinter as ctk


class OrderCard(ctk.CTkFrame):
    """
    Card visual utilizado na tela de gerenciamento de pedidos.
    """

    def __init__(
        self,
        master,
        order_id: int,
        client: str,
        product_name: str,
        stage: str,
        created_at: str,
        command=None,
        width: int = 500,
        height: int = 190,
        **kwargs
    ):
        super().__init__(
            master,
            width=width,
            height=height,
            corner_radius=12,
            border_width=2,
            fg_color="#2B2B2B",
            border_color="#3C3C3C",
            **kwargs
        )

        self.grid_propagate(False)

        self.order_id = order_id
        self.client = client
        self.product_name = product_name
        self.stage = stage
        self.created_at = created_at

        self.command = command

        self.selected = False
        self.hover = False

        self.interactive_widgets = []
        self.value_labels = []

        # ==========================
        # Cores
        # ==========================

        self.default_fg = "#2B2B2B"
        self.hover_fg = "#343434"
        self.selected_fg = "#1F3B63"

        self.default_border = "#3C3C3C"
        self.hover_border = "#3B82F6"
        self.selected_border = "#2563EB"

        self.title_color = "#F5F5F5"
        self.subtitle_color = "#A8A8A8"
        self.highlight_color = "#3B82F6"

        self._build_ui()
        self._bind_events()
        self._apply_style()

    # =====================================================
    # Propriedades
    # =====================================================

    @property
    def id(self):
        return self.order_id

    @property
    def client_name(self):
        return self.client

    @property
    def product(self):
        return self.product_name

    @property
    def current_stage(self):
        return self.stage

    @property
    def created(self):
        return self.created_at

    @property
    def is_selected(self):
        return self.selected

    # =====================================================
    # Interface
    # =====================================================

    def _build_ui(self):

        self.columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text=f"📦 Pedido #{self.order_id}",
            font=("Segoe UI", 20, "bold"),
            anchor="w",
            text_color=self.title_color
        )

        self.title_label.pack(
            fill="x",
            padx=20,
            pady=(18, 10)
        )

        self.info_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.info_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 15)
        )

        self._create_info_row(
            "Cliente",
            self.client
        )

        self._create_info_row(
            "Produto",
            self.product_name
        )

        self._create_info_row(
            "Etapa",
            self.stage
        )

        self._create_info_row(
            "Prazo",
            self.created_at
        )

    def _create_info_row(
        self,
        title: str,
        value: str,
    ):

        row = ctk.CTkFrame(
            self.info_frame,
            fg_color="transparent"
        )

        row.columnconfigure(1, weight=1)

        row.pack(
            fill="x",
            pady=2
        )

        title_label = ctk.CTkLabel(
            row,
            text=f"{title}:",
            width=90,
            anchor="w",
            font=("Segoe UI", 13, "bold"),
            text_color=self.subtitle_color
        )

        title_label.pack(
            side="left"
        )

        value_label = ctk.CTkLabel(
            row,
            text=value,
            anchor="w",
            font=("Segoe UI", 13),
            text_color=self.title_color
        )

        value_label.pack(
            side="left",
            fill="x",
            expand=True
        )

        self.interactive_widgets.extend([
            row,
            title_label,
            value_label
        ])

        self.value_labels.append(value_label)

    def _register_widget(self, widget):

        widget.bind("<Enter>", self._on_enter)
        widget.bind("<Leave>", self._on_leave)
        widget.bind("<Button-1>", self._on_click)

        try:
            widget.configure(cursor="hand2")
        except Exception:
            pass


    def _bind_events(self):

        self._register_widget(self)
        self._register_widget(self.title_label)
        self._register_widget(self.info_frame)

        for widget in self.interactive_widgets:
            self._register_widget(widget)


    def _apply_style(self):

        if self.selected:
            fg = self.selected_fg
            border = self.selected_border
            title = self.highlight_color

        elif self.hover:
            fg = self.hover_fg
            border = self.hover_border
            title = self.highlight_color

        else:
            fg = self.default_fg
            border = self.default_border
            title = self.title_color

        self.configure(
            fg_color=fg,
            border_color=border
        )

        self.title_label.configure(
            text_color=title
        )

        for label in self.value_labels:
            label.configure(text_color=title)


    def _on_enter(self, event):
        self.hover = True
        self._apply_style()


    def _on_leave(self, event):
        self.hover = False
        self._apply_style()


    def _on_click(self, event):

        if self.command:
            self.command(self)


    def select(self):
        self.selected = True
        self._apply_style()


    def deselect(self):
        self.selected = False
        self._apply_style()