import customtkinter as ctk

from app.services.stock_movement_service import StockMovementService
from app.services.stock_service import StockService


class StockConversionDialog(ctk.CTkToplevel):
    def __init__(self, master, stock_id: int, on_save=None) -> None:
        super().__init__(master)

        self.stock_id = stock_id
        self.on_save = on_save
        self.stock_service = StockService()
        self.movement_service = StockMovementService()
        self.item_rows = []

        self.stock = self.stock_service.get_stock_entry_by_id(stock_id)

        self.title("Converter Estoque")
        self.geometry("940x800")
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
            text="Converter Base em Finalizado",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 6))

        subtitle_text = "Escolha as quantidades que sairão do estoque base e virarão estoque finalizado."
        if self.stock:
            subtitle_text = (
                f"Origem: {self.stock.model or 'Sem modelo'} | "
                f"{self.stock.type or 'Sem tipo'} | "
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
        self.body.grid_columnconfigure(1, weight=1)

        self.model_entry = self._create_entry("Modelo finalizado", 0, 0)
        self.type_entry = self._create_entry("Tipo", 0, 1)
        self.color_entry = self._create_entry("Cor", 1, 0)
        self.fabric_entry = self._create_entry("Tecido", 1, 1)
        self.group_entry = self._create_entry("Grupo", 2, 0)
        self.reference_entry = self._create_entry("Referência / Colégio / Cliente", 2, 1)

        if self.stock:
            self.model_entry.insert(0, self.stock.model or "")
            self.type_entry.insert(0, self.stock.type or "")
            self.color_entry.insert(0, self.stock.color or "")
            self.fabric_entry.insert(0, self.stock.fabric or "")
            self.group_entry.insert(0, self.stock.stock_group or "")

        notes_frame = ctk.CTkFrame(self.body)
        notes_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=8, pady=8)
        notes_frame.grid_columnconfigure(0, weight=1)

        notes_label = ctk.CTkLabel(
            notes_frame,
            text="Observação",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        notes_label.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.notes_box = ctk.CTkTextbox(notes_frame, height=90)
        self.notes_box.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))

        self.items_frame = ctk.CTkFrame(self.body)
        self.items_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=8, pady=8)
        self.items_frame.grid_columnconfigure(0, weight=1)

        items_title = ctk.CTkLabel(
            self.items_frame,
            text="Quantidades para converter",
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
                    available=item.quantity,
                )
        else:
            self._add_item_row()

    def _add_item_row(self, size="", gender="", available="") -> None:
        row_index = len(self.item_rows)

        row_frame = ctk.CTkFrame(self.items_rows_container)
        row_frame.grid(row=row_index, column=0, sticky="ew", padx=4, pady=6)
        row_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        size_entry = ctk.CTkEntry(row_frame, placeholder_text="Tamanho")
        size_entry.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
        if size:
            size_entry.insert(0, size)

        gender_entry = ctk.CTkEntry(row_frame, placeholder_text="Categoria / gênero")
        gender_entry.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        if gender:
            gender_entry.insert(0, gender)

        available_label = ctk.CTkLabel(
            row_frame,
            text=f"Disponível: {available}",
            font=ctk.CTkFont(size=13),
        )
        available_label.grid(row=0, column=2, padx=8, pady=8, sticky="w")

        quantity_entry = ctk.CTkEntry(row_frame, placeholder_text="Converter")
        quantity_entry.grid(row=0, column=3, padx=8, pady=8, sticky="ew")

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
            text="Converter estoque",
            command=self._save,
        )
        save_button.grid(row=0, column=1, padx=12, pady=12, sticky="e")

    def _create_entry(self, label_text: str, row: int, column: int):
        frame = ctk.CTkFrame(self.body)
        frame.grid(row=row, column=column, sticky="ew", padx=8, pady=8)
        frame.grid_columnconfigure(0, weight=1)

        label = ctk.CTkLabel(
            frame,
            text=label_text,
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        label.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        entry = ctk.CTkEntry(frame)
        entry.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))
        return entry

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
            self.movement_service.convert_base_to_finished(
                source_stock_id=self.stock_id,
                target_model=self.model_entry.get().strip(),
                target_type=self.type_entry.get().strip(),
                target_color=self.color_entry.get().strip(),
                target_fabric=self.fabric_entry.get().strip(),
                target_group=self.group_entry.get().strip(),
                target_reference=self.reference_entry.get().strip(),
                notes=self.notes_box.get("1.0", "end").strip(),
                items=items,
            )
        except Exception as error:
            dialog = ctk.CTkInputDialog(
                text=str(error),
                title="Erro na conversão",
            )
            dialog.destroy()
            return

        if callable(self.on_save):
            self.on_save()

        self.destroy()