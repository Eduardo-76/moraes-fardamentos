import customtkinter as ctk

from app.services.stock_movement_service import StockMovementService
from app.services.stock_service import StockService


class StockMovementDialog(ctk.CTkToplevel):
    def __init__(self, master, stock_id: int, on_save=None) -> None:
        super().__init__(master)

        self.stock_id = stock_id
        self.on_save = on_save
        self.stock_service = StockService()
        self.movement_service = StockMovementService()
        self.item_rows = []

        self.stock = self.stock_service.get_stock_entry_by_id(stock_id)

        self.title("Movimentar Estoque")
        self.geometry("900x760")
        self.minsize(820, 620)

        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_body()
        self._build_footer()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Movimentar Estoque",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 6))

        subtitle_text = "Selecione entrada ou saída e informe as quantidades por variação."
        if self.stock:
            subtitle_text = (
                f"{self.stock.model or 'Sem modelo'} | {self.stock.type or 'Sem tipo'} | "
                f"{self.stock.color or 'Sem cor'}"
            )

        subtitle = ctk.CTkLabel(
            header,
            text=subtitle_text,
            font=ctk.CTkFont(size=14),
        )
        subtitle.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 16))

    def _build_body(self) -> None:
        self.body = ctk.CTkScrollableFrame(self)
        self.body.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.body.grid_columnconfigure(0, weight=1)

        type_frame = ctk.CTkFrame(self.body)
        type_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        type_frame.grid_columnconfigure(0, weight=1)

        type_label = ctk.CTkLabel(
            type_frame,
            text="Tipo de movimentação",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        type_label.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.type_option = ctk.CTkOptionMenu(type_frame, values=["Entrada", "Saída"])
        self.type_option.grid(row=1, column=0, sticky="w", padx=12, pady=(0, 12))
        self.type_option.set("Entrada")

        notes_frame = ctk.CTkFrame(self.body)
        notes_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=8)
        notes_frame.grid_columnconfigure(0, weight=1)

        notes_label = ctk.CTkLabel(
            notes_frame,
            text="Observação",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        notes_label.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.notes_box = ctk.CTkTextbox(notes_frame, height=100)
        self.notes_box.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))

        self.items_frame = ctk.CTkFrame(self.body)
        self.items_frame.grid(row=2, column=0, sticky="ew", padx=8, pady=8)
        self.items_frame.grid_columnconfigure(0, weight=1)

        items_title = ctk.CTkLabel(
            self.items_frame,
            text="Variações para movimentar",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        items_title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.items_rows_container = ctk.CTkFrame(self.items_frame)
        self.items_rows_container.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))
        self.items_rows_container.grid_columnconfigure(0, weight=1)

        self._build_item_rows()

    def _build_item_rows(self) -> None:
        if self.stock and self.stock.items:
            for item in self.stock.items:
                self._add_item_row(
                    size=item.size or "",
                    gender=item.gender or "",
                )
        else:
            self._add_item_row()

    def _add_item_row(self, size="", gender="") -> None:
        row_index = len(self.item_rows)

        row_frame = ctk.CTkFrame(self.items_rows_container)
        row_frame.grid(row=row_index, column=0, sticky="ew", padx=4, pady=6)
        row_frame.grid_columnconfigure((0, 1, 2), weight=1)

        size_entry = ctk.CTkEntry(row_frame, placeholder_text="Tamanho")
        size_entry.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
        if size:
            size_entry.insert(0, size)

        gender_entry = ctk.CTkEntry(row_frame, placeholder_text="Categoria / gênero")
        gender_entry.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        if gender:
            gender_entry.insert(0, gender)

        quantity_entry = ctk.CTkEntry(row_frame, placeholder_text="Quantidade")
        quantity_entry.grid(row=0, column=2, padx=8, pady=8, sticky="ew")

        self.item_rows.append(
            {
                "size": size_entry,
                "gender": gender_entry,
                "quantity": quantity_entry,
            }
        )

    def _build_footer(self) -> None:
        footer = ctk.CTkFrame(self)
        footer.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 12))

        cancel_button = ctk.CTkButton(
            footer,
            text="Cancelar",
            command=self.destroy,
            fg_color="#374151",
            hover_color="#1F2937",
        )
        cancel_button.grid(row=0, column=0, padx=12, pady=12, sticky="w")

        save_button = ctk.CTkButton(
            footer,
            text="Salvar movimentação",
            command=self._save,
        )
        save_button.grid(row=0, column=1, padx=12, pady=12, sticky="e")

    def _save(self) -> None:
        items = []
        for row in self.item_rows:
            size = row["size"].get().strip()
            gender = row["gender"].get().strip()
            quantity = row["quantity"].get().strip()

            if not size and not gender and not quantity:
                continue

            items.append(
                {
                    "size": size,
                    "gender": gender,
                    "quantity": quantity,
                }
            )

        try:
            self.movement_service.create_movement(
                stock_entry_id=self.stock_id,
                movement_type=self.type_option.get(),
                notes=self.notes_box.get("1.0", "end").strip(),
                items=items,
            )
        except Exception as error:
            error_dialog = ctk.CTkInputDialog(
                text=str(error),
                title="Erro na movimentação",
            )
            error_dialog.destroy()
            return

        if callable(self.on_save):
            self.on_save()

        self.destroy()