
import customtkinter as ctk


class DashboardScreen(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_cards()
        self._build_upcoming_deadlines()

    def _build_header(self) -> None:
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=8, pady=8)
        header_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header_frame,
            text="Dashboard",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 4))

        subtitle = ctk.CTkLabel(
            header_frame,
            text="Visão geral dos pedidos com prazo nos próximos 5 dias.",
            font=ctk.CTkFont(size=14),
        )
        subtitle.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 16))

    def _build_cards(self) -> None:
        card_1 = self._create_info_card(
            title="Pedidos Próximos do Prazo",
            value="0",
            description="Pedidos com prazo nos próximos 5 dias.",
        )
        card_1.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)

        card_2 = self._create_info_card(
            title="Pedidos em Produção",
            value="0",
            description="Pedidos atualmente em alguma etapa produtiva.",
        )
        card_2.grid(row=1, column=1, sticky="nsew", padx=8, pady=8)

    def _build_upcoming_deadlines(self) -> None:
        deadlines_frame = ctk.CTkFrame(self)
        deadlines_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=8, pady=8)
        deadlines_frame.grid_columnconfigure(0, weight=1)
        deadlines_frame.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            deadlines_frame,
            text="Próximos prazos",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        placeholder = ctk.CTkLabel(
            deadlines_frame,
            text=(
                "Nenhum pedido cadastrado ainda.\n\n"
                "Quando começarmos a cadastrar pedidos, eles aparecerão aqui "
                "com cliente, prazo e etapa atual."
            ),
            justify="left",
            font=ctk.CTkFont(size=14),
        )
        placeholder.grid(row=1, column=0, sticky="nw", padx=16, pady=(0, 16))

    def _create_info_card(self, title: str, value: str, description: str) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self)
        frame.grid_columnconfigure(0, weight=1)

        title_label = ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        title_label.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        value_label = ctk.CTkLabel(
            frame,
            text=value,
            font=ctk.CTkFont(size=36, weight="bold"),
        )
        value_label.grid(row=1, column=0, sticky="w", padx=16, pady=4)

        description_label = ctk.CTkLabel(
            frame,
            text=description,
            justify="left",
            font=ctk.CTkFont(size=13),
        )
        description_label.grid(row=2, column=0, sticky="w", padx=16, pady=(4, 16))

        return frame