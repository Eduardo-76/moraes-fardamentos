import customtkinter as ctk
from app.services.fabric_roll_service import FabricRollService


class FabricRollHistoryScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.service = FabricRollService()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Histórico de Malha",
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

            card = ctk.CTkFrame(
                self.list_frame,
                corner_radius=12,
                fg_color=("gray20", "gray20")
            )

            # título
            title = ctk.CTkLabel(
                card,
                text=mov["roll_name"],
                font=ctk.CTkFont(size=18, weight="bold"),
            )
            title.pack(anchor="w", padx=16, pady=(12, 4))

            # linha divisória
            separator = ctk.CTkFrame(
                card,
                height=2,
                fg_color="#2A2A2A"
            )
            separator.pack(fill="x", padx=12, pady=6)

            movement_type = mov["movement_type"]

            # 🔥 ENTRADA
            if movement_type == "entrada":

                color = "#4ADE80"

                details = f"""
            Local: {mov['location_name']}
            Quantidade: +{mov['quantity']}
            Data: {mov['created_at']}
            """

            # 🔥 SAÍDA
            elif movement_type == "saida":

                color = "#F87171"

                details = f"""
            Local: {mov['location_name']}
            Quantidade: -{mov['quantity']}
            Data: {mov['created_at']}
            """

            # 🔥 TRANSFERÊNCIA
            elif movement_type == "transferencia":

                color = "#A855F7"

                details = f"""
            {mov['from_location']} → {mov['to_location']}
            Quantidade: {mov['quantity']}
            Data: {mov['created_at']}
            """

            # 🔥 FALLBACK
            else:

                color = "white"

                details = f"""
            Movimentação desconhecida
            Data: {mov['created_at']}
            """

            details_label = ctk.CTkLabel(
                card,
                text=details.strip(),
                justify="left",
                text_color=color
            )

            details_label.pack(anchor="w", padx=16, pady=(4, 12))

            card.pack(fill="x", padx=12, pady=12)