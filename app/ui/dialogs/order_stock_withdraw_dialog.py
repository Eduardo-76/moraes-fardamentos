import customtkinter as ctk

from app.services.order_service import OrderService
from app.services.stock_movement_service import StockMovementService
from app.services.stock_service import StockService


class OrderStockWithdrawDialog(ctk.CTkToplevel):
    def __init__(self, master, order_id: int, on_save=None) -> None:
        super().__init__(master)

        self.order_id = order_id
        self.on_save = on_save

        self.order_service = OrderService()
        self.stock_service = StockService()
        self.movement_service = StockMovementService()

        self.order = self.order_service.get_order_by_id(order_id)
        self.stock_entries = self.stock_service.list_stock_entries()
        self.item_rows = []

        self.title("Baixar Pedido do Estoque")
        self.geometry("940x780")
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
            text="Baixar Pedido do Estoque",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 6))

        subtitle = ctk.CTkLabel(
            header,
            text=f"Pedido: {self.order.client_name if self.order else 'Não encontrado'}",
            font=ctk.CTkFont(size=14),
        )
        subtitle.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 16))

    def _build_body(self) -> None:
        self.body = ctk.CTkScrollableFrame(self)
        self.body.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.body.grid_columnconfigure(0, weight=1)

        stock_frame = ctk.CTkFrame(self.body)
        stock_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        stock_frame.grid_columnconfigure(0, weight=1)

        stock_label = ctk.CTkLabel(
            stock_frame,
            text="Escolha o estoque de origem",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        stock_label.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.stock_options = self._build_stock_options()

        self.stock_option = ctk.CTkOptionMenu(
            stock_frame,
            values=list(self.stock_options.keys()) if self.stock_options else ["Nenhum estoque disponível"],
        )
        self.stock_option.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))

        notes_frame = ctk.CTkFrame(self.body)
        notes_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=8)
        notes_frame.grid_columnconfigure(0, weight=1)

        notes_label = ctk.CTkLabel(
            notes_frame,
            text="Observação",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        notes_label.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.notes_box = ctk.CTkTextbox(notes_frame, height=90)
        self.notes_box.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))
        self.notes_box.insert(
            "1.0",
            f"Baixa vinculada ao pedido #{self.order_id}"
            if self.order
            else "Baixa vinculada ao pedido",
        )

        self.items_frame = ctk.CTkFrame(self.body)
        self.items_frame.grid(row=2, column=0, sticky="ew", padx=8, pady=8)
        self.items_frame.grid_columnconfigure(0, weight=1)

        items_title = ctk.CTkLabel(
            self.items_frame,
            text="Itens para baixar",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        items_title.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.items_rows_container = ctk.CTkFrame(self.items_frame)
        self.items_rows_container.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))
        self.items_rows_container.grid_columnconfigure(0, weight=1)

        self._build_item_rows_from_order()

    def _build_stock_options(self) -> dict[str, int]:
        options = {}

        for stock in self.stock_entries:
            label = (
                f"#{stock.id} | {stock.model or 'Sem modelo'} | "
                f"{stock.type or 'Sem tipo'} | {stock.color or 'Sem cor'} | "
                f"{stock.stock_category or 'Sem categoria'} | "
                f"Ref: {stock.reference or 'Sem referência'} | "
                f"Qtd: {stock.total_quantity}"
            )
            options[label] = stock.id

        return options

    def _build_item_rows_from_order(self) -> None:
        if self.order and self.order.items:
            for item in self.order.items:
                self._add_item_row(
                    size=item.size or "",
                    gender=item.gender or "",
                    quantity=item.quantity or 0,
                )
        else:
            self._add_item_row()

    def _add_item_row(self, size="", gender="", quantity="") -> None:
        row_index = len(self.item_rows)

        row_frame = ctk.CTkFrame(self.items_rows_container)
        row_frame.grid(row=row_index, column=0, sticky="ew", padx=4, pady=6)
        row_frame.grid_columnconfigure((0, 1, 2), weight=1)

        size_entry = ctk.CTkEntry(row_frame, placeholder_text="Tamanho")
        size_entry.grid(row=0, column=0, padx=8, pady=8, sticky="ew")
        if size:
            size_entry.insert(0, str(size))

        gender_entry = ctk.CTkEntry(row_frame, placeholder_text="Categoria / gênero")
        gender_entry.grid(row=0, column=1, padx=8, pady=8, sticky="ew")
        if gender:
            gender_entry.insert(0, str(gender))

        quantity_entry = ctk.CTkEntry(row_frame, placeholder_text="Quantidade")
        quantity_entry.grid(row=0, column=2, padx=8, pady=8, sticky="ew")
        if quantity != "":
            quantity_entry.insert(0, str(quantity))

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
            text="Confirmar baixa",
            command=self._save,
        )
        save_button.grid(row=0, column=1, padx=12, pady=12, sticky="e")

    def _save(self) -> None:
        if not self.stock_options:
            return

        selected_label = self.stock_option.get()
        stock_id = self.stock_options.get(selected_label)

        if not stock_id:
            return

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
                stock_entry_id=stock_id,
                movement_type="Saída",
                notes=self.notes_box.get("1.0", "end").strip(),
                items=items,
            )

            self.stock_service.withdraw_order_stock(
                self.order_id
            )
           
            self.order_service.mark_stock_withdrawn(self.order_id)
        except Exception as error:
            error_window = ctk.CTkToplevel(self)
            error_window.title("Erro na baixa")
            error_window.geometry("520x220")
            error_window.transient(self)
            error_window.grab_set()

            label = ctk.CTkLabel(
                error_window,
                text=str(error),
                wraplength=460,
                font=ctk.CTkFont(size=14),
            )
            label.pack(padx=24, pady=(30, 20))

            close_button = ctk.CTkButton(
                error_window,
                text="Fechar",
                command=error_window.destroy,
            )
            close_button.pack(pady=(0, 20))
            return

        if callable(self.on_save):
            self.on_save()

        self.destroy()