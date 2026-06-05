import customtkinter as ctk


class FabricVoiceConfirmDialog(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        roll,
        quantity,
        on_confirm
    ):
        super().__init__(master)

        self.roll = roll
        self.quantity = quantity
        self.on_confirm = on_confirm

        self.title("Confirmar entrada")
        self.geometry("420x300")

        self.transient(master)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Entrada detectada",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        title.pack(pady=(20, 10))

        text = f"""
Malha encontrada:

{self.roll.name}

Quantidade:
+{self.quantity}

Local:
Depósito
"""

        label = ctk.CTkLabel(
            self,
            text=text,
            justify="left"
        )

        label.pack(
            padx=20,
            pady=20
        )

        buttons = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        buttons.pack(
            pady=20
        )

        cancel_btn = ctk.CTkButton(
            buttons,
            text="Cancelar",
            fg_color="#DC2626",
            command=self.destroy
        )

        cancel_btn.pack(
            side="left",
            padx=10
        )

        confirm_btn = ctk.CTkButton(
            buttons,
            text="Confirmar",
            command=self._confirm
        )

        confirm_btn.pack(
            side="left",
            padx=10
        )

    def _confirm(self):

        self.destroy()

        self.after(
            100,
            lambda: self.on_confirm(
                self.roll,
                self.quantity
            )
        )