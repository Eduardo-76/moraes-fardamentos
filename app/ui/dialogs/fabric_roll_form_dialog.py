import customtkinter as ctk
from app.core.constants import FABRIC_LOCATIONS
from app.services.fabric_roll_service import FabricRollService
from app.models.fabric_roll_model import (
    FabricRollModel,
    FabricRollLocation
)


class FabricRollFormDialog(ctk.CTkToplevel):

    def __init__(self, master, on_save=None, roll=None):
        super().__init__(master)

        self.service = FabricRollService()

        self.on_save = on_save
        self.roll = roll

        self.title(
            "Editar Rolo"
            if roll else
            "Novo Rolo"
        )

        self.geometry("500x500")

        self.location_rows = []

        self._build_ui()

    def _build_ui(self):

        self.name_entry = ctk.CTkEntry(
            self,
            placeholder_text="Nome do rolo"
        )

        self.name_entry.pack(
            pady=10,
            padx=20,
            fill="x"
        )

        # 🔥 frame das localizações

        self.locations_frame = ctk.CTkFrame(self)

        self.locations_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # 🔥 botão adicionar

        add_button = ctk.CTkButton(
            self,
            text="+ Adicionar Local",
            command=self._add_location_row
        )

        add_button.pack(pady=10)

        # 🔥 edição

        if self.roll:

            self.name_entry.insert(
                0,
                self.roll.name
            )

            for loc in self.roll.locations:

                self._add_location_row(
                    loc.location_name,
                    loc.quantity
                )

        else:

            for location in FABRIC_LOCATIONS:

                self._add_location_row(
                    name=location,
                    qty=0
                )

        # 🔥 botão salvar

        self.save_button = ctk.CTkButton(
            self,
            text="Salvar",
            command=self._save
        )

        self.save_button.pack(pady=20)

    def _add_location_row(
        self,
        name="",
        qty=""
    ):

        row = ctk.CTkFrame(
            self.locations_frame,
            fg_color="transparent"
        )

        row.pack(
            fill="x",
            pady=4
        )

        name_entry = ctk.CTkEntry(
            row,
            placeholder_text="Local"
        )

        name_entry.pack(
            side="left",
            expand=True,
            fill="x",
            padx=(0, 8)
        )

        qty_entry = ctk.CTkEntry(
            row,
            width=100,
            placeholder_text="Qtd"
        )

        qty_entry.pack(side="left")

        remove_btn = ctk.CTkButton(
            row,
            text="✕",
            width=40,
            fg_color="#DC2626",
            hover_color="#991B1B",
            command=lambda: self._remove_location_row(row)
        )

        remove_btn.pack(side="left", padx=(8, 0))       

        if name:
            name_entry.insert(0, name)

        if qty != "":
            qty_entry.insert(0, str(qty))

        self.location_rows.append(
            {
                "frame": row,
                "name": name_entry,
                "qty": qty_entry
            }
        )

    def _save(self):

        self.save_button.configure(
            state="disabled"
        )

        try:

            name = self.name_entry.get().strip()

            if not name:
                print("Nome inválido")
                return

            locations = []

            for row_data in self.location_rows:

                name_entry = row_data["name"]
                qty_entry = row_data["qty"]

                loc_name = name_entry.get().strip()
                qty = qty_entry.get().strip()

                if not loc_name:
                    continue

                if not qty.isdigit():
                    print("Quantidade inválida")
                    return

                qty = int(qty)

                if qty < 0:
                    print("Quantidade negativa")
                    return
                
                # 🔥 impedir nomes duplicados

                existing_locations = [
                    loc.location_name.lower()
                    for loc in locations
                ]

                if loc_name.lower() in existing_locations:

                    print(
                        f"Local duplicado: {loc_name}"
                    )

                    return

                locations.append(
                    FabricRollLocation(
                        location_name=loc_name,
                        quantity=qty
                    )
                )

            if not locations:
                print("Nenhuma localização adicionada")
                return

            # 🔥 total automático

            total = sum(
                loc.quantity
                for loc in locations
            )

            roll = FabricRollModel(
                id=None,
                name=name,
                total_quantity=total,
                locations=locations
            )

            # 🔥 editar

            if self.roll:

                roll.id = self.roll.id

                self.service.update_roll(roll)

            # 🔥 criar

            else:

                self.service.create_roll(roll)

            if self.on_save:
                self.on_save()

            self.destroy()

        except Exception as e:

            print("Erro ao salvar:")
            print(e)

            self.save_button.configure(
                state="normal"
            )

    def _remove_location_row(self, row_frame):

        updated_rows = []

        for row_data in self.location_rows:

            if row_data["frame"] != row_frame:
                updated_rows.append(row_data)

        self.location_rows = updated_rows

        row_frame.destroy()