import customtkinter as ctk


class OrderCommand(ctk.CTkFrame):

    def __init__(
        self,
        master,
        command_text: str,
        callbacks: dict
    ):
        super().__init__(master)

        self.command_text = command_text
        self.callbacks = callbacks

        self._build()

    def _build(self):

        self.grid_columnconfigure(
            0,
            weight=1
        )

        title = ctk.CTkLabel(
            self,
            text="Comanda",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=12,
            pady=(12,10)
        )

        self.command_box = ctk.CTkTextbox(
            self,
            height=220
        )

        self.command_box.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=12,
            pady=(0,12)
        )

        self.command_box.insert(
            "1.0",
            self.command_text
        )

        self.command_box.configure(
            state="disabled"
        )

        copy_button = ctk.CTkButton(
            self,
            text="Copiar Comanda",
            command=self.callbacks["copy_command"]
        )

        copy_button.grid(
            row=2,
            column=0,
            sticky="w",
            padx=12,
            pady=(0,12)
        )