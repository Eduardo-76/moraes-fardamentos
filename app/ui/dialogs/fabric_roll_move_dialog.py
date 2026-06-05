import customtkinter as ctk


class FabricRollMoveDialog(ctk.CTkToplevel):
    def __init__(self, master, roll, on_confirm):
        super().__init__(master)

        self.roll = roll
        self.on_confirm = on_confirm

        self.title("Movimentar Rolo")
        self.geometry("400x350")

        self.transient(master)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(
            self,
            text=self.roll.name,
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=10)

        # origem
        self.location_var = ctk.StringVar()
        from_menu = ctk.CTkOptionMenu(
            self,
            variable=self.location_var,
            values=[loc.location_name for loc in self.roll.locations],
        )
        from_menu.pack(pady=10)

        # quantidade
        self.qty_entry = ctk.CTkEntry(self, placeholder_text="Quantidade")
        self.qty_entry.pack(pady=10)

        btn = ctk.CTkButton(self, text="Confirmar", command=self._confirm)
        btn.pack(pady=20)


    def _confirm(self):
        try:
            qty = int(self.qty_entry.get())

            if qty <= 0:
                return

        except:
            return

        self.on_confirm(
            self.roll,
            self.location_var.get(),
            qty
        )

        self.destroy()