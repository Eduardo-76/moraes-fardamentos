import customtkinter as ctk

from app.core.constants import PRIORITIES
from app.core.utils import (
    normalize_city,
    normalize_gender,
    normalize_int,
    normalize_money,
    normalize_name,
    normalize_phone,
    normalize_size,
    normalize_text,
)
from app.services.order_service import OrderService


class OrderFormDialog(ctk.CTkToplevel):
    def __init__(self, master, on_save=None, order_id: int | None = None, initial_data: dict | None = None) -> None:
        super().__init__(master)

        self.on_save = on_save
        self.order_service = OrderService()
        self.item_rows = []
        self.order_id = order_id
        self.initial_data = initial_data or {}
        self.is_edit_mode = order_id is not None

        self.title("Editar Pedido" if self.is_edit_mode else "Novo Pedido")
        self.geometry("900x720")
        self.minsize(820, 620)

        self.transient(master)
        self.grab_set()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_body()
        self._build_footer()

        if self.is_edit_mode:
            self._load_order_data()
        elif self.initial_data:
            self._load_initial_data()

    def _load_initial_data(self) -> None:
        data = self.initial_data

        if data.get("client_name"):
            self.client_entry.insert(0, data["client_name"])

        if data.get("model"):
            self.model_entry.insert(0, data["model"])

        if data.get("fabric"):
            self.fabric_entry.insert(0, data["fabric"])

        if data.get("quantity"):
            self.quantity_entry.insert(0, str(data["quantity"]))

        if data.get("deadline"):
            self.deadline_entry.insert(0, data["deadline"])

        self.type_entry.insert(0, data.get("order_type") or "Estampada Toda")

        notes = []
        if data.get("color"):
            notes.append(f"Cor informada no áudio: {data['color']}")
        if data.get("deadline_text"):
            notes.append(f"Prazo falado no áudio: {data['deadline_text']}")
        if data.get("raw_text"):
            notes.append(f"Texto do áudio: {data['raw_text']}")

        if notes:
            self.notes_box.insert("1.0", "\n".join(notes))

        for item in self.item_rows:
            item["frame"].destroy()
        self.item_rows = []

        for item in data.get("items", []):
            self._add_item_row(
                size=item.get("size") or "",
                gender=item.get("gender") or "",
                quantity=item.get("quantity") or "",
            )

        if not self.item_rows:
            self._add_item_row()



    def _build_header(self) -> None:
        header = ctk.CTkFrame(self)
        header.grid(row=0, column=0, sticky="ew", padx=12, pady=12)
        header.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            header,
            text="Editar Pedido" if self.is_edit_mode else "Novo Pedido",
            font=ctk.CTkFont(size=26, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 6))

        subtitle = ctk.CTkLabel(
            header,
            text="Preencha os dados principais e os tamanhos do pedido.",
            font=ctk.CTkFont(size=14),
        )
        subtitle.grid(row=1, column=0, sticky="w", padx=16, pady=(0, 16))

    def _build_body(self) -> None:
        self.body = ctk.CTkScrollableFrame(self)
        self.body.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.body.grid_columnconfigure(0, weight=1)
        self.body.grid_columnconfigure(1, weight=1)

        self.client_entry = self._create_entry("Cliente", 0, 0)
        self.phone_entry = self._create_entry("Contato", 0, 1)
        self.city_entry = self._create_entry("Cidade", 1, 0)
        self.model_entry = self._create_entry("Modelo", 1, 1)
        self.type_entry = self._create_entry("Tipo", 2, 0)
        self.fabric_entry = self._create_entry("Tecido", 2, 1)
        self.quantity_entry = self._create_entry("Quantidade total", 3, 0)
        self.deadline_entry = self._create_entry("Prazo (YYYY-MM-DD)", 3, 1)
        self.total_value_entry = self._create_entry("Valor total", 4, 0)

        priority_frame = ctk.CTkFrame(self.body)
        priority_frame.grid(row=4, column=1, sticky="ew", padx=8, pady=8)
        priority_frame.grid_columnconfigure(0, weight=1)

        priority_label = ctk.CTkLabel(
            priority_frame,
            text="Prioridade",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        priority_label.grid(row=0, column=0, sticky="w", padx=12, pady=(12, 6))

        self.priority_option = ctk.CTkOptionMenu(priority_frame, values=PRIORITIES)
        self.priority_option.grid(row=1, column=0, sticky="ew", padx=12, pady=(0, 12))
        self.priority_option.set("Média")

        notes_frame = ctk.CTkFrame(self.body)
        notes_frame.grid(row=5, column=0, columnspan=2, sticky="ew", padx=8, pady=8)
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
        self.items_frame.grid(row=6, column=0, columnspan=2, sticky="ew", padx=8, pady=8)
        self.items_frame.grid_columnconfigure(0, weight=1)

        items_title = ctk.CTkLabel(
            self.items_frame,
            text="Itens do pedido",
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
            text="Salvar alterações" if self.is_edit_mode else "Salvar pedido",
            command=self._save_order,
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

    def _load_order_data(self) -> None:
        if not self.order_id:
            return

        order = self.order_service.get_order_by_id(self.order_id)
        if not order:
            return

        if order.client_name:
            self.client_entry.insert(0, order.client_name)
        if order.client_phone:
            self.phone_entry.insert(0, order.client_phone)
        if order.client_city:
            self.city_entry.insert(0, order.client_city)
        if order.model:
            self.model_entry.insert(0, order.model)
        if order.type:
            self.type_entry.insert(0, order.type)
        if order.fabric:
            self.fabric_entry.insert(0, order.fabric)
        if order.quantity is not None:
            self.quantity_entry.insert(0, str(order.quantity))
        if order.deadline:
            self.deadline_entry.insert(0, order.deadline)
        if order.total_value is not None:
            self.total_value_entry.insert(0, str(order.total_value))
        if order.priority:
            self.priority_option.set(order.priority)
        if order.notes:
            self.notes_box.insert("1.0", order.notes)

        for item in self.item_rows:
            item["frame"].destroy()
        self.item_rows = []

        if order.items:
            for item in order.items:
                self._add_item_row(
                    size=item.size or "",
                    gender=item.gender or "",
                    quantity=item.quantity or "",
                )
        else:
            self._add_item_row()

    def _save_order(self) -> None:
        items = []

        for item in self.item_rows:
            raw_size = item["size"].get().strip()
            raw_gender = item["gender"].get().strip()
            raw_quantity = item["quantity"].get().strip()

            if not raw_size and not raw_gender and not raw_quantity:
                continue

            normalized_item = {
                "size": normalize_size(raw_size),
                "gender": normalize_gender(raw_gender),
                "quantity": normalize_int(raw_quantity),
            }

            items.append(normalized_item)

        total_quantity = normalize_int(self.quantity_entry.get())
        total_value = normalize_money(self.total_value_entry.get())

        payload = {
            "client_name": normalize_name(self.client_entry.get()),
            "audio_id": self.initial_data.get("audio_id"),
            "client_phone": normalize_phone(self.phone_entry.get()),
            "client_city": normalize_city(self.city_entry.get()),
            "model": normalize_text(self.model_entry.get()),
            "fabric": normalize_text(self.fabric_entry.get()),
            "order_type": normalize_text(self.type_entry.get()),
            "quantity": total_quantity,
            "deadline": normalize_text(self.deadline_entry.get()),
            "priority": self.priority_option.get(),
            "total_value": total_value,
            "notes": normalize_text(self.notes_box.get("1.0", "end")),
            "items": items,
        }

        if self.is_edit_mode and self.order_id:
            self.order_service.update_order(
                order_id=self.order_id,
                **payload,
            )
            saved_order_id = self.order_id
        else:
            saved_order_id = self.order_service.create_order(**payload)

        if callable(self.on_save):
            self.on_save(saved_order_id)

        self.destroy()