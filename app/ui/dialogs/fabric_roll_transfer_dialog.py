import customtkinter as ctk


class FabricRollTransferDialog(ctk.CTkToplevel):

    def __init__(self, master, roll, on_confirm):
        super().__init__(master)

        self.roll = roll
        self.on_confirm = on_confirm

        self.title("Transferir Malha")
        self.geometry("400x350")

        self.transient(master)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):

        title = ctk.CTkLabel(
            self,
            text=self.roll.name,
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(pady=(20, 20))

        # 🔥 origem

        self.from_var = ctk.StringVar()

        from_menu = ctk.CTkOptionMenu(
            self,
            variable=self.from_var,
            values=[
                loc.location_name
                for loc in self.roll.locations
            ]
        )
        from_menu.pack(pady=10)

        # 🔥 destino

        self.to_var = ctk.StringVar()

        to_menu = ctk.CTkOptionMenu(
            self,
            variable=self.to_var,
            values=[
                loc.location_name
                for loc in self.roll.locations
            ]
        )
        to_menu.pack(pady=10)

        # 🔥 quantidade

        self.qty_entry = ctk.CTkEntry(
            self,
            placeholder_text="Quantidade"
        )
        self.qty_entry.pack(pady=10)

        # 🔥 botão

        confirm_btn = ctk.CTkButton(
            self,
            text="Transferir",
            fg_color="#7C3AED",
            command=self._confirm
        )
        confirm_btn.pack(pady=20)

    def _confirm(self):

        try:

            qty = int(self.qty_entry.get())

            if qty <= 0:
                return

        except:
            return

        self.on_confirm(
            self.roll,
            self.from_var.get(),
            self.to_var.get(),
            qty
        )

        self.destroy()