import customtkinter as ctk

from app.core.utils import (
    normalize_gender,
    normalize_int,
    normalize_size,
)
from app.services.stock_service import StockService


class StockFormDialog(ctk.CTkToplevel):
    def __init__(self, master, on_save=None, stock_id: int | None = None) -> None:
        super().__init__(master)

        self.on_save = on_save
        self.stock_id = stock_id
        self.is_edit_mode = stock_id is not None
        self.stock_service = StockService()
        self.item_rows = []

        self.title("Editar Estoque" if self.is_edit_mode else "Novo Estoque")
        self.geometry("920x760")
        self.minsize(820, 620)

        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_body()
        self._build_footer()

        if self.is_edit_mode:
            self._load_data()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Editar Estoque" if self.is_edit_mode else "Novo Estoque",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 6))

        subtitle = ctk.CTkLabel(
            header,
            text="Cadastre o item principal e suas variações por tamanho e gênero.",
            font=ctk.CTkFont(size=14),
        )
        subtitle.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 16))

    def _build_body(self) -> None:
        self.body = ctk.CTkScrollableFrame(self)
        self.body.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_columnconfigure(1, weight=1)

        self.model_entry = self._create_entry("Modelo", 0, 0)
        self.type_entry = self._create_entry("Tipo", 0, 1)
        self.color_entry = self._create_entry("Cor", 1, 0)
        self.fabric_entry = self._create_entry("Tecido", 1, 1)
        self.group_entry = self._create_entry("Grupo", 2, 0)
        self.category_entry = self._create_entry("Categoria do estoque", 2, 1)
        self.reference_entry = self._create_entry("Referência", 3, 0)
        self.total_quantity_entry = self._create_entry("Quantidade total", 3, 1)
        self.total_quantity_entry.configure(state="readonly")

        notes_frame = ctk.CTkFrame(self.body)
        notes_frame.grid(row=4, column=0, columnspan=2, sticky="ew", padx=8, pady=8)
        notes_frame.grid_columnconfigure(0, weight=1)

        notes_label = ctk.CTkLabel(
            notes_frame,
            text="Observação",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        notes_label.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.notes_box = ctk.CTkTextbox(notes_frame, height=100)
        self.notes_box.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))

        self._build_items_section()

    def _build_items_section(self) -> None:
        self.items_frame = ctk.CTkFrame(self.body)
        self.items_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=8, pady=8)
        self.items_frame.grid_columnconfigure(0, weight=1)

        items_title = ctk.CTkLabel(
            self.items_frame,
            text="Variações do estoque",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        items_title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        add_item_button = ctk.CTkButton(
            self.items_frame,
            text="Adicionar linha",
            command=self._add_item_row,
        )
        add_item_button.grid(row=0, column=1, sticky="e", padx=12, pady=(12, 6))

        self.items_rows_container = ctk.CTkFrame(self.items_frame)
        self.items_rows_container.grid(row=1, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 12))
        self.items_rows_container.grid_columnconfigure(0, weight=1)

        self._add_item_row()
        self._add_item_row()

    def _add_item_row(self, size="", gender="", quantity="") -> None:
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
        if quantity != "":
            quantity_entry.insert(0, str(quantity))

        quantity_entry.bind(
            "<KeyRelease>",
            lambda _event: self._update_total_quantity()
        )

        remove_button = ctk.CTkButton(
            row_frame,
            text="Remover",
            width=90,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=lambda rf=row_frame: self._remove_item_row(rf),
        )
        remove_button.grid(row=0, column=3, padx=8, pady=8)

        self.item_rows.append(
            {
                "frame": row_frame,
                "size": size_entry,
                "gender": gender_entry,
                "quantity": quantity_entry,
            }
        )

        self._update_total_quantity()

    def _update_total_quantity(self) -> None:
        total = 0

        for item in self.item_rows:
            raw_quantity = item["quantity"].get().strip()

            if not raw_quantity:
                continue

            try:
                quantity = int(raw_quantity)
            except ValueError:
                continue

            if quantity > 0:
                total += quantity

        self.total_quantity_entry.configure(state="normal")
        self.total_quantity_entry.delete(0, "end")
        self.total_quantity_entry.insert(0, str(total))
        self.total_quantity_entry.configure(state="readonly")

    def _remove_item_row(self, row_frame) -> None:
        if len(self.item_rows) <= 1:
            return

        remaining = []
        for item in self.item_rows:
            if item["frame"] == row_frame:
                item["frame"].destroy()
            else:
                remaining.append(item)

        self.item_rows = remaining
        self._rebuild_item_rows()
        self._update_total_quantity()

    def _rebuild_item_rows(self) -> None:
        for index, item in enumerate(self.item_rows):
            item["frame"].grid_configure(row=index)

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
            text="Salvar alterações" if self.is_edit_mode else "Salvar estoque",
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

    def _load_data(self) -> None:
        if not self.stock_id:
            return

        stock = self.stock_service.get_stock_entry_by_id(self.stock_id)
        if not stock:
            return

        if stock.model:
            self.model_entry.insert(0, stock.model)
        if stock.type:
            self.type_entry.insert(0, stock.type)
        if stock.color:
            self.color_entry.insert(0, stock.color)
        if stock.fabric:
            self.fabric_entry.insert(0, stock.fabric)
        if stock.stock_group:
            self.group_entry.insert(0, stock.stock_group)
        if stock.stock_category:
            self.category_entry.insert(0, stock.stock_category)
        if stock.reference:
            self.reference_entry.insert(0, stock.reference)
        self.total_quantity_entry.configure(state="normal")
        self.total_quantity_entry.delete(0, "end")
        self.total_quantity_entry.insert(0, str(stock.total_quantity))
        self.total_quantity_entry.configure(state="readonly")
        if stock.notes:
            self.notes_box.insert("1.0", stock.notes)

        for item in self.item_rows:
            item["frame"].destroy()
        self.item_rows = []

        if stock.items:
            for item in stock.items:
                self._add_item_row(
                    size=item.size or "",
                    gender=item.gender or "",
                    quantity=item.quantity or "",
                )
        else:
            self._add_item_row()

    def _save(self) -> None:
        items = []

        for item in self.item_rows:
            raw_size = item["size"].get().strip()
            raw_gender = item["gender"].get().strip()
            raw_quantity = item["quantity"].get().strip()

            if not raw_size and not raw_gender and not raw_quantity:
                continue

            items.append(
                {
                    "size": normalize_size(raw_size),
                    "gender": normalize_gender(raw_gender),
                    "quantity": normalize_int(raw_quantity),
                }
            )

        self._update_total_quantity()

        payload = {
            "model": self.model_entry.get(),
            "type": self.type_entry.get(),
            "color": self.color_entry.get(),
            "fabric": self.fabric_entry.get(),
            "stock_group": self.group_entry.get(),
            "stock_category": self.category_entry.get(),
            "reference": self.reference_entry.get(),
            "total_quantity": self.total_quantity_entry.get(),
            "notes": self.notes_box.get("1.0", "end").strip(),
            "items": items,
        }

        if self.is_edit_mode and self.stock_id:
            self.stock_service.update_stock_entry(self.stock_id, **payload)
            saved_id = self.stock_id
        else:
            saved_id = self.stock_service.create_stock_entry(**payload)

        if callable(self.on_save):
            self.on_save(saved_id)

        self.destroy()