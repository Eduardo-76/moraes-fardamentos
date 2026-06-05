import customtkinter as ctk
from app.core.utils import format_datetime_local
from app.services.stock_movement_service import StockMovementService


class StockMovementHistoryDialog(ctk.CTkToplevel):
    def __init__(self, master, stock_id: int) -> None:
        super().__init__(master)

        self.stock_id = stock_id
        self.service = StockMovementService()

        self.title("Histórico de Movimentações")
        self.geometry("820x620")
        self.minsize(720, 520)

        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_list()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Histórico de Movimentações",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=16)

    def _build_list(self) -> None:
        scroll = ctk.CTkScrollableFrame(self)
        scroll.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        scroll.grid_columnconfigure(0, weight=1)

        movements = self.service.list_movements_by_stock_entry(self.stock_id)

        if not movements:
            label = ctk.CTkLabel(
                scroll,
                text="Nenhuma movimentação registrada.",
                font=ctk.CTkFont(size=15),
            )
            label.grid(row=0, column=0, padx=16, pady=16, sticky="w")
            return

        for index, movement in enumerate(movements):
            card = ctk.CTkFrame(scroll)
            card.grid(row=index, column=0, sticky="ew", padx=8, pady=8)
            card.grid_columnconfigure(0, weight=1)

            title = ctk.CTkLabel(
                card,
                text=f"{movement.movement_type} | Quantidade total: {movement.quantity}",
                font=ctk.CTkFont(size=18, weight="bold"),
            )
            title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 6))

            meta = ctk.CTkLabel(
                card,
                text=f"Data: {format_datetime_local(movement.created_at)}",
                font=ctk.CTkFont(size=13),
            )
            meta.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 6))

            if movement.notes:
                notes = ctk.CTkLabel(
                    card,
                    text=f"Observação: {movement.notes}",
                    font=ctk.CTkFont(size=13),
                    justify="left",
                )
                notes.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 6))

            lines = []
            for item in movement.items:
                lines.append(f"- {item.quantity} {item.size or 'Sem tamanho'} - {item.gender or 'Sem categoria'}")

            items_label = ctk.CTkLabel(
                card,
                text="\n".join(lines) if lines else "Sem itens detalhados.",
                justify="left",
                font=ctk.CTkFont(size=13),
            )
            items_label.grid(row=3, column=0, sticky="w", padx=16, pady=(0, 16))