import customtkinter as ctk
from app.services.fabric_roll_service import FabricRollService


class FabricRollScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.service = FabricRollService()

        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Rolos de Malha",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        title.grid(row=0, column=0, padx=16, pady=16, sticky="w")

        self.grid_rowconfigure(2, weight=1)

        self.search_var = ctk.StringVar()

        self.search_entry = ctk.CTkEntry(
            self,
            placeholder_text="Buscar rolo...",
            textvariable=self.search_var
        )

        self.search_entry.grid(
            row=1,
            column=0,
            padx=16,
            pady=(70, 0),
            sticky="ew"
        )

        self.search_var.trace_add(
            "write",
            lambda *args: self.refresh()
        )

        self.list_frame = ctk.CTkScrollableFrame(
            self,
            corner_radius=12
        )
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=16, pady=16)

        self.refresh()

        self.new_button = ctk.CTkButton(
            self,
            text="Novo rolo",
            command=self._open_create_dialog,
        )
        self.new_button.grid(row=0, column=1, padx=16, pady=16, sticky="e")


    def refresh(self):

        for w in self.list_frame.winfo_children():
            w.destroy()

        rolls = self.service.list_rolls()
        search = self.search_var.get().lower().strip()

        if search:
            filtered = []

            for roll in rolls:
                if search in roll.name.lower():
                    filtered.append(roll)
            rolls = filtered

        for roll in rolls:
            card = self._create_roll_card(roll)

            card.pack(
                fill="x",
                padx=12,
                pady=12
            )


    def _create_roll_card(self, roll):
        # 🔥 alerta visual

        border_color = "#2A2A2A"

        if roll.available_quantity <= 10:
            border_color = "#DC2626"  # vermelho

        elif roll.available_quantity <= 20:
            border_color = "#D97706"  # amarelo

        frame = ctk.CTkFrame(
            self.list_frame,
            corner_radius=12,
            fg_color=("gray20", "gray20")
        )

        frame.grid_columnconfigure(0, weight=1)
        frame.configure(
            border_width=2,
            border_color=border_color
        )

        separator = ctk.CTkFrame(frame, height=2, fg_color="#2A2A2A")
        separator.grid(row=1, column=0, columnspan=2, sticky="ew", padx=12, pady=6)

        title = ctk.CTkLabel(
            frame,
            text=roll.name,
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 4))

        total = ctk.CTkLabel(
            frame,
            text=(
                f"Total: {roll.total_quantity}\n"
                f"Reservado: {roll.reserved_quantity}\n"
                f"Disponível: {roll.available_quantity}"
            )
        )
        total.grid(row=1, column=0, sticky="w", padx=12)

        locations_text = ""
        for loc in roll.locations:
            locations_text += f"- {loc.location_name}: {loc.quantity}\n"

        locations = ctk.CTkLabel(
            frame,
            text=locations_text.strip(),
            justify="left",
        )
        locations.grid(row=2, column=0, sticky="w", padx=12, pady=(4, 8))

        # 🔥 Botões (ainda simples)
        buttons = ctk.CTkFrame(frame, fg_color="transparent")
        buttons.grid(row=0, column=1, rowspan=3, padx=12, pady=12, sticky="e")

        entry_btn = ctk.CTkButton(
            buttons,
            text="Entrada",
            width=120,
            fg_color="#15803D",
            hover_color="#166534",
            command=lambda r=roll: self._entry_roll(r),
        )
        entry_btn.pack(pady=4)

        transfer_btn = ctk.CTkButton(
            buttons,
            text="Transferir",
            width=120,
            fg_color="#7C3AED",
            command=lambda r=roll: self._transfer_roll(r),
        )
        transfer_btn.pack(pady=4)

        move_btn = ctk.CTkButton(
            buttons,
            text="Dar saída",
            width=120,
            command=lambda r=roll: self._move_roll(r),
        )
        move_btn.pack(pady=4)

        edit_btn = ctk.CTkButton(
            buttons,
            text="Editar",
            width=120,
            command=lambda r=roll: self._edit_roll(r),
        )
        edit_btn.pack(pady=4)

        delete_btn = ctk.CTkButton(
            buttons,
            text="Excluir",
            width=120,
            fg_color="#DC2626",
            command=lambda r=roll: self._delete_roll(r),
        )
        delete_btn.pack(pady=4)

        return frame

    def _open_create_dialog(self):
        from app.ui.dialogs.fabric_roll_form_dialog import FabricRollFormDialog

        FabricRollFormDialog(
            self,
            on_save=self._handle_created
        )

    def _handle_created(self):
        self.refresh()


    def _move_roll(self, roll):
        from app.ui.dialogs.fabric_roll_move_dialog import FabricRollMoveDialog

        FabricRollMoveDialog(
            self,
            roll,
            on_confirm=self._handle_move
        )

    def _handle_move(self, roll, from_loc, qty):

        for loc in roll.locations:
            if loc.location_name == from_loc:
                if loc.quantity < qty:
                    print("Quantidade insuficiente")
                    return
                loc.quantity -= qty

        # 🔥 AJUSTE DO TOTAL
        roll.total_quantity -= qty

        self.service.register_movement(
            roll_id=roll.id,
            quantity=qty,
            movement_type="saida",
            location_name=from_loc
        )

        self.service.update_roll(roll)

        self.refresh()

    def _edit_roll(self, roll):

        from app.ui.dialogs.fabric_roll_edit_dialog import (
            FabricRollEditDialog
        )

        FabricRollEditDialog(
            self,
            roll,
            on_save=self.refresh
        )

    def _entry_roll(self, roll):
        from app.ui.dialogs.fabric_roll_move_dialog import FabricRollMoveDialog

        FabricRollMoveDialog(
            self,
            roll,
            on_confirm=self._handle_entry
        )


    def _delete_roll(self, roll):

        from tkinter import messagebox

        confirm = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja excluir o rolo:\n\n{roll.name} ?"
        )

        if not confirm:
            return

        self.service.delete_roll(roll.id)

        self.refresh()

    def _handle_entry(self, roll, location_name, qty):

        for loc in roll.locations:
            if loc.location_name == location_name:
                loc.quantity += qty

        roll.total_quantity += qty

        self.service.register_movement(
            roll_id=roll.id,
            quantity=qty,
            movement_type="entrada",
            location_name=location_name
        )

        self.service.update_roll(roll)

        self.refresh()   


    def _transfer_roll(self, roll):

        from app.ui.dialogs.fabric_roll_transfer_dialog import (
            FabricRollTransferDialog
        )

        FabricRollTransferDialog(
            self,
            roll,
            on_confirm=self._handle_transfer
        )

    def _handle_transfer(
        self,
        roll,
        from_loc,
        to_loc,
        qty
    ):

        if from_loc.quantity < qty:
            print("Estoque insuficiente")
            return

        if from_loc == to_loc:
            return

        if from_loc.location_name == to_loc.location_name:
            print("Locais iguais")
            return

        from_location = None
        to_location = None

        for loc in roll.locations:

            if loc.location_name == from_loc:
                from_location = loc

            if loc.location_name == to_loc:
                to_location = loc

        if not from_location or not to_location:
            return

        if from_location.quantity < qty:
            return

        from_location.quantity -= qty
        to_location.quantity += qty

        self.service.update_roll(roll)

        from_name = (
            from_location.location_name
            if hasattr(from_location, "location_name")
            else from_location
        )

        to_name = (
            to_location.location_name
            if hasattr(to_location, "location_name")
            else to_location
        )

        self.service.register_transfer(
            roll.id,
            from_name,
            to_name,
            qty
        )

        self.refresh()