import customtkinter as ctk

from app.models.fabric_roll_model import (
    FabricRollLocation,
    FabricRollModel,
)

from app.services.fabric_roll_service import FabricRollService


class FabricRollEditDialog(ctk.CTkToplevel):

    def __init__(self, master, roll, on_save=None):
        super().__init__(master)

        self.roll = roll
        self.on_save = on_save

        self.service = FabricRollService()

        self.title("Editar Rolo")
        self.geometry("400x500")

        self.transient(master)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):

        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(padx=20, pady=(20, 10), fill="x")

        self.name_entry.insert(0, self.roll.name)

        self.total_entry = ctk.CTkEntry(self)
        self.total_entry.pack(padx=20, pady=10, fill="x")

        self.total_entry.insert(0, str(self.roll.total_quantity))

        self.locations_box = ctk.CTkTextbox(
            self,
            height=250
        )
        self.locations_box.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        locations_text = ""

        for loc in self.roll.locations:
            locations_text += (
                f"{loc.location_name}: {loc.quantity}\n"
            )

        self.locations_box.insert(
            "1.0",
            locations_text.strip()
        )

        save_btn = ctk.CTkButton(
            self,
            text="Salvar",
            command=self._save
        )
        save_btn.pack(pady=20)

    def _save(self):

        try:

            name = self.name_entry.get().strip()

            total = int(
                self.total_entry.get()
            )

            lines = self.locations_box.get(
                "1.0",
                "end"
            ).strip().split("\n")

            locations = []

            for line in lines:

                if ":" not in line:
                    continue

                loc_name, qty = line.split(":")

                locations.append(
                    FabricRollLocation(
                        location_name=loc_name.strip(),
                        quantity=int(qty.strip())
                    )
                )

            roll = FabricRollModel(
                id=self.roll.id,
                name=name,
                total_quantity=total,
                locations=locations
            )

            self.service.update_roll(roll)

            if self.on_save:
                self.on_save()

            self.destroy()

        except Exception as e:
            print("Erro ao editar rolo:")
            print(e)