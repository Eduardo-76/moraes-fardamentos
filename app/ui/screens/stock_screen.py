import customtkinter as ctk

from app.services.stock_service import StockService
from app.ui.dialogs.stock_conversion_dialog import StockConversionDialog
from app.ui.dialogs.stock_form_dialog import StockFormDialog
from app.ui.dialogs.stock_movement_dialog import StockMovementDialog
from app.ui.dialogs.stock_movement_history_dialog import StockMovementHistoryDialog


class StockScreen(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master)

        self.stock_service = StockService()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self._build_header()
        self._build_filters()
        self._build_list()
        self.refresh_items()

    def _build_header(self) -> None:
        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Estoque",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 4))

        subtitle = ctk.CTkLabel(
            header,
            text="Controle agrupado dos itens base e finalizados.",
            font=ctk.CTkFont(size=14),
        )
        subtitle.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 12))

        buttons_frame = ctk.CTkFrame(header, fg_color="transparent")
        buttons_frame.grid(row=0, column=1, rowspan=2, padx=16, pady=16, sticky="e")

        new_button = ctk.CTkButton(
            buttons_frame,
            text="Novo estoque",
            command=self._open_new_dialog,
        )
        new_button.grid(row=0, column=0, padx=(0, 8))

        refresh_button = ctk.CTkButton(
            buttons_frame,
            text="Atualizar",
            command=self.refresh_items,
        )
        refresh_button.grid(row=0, column=1)

    def _build_filters(self) -> None:
        filters = ctk.CTkFrame(self)
        filters.grid(row=1, column=0, sticky="ew", padx=8, pady=(0, 8))
        filters.grid_columnconfigure(0, weight=2)
        filters.grid_columnconfigure(1, weight=1)
        filters.grid_columnconfigure(2, weight=1)
        filters.grid_columnconfigure(3, weight=1)
        filters.grid_columnconfigure(4, weight=1)

        self.search_entry = ctk.CTkEntry(
            filters,
            placeholder_text="Buscar por modelo, tipo, cor ou referência...",
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=8, pady=12)
        self.search_entry.bind("<KeyRelease>", lambda _event: self.refresh_items())

        self.category_filter = ctk.CTkOptionMenu(
            filters,
            values=["Todas categorias", "Base", "Finalizado"],
            command=lambda _value: self.refresh_items(),
        )
        self.category_filter.grid(row=0, column=1, sticky="ew", padx=8, pady=12)
        self.category_filter.set("Todas categorias")

        self.group_entry = ctk.CTkEntry(
            filters,
            placeholder_text="Grupo",
        )
        self.group_entry.grid(row=0, column=2, sticky="ew", padx=8, pady=12)
        self.group_entry.bind("<KeyRelease>", lambda _event: self.refresh_items())

        self.size_entry = ctk.CTkEntry(
            filters,
            placeholder_text="Tamanho",
        )
        self.size_entry.grid(row=0, column=3, sticky="ew", padx=8, pady=12)
        self.size_entry.bind("<KeyRelease>", lambda _event: self.refresh_items())

        self.gender_entry = ctk.CTkEntry(
            filters,
            placeholder_text="Gênero/categoria",
        )
        self.gender_entry.grid(row=0, column=4, sticky="ew", padx=8, pady=12)
        self.gender_entry.bind("<KeyRelease>", lambda _event: self.refresh_items())

        clear_button = ctk.CTkButton(
            filters,
            text="Limpar filtros",
            command=self._clear_filters,
        )
        clear_button.grid(row=0, column=5, sticky="ew", padx=8, pady=12)

    def _build_list(self) -> None:
        self.list_frame = ctk.CTkScrollableFrame(self)
        self.list_frame.grid(row=2, column=0, sticky="nsew", padx=8, pady=8)
        self.list_frame.grid_columnconfigure(0, weight=1)

    def refresh_items(self) -> None:
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        items = self._apply_filters(self.stock_service.list_stock_entries())

        if not items:
            label = ctk.CTkLabel(
                self.list_frame,
                text="Nenhum estoque encontrado com os filtros atuais.",
                font=ctk.CTkFont(size=15),
            )
            label.grid(row=0, column=0, padx=16, pady=16, sticky="w")
            return

        for index, item in enumerate(items):
            card = self._create_stock_card(item)
            card.grid(row=index, column=0, sticky="ew", padx=8, pady=8)

    def _apply_filters(self, items):
        search = self.search_entry.get().strip().lower()
        category = self.category_filter.get()
        group = self.group_entry.get().strip().lower()
        size = self.size_entry.get().strip().upper()
        gender = self.gender_entry.get().strip().lower()

        filtered = []

        for item in items:
            if search:
                searchable_text = " ".join(
                    [
                        item.model or "",
                        item.type or "",
                        item.color or "",
                        item.fabric or "",
                        item.stock_group or "",
                        item.stock_category or "",
                        item.reference or "",
                        item.notes or "",
                    ]
                ).lower()

                if search not in searchable_text:
                    continue

            if category != "Todas categorias":
                if item.stock_category != category:
                    continue

            if group:
                item_group = (item.stock_group or "").lower()
                if group not in item_group:
                    continue

            if size:
                if not any((stock_item.size or "").upper() == size for stock_item in item.items):
                    continue

            if gender:
                if not any(gender in (stock_item.gender or "").lower() for stock_item in item.items):
                    continue

            filtered.append(item)

        return filtered

    def _create_stock_card(self, item) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(self.list_frame)
        frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            frame,
            text=f"{item.model or 'Sem modelo'} | {item.type or 'Sem tipo'} | {item.color or 'Sem cor'}",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        reference_text = item.reference or "Sem referência"

        details = ctk.CTkLabel(
            frame,
            text=(
                f"Tecido: {item.fabric or 'Não informado'}\n"
                f"Grupo: {item.stock_group or 'Não informado'}\n"
                f"Categoria do estoque: {item.stock_category or 'Não informado'}\n"
                f"Referência: {reference_text}\n"
                f"Quantidade total: {item.total_quantity}"
            ),
            justify="left",
            font=ctk.CTkFont(size=14),
        )
        details.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 8))

        items_text = self._build_items_text(item)
        items_label = ctk.CTkLabel(
            frame,
            text=items_text,
            justify="left",
            font=ctk.CTkFont(size=14),
        )
        items_label.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 12))

        actions = ctk.CTkFrame(frame, fg_color="transparent")
        actions.grid(row=0, column=1, rowspan=3, padx=16, pady=16, sticky="e")

        move_button = ctk.CTkButton(
            actions,
            text="Movimentar",
            width=110,
            command=lambda sid=item.id: self._open_movement_dialog(sid),
        )
        move_button.grid(row=0, column=0, padx=(0, 8), pady=(0, 8))

        convert_button = ctk.CTkButton(
            actions,
            text="Converter",
            width=110,
            command=lambda sid=item.id: self._open_conversion_dialog(sid),
        )
        convert_button.grid(row=1, column=0, padx=(0, 8), pady=(0, 8))

        if item.stock_category != "Base":
            convert_button.configure(state="disabled")

        history_button = ctk.CTkButton(
            actions,
            text="Histórico",
            width=110,
            command=lambda sid=item.id: self._open_history_dialog(sid),
        )
        history_button.grid(row=2, column=0, padx=(0, 8), pady=(0, 8))

        edit_button = ctk.CTkButton(
            actions,
            text="Editar",
            width=110,
            command=lambda sid=item.id: self._open_edit_dialog(sid),
        )
        edit_button.grid(row=3, column=0, padx=(0, 8), pady=(0, 8))

        delete_button = ctk.CTkButton(
            actions,
            text="Excluir",
            width=110,
            fg_color="#B91C1C",
            hover_color="#991B1B",
            command=lambda sid=item.id: self._delete_item(sid),
        )
        delete_button.grid(row=4, column=0, padx=(0, 8), pady=0)

        return frame

    def _build_items_text(self, item) -> str:
        if not item.items:
            return "Sem detalhamento de tamanhos."

        lines = ["Variações:"]
        for stock_item in item.items:
            lines.append(
                f"- {stock_item.quantity} {stock_item.size or 'Sem tamanho'} - {stock_item.gender or 'Sem categoria'}"
            )
        return "\n".join(lines)

    def _clear_filters(self) -> None:
        self.search_entry.delete(0, "end")
        self.category_filter.set("Todas categorias")
        self.group_entry.delete(0, "end")
        self.size_entry.delete(0, "end")
        self.gender_entry.delete(0, "end")
        self.refresh_items()

    def _open_new_dialog(self) -> None:
        StockFormDialog(self, on_save=self._handle_saved)

    def _open_edit_dialog(self, stock_id: int) -> None:
        StockFormDialog(self, stock_id=stock_id, on_save=self._handle_saved)

    def _open_movement_dialog(self, stock_id: int) -> None:
        StockMovementDialog(self, stock_id=stock_id, on_save=self.refresh_items)

    def _open_conversion_dialog(self, stock_id: int) -> None:
        StockConversionDialog(self, stock_id=stock_id, on_save=self.refresh_items)

    def _open_history_dialog(self, stock_id: int) -> None:
        StockMovementHistoryDialog(self, stock_id=stock_id)

    def _delete_item(self, stock_id: int) -> None:
        self.stock_service.delete_stock_entry(stock_id)
        self.refresh_items()

    def _handle_saved(self, _stock_id: int) -> None:
        self.refresh_items()