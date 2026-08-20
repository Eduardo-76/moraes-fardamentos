import customtkinter as ctk


class FabricVoiceSelectionDialog(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        rolls,
        quantity,
        fabric_name,
        location,
        on_confirm
    ):
        super().__init__(master)

        self.rolls = rolls
        self.quantity = quantity
        self.fabric_name = fabric_name
        self.location = location
        self.on_confirm = on_confirm

        self.result = None

        self.title(
            "Selecionar Estoque"
        )

        self.geometry(
            "650x500"
        )

        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self._build()

    def _build(self):

        title = ctk.CTkLabel(
            self,
            text="Estoque encontrado",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            padx=20,
            pady=(20, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text=(
                f"Entrada de {self.quantity} unidades\n"
                f"Malha identificada: "
                f"{self.fabric_name}"
            )
        )

        subtitle.grid(
            row=1,
            column=0,
            padx=20,
            pady=(0, 15)
        )

        self.list_frame = ctk.CTkScrollableFrame(
            self
        )

        self.list_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20,
            pady=10
        )

        self.grid_rowconfigure(
            2,
            weight=1
        )

        if not self.rolls:

            label = ctk.CTkLabel(
                self.list_frame,
                text=(
                    "Nenhum estoque semelhante "
                    "foi encontrado."
                ),
                font=ctk.CTkFont(size=15)
            )

            label.pack(
                padx=20,
                pady=30
            )

            return

        for roll in self.rolls:

            self._create_roll_option(
                roll
            )

        cancel_button = ctk.CTkButton(
            self,
            text="Cancelar",
            fg_color="#374151",
            hover_color="#1F2937",
            command=self.destroy
        )

        cancel_button.grid(
            row=3,
            column=0,
            padx=20,
            pady=15
        )

    def _create_roll_option(
        self,
        roll
    ):

        frame = ctk.CTkFrame(
            self.list_frame
        )

        frame.pack(
            fill="x",
            padx=5,
            pady=6
        )

        frame.grid_columnconfigure(
            0,
            weight=1
        )

        title = ctk.CTkLabel(
            frame,
            text=roll.name,
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=12,
            pady=(10, 2)
        )

        details = ctk.CTkLabel(
            frame,
            text=(
                f"Quantidade atual: "
                f"{roll.total_quantity}\n"
                f"Disponível para entrada."
            ),
            justify="left"
        )

        details.grid(
            row=1,
            column=0,
            sticky="w",
            padx=12,
            pady=(0, 10)
        )

        button = ctk.CTkButton(
            frame,
            text="Selecionar",
            width=110,
            command=lambda r=roll: (
                self._select_roll(r)
            )
        )

        button.grid(
            row=0,
            column=1,
            rowspan=2,
            padx=12
        )

    def _select_roll(self, roll):

        self.destroy()

        if callable(self.on_confirm):
            self.on_confirm(
                roll,
                self.quantity,
                self.location
            )