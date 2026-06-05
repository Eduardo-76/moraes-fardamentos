import customtkinter as ctk
from app.services.fabric_roll_service import FabricRollService


class MovementHistoryScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.service = FabricRollService()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Histórico de Movimentações",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        title.grid(row=0, column=0, padx=16, pady=16, sticky="w")

        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.grid(row=1, column=0, sticky="nsew", padx=16, pady=16)

        self.refresh()

    def refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        movements = self.service.movement_repo.list_all()

        for mov in movements:
            text = f"""
Rolo ID: {mov['roll_id']}
Local: {mov['location_name']}
Quantidade: {mov['quantity']}
Tipo: {mov['movement_type']}
Data: {mov['created_at']}
"""

            card = ctk.CTkFrame(self.list_frame, corner_radius=12)
            label = ctk.CTkLabel(card, text=text.strip(), justify="left")
            label.pack(padx=10, pady=10)

            card.pack(fill="x", padx=10, pady=10)