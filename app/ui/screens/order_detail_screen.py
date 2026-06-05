import customtkinter as ctk
from app.services.audio_service import AudioService
from app.core.constants import MESSAGE_SECTORS, STAGE_STATUS_COLORS
from app.services.order_service import OrderService
from app.ui.dialogs.order_form_dialog import OrderFormDialog
from app.ui.dialogs.order_stock_withdraw_dialog import OrderStockWithdrawDialog
from app.services.stock_service import StockService


class OrderDetailScreen(ctk.CTkFrame):
    def __init__(self, master, order_id: int, on_back=None) -> None:
        super().__init__(master)

        self.order_id = order_id
        self.on_back = on_back
        self.order_service = OrderService()
        self.stock_service = StockService()
        self.stage_note_entries = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_content()

    def _build_header(self) -> None:
        header_frame = ctk.CTkFrame(self)
        header_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        header_frame.grid_columnconfigure(1, weight=1)

        back_button = ctk.CTkButton(
            header_frame,
            text="← Voltar",
            width=120,
            command=self._handle_back,
        )
        back_button.grid(row=0, column=0, padx=16, pady=16, sticky="w")

        title = ctk.CTkLabel(
            header_frame,
            text="Detalhes do Pedido",
            font=ctk.CTkFont(size=28, weight="bold"),
        )
        title.grid(row=0, column=1, padx=16, pady=16, sticky="w")

    def _build_content(self) -> None:
        self.content_frame = ctk.CTkScrollableFrame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=8, pady=8)
        self.content_frame.grid_columnconfigure(0, weight=1)

        self._render_content()

    def _render_content(self) -> None:
        self.stage_note_entries = {}

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        order = self.order_service.get_order_by_id(self.order_id)
        stages = self.order_service.list_order_stages(self.order_id)

        if not order:
            label = ctk.CTkLabel(
                self.content_frame,
                text="Pedido não encontrado.",
                font=ctk.CTkFont(size=16),
            )
            label.grid(row=0, column=0, padx=16, pady=16, sticky="w")
            return

        summary_frame = ctk.CTkFrame(self.content_frame)
        summary_frame.grid(row=0, column=0, sticky="ew", padx=8, pady=8)
        summary_frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            summary_frame,
            text=order.client_name or "Sem cliente",
            font=ctk.CTkFont(size=24, weight="bold"),
        )
        title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        command_text = self.order_service.build_order_command_text(self.order_id)

        self.command_box = ctk.CTkTextbox(summary_frame, height=220)
        self.command_box.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))
        self.command_box.insert("1.0", command_text)
        self.command_box.configure(state="disabled")

        summary_buttons = ctk.CTkFrame(summary_frame, fg_color="transparent")
        summary_buttons.grid(row=2, column=0, sticky="w", padx=16, pady=(0, 16))

        copy_command_button = ctk.CTkButton(
            summary_buttons,
            text="Copiar comanda",
            command=lambda: self._copy_text(command_text),
        )
        copy_command_button.grid(row=0, column=0, padx=(0, 8), pady=0)

        edit_button = ctk.CTkButton(
            summary_buttons,
            text="Editar pedido",
            command=self._open_edit_dialog,
        )
        edit_button.grid(row=0, column=1, padx=(0, 8), pady=0)

        withdraw_button = ctk.CTkButton(
            summary_buttons,
            text="Estoque já baixado" if order.stock_withdrawn else "Baixar do estoque",
            command=self._open_stock_withdraw_dialog,
        )
        withdraw_button.grid(row=0, column=2, padx=(0, 8), pady=0)

        simulate_button = ctk.CTkButton(
            summary_buttons,
            text="Simular reserva",
            command=self._simulate_stock_reservation,
        )

        simulate_button.grid(
            row=0,
            column=3,
            padx=(0, 8),
            pady=0
        )

        if order.stock_withdrawn:
            withdraw_button.configure(state="disabled")

        if order.audio_id:
            audio_service = AudioService()
            audio = audio_service.get_audio_by_id(order.audio_id)

            if audio:
                play_button = ctk.CTkButton(
                    summary_buttons,
                    text="Ouvir áudio",
                    command=lambda p=audio.file_path: audio_service.open_audio(p),
                )
                play_button.grid(row=0, column=4, padx=0, pady=0)

        actions_frame = ctk.CTkFrame(self.content_frame)
        actions_frame.grid(row=1, column=0, sticky="ew", padx=8, pady=8)

        prev_button = ctk.CTkButton(
            actions_frame,
            text="Voltar etapa",
            command=self._move_previous,
        )
        prev_button.grid(row=0, column=0, padx=16, pady=16, sticky="w")

        next_button = ctk.CTkButton(
            actions_frame,
            text="Avançar etapa",
            command=self._move_next,
        )
        next_button.grid(row=0, column=1, padx=16, pady=16, sticky="w")

        message_frame = ctk.CTkFrame(self.content_frame)
        message_frame.grid(row=2, column=0, sticky="ew", padx=8, pady=8)
        message_frame.grid_columnconfigure(1, weight=1)

        message_title = ctk.CTkLabel(
            message_frame,
            text="Gerar mensagem pronta",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        message_title.grid(row=0, column=0, columnspan=2, sticky="w", padx=16, pady=(16, 8))

        self.sector_option = ctk.CTkOptionMenu(
            message_frame,
            values=MESSAGE_SECTORS,
        )
        self.sector_option.grid(row=1, column=0, padx=16, pady=8, sticky="w")

        generate_button = ctk.CTkButton(
            message_frame,
            text="Gerar mensagem",
            command=self._generate_message,
        )
        generate_button.grid(row=1, column=1, padx=16, pady=8, sticky="w")

        self.message_box = ctk.CTkTextbox(message_frame, height=150)
        self.message_box.grid(row=2, column=0, columnspan=2, sticky="ew", padx=16, pady=8)

        copy_message_button = ctk.CTkButton(
            message_frame,
            text="Copiar mensagem",
            command=lambda: self._copy_text(self.message_box.get("1.0", "end").strip()),
        )
        copy_message_button.grid(row=3, column=0, padx=16, pady=(0, 16), sticky="w")

        timeline_frame = ctk.CTkFrame(self.content_frame)
        timeline_frame.grid(row=3, column=0, sticky="ew", padx=8, pady=8)
        timeline_frame.grid_columnconfigure(0, weight=1)

        timeline_title = ctk.CTkLabel(
            timeline_frame,
            text="Linha do tempo do pedido",
            font=ctk.CTkFont(size=22, weight="bold"),
        )
        timeline_title.grid(row=0, column=0, sticky="w", padx=16, pady=(16, 8))

        for index, stage in enumerate(stages, start=1):
            self._create_stage_row(timeline_frame, index, stage)

    def _create_stage_row(self, master, row_index: int, stage: dict) -> None:
        row_frame = ctk.CTkFrame(master)
        row_frame.grid(row=row_index, column=0, sticky="ew", padx=16, pady=8)
        row_frame.grid_columnconfigure(0, weight=1)

        stage_name = stage.get("stage_name", "Etapa")
        status = stage.get("status", "Em espera")
        color = STAGE_STATUS_COLORS.get(status, "#3B82F6")

        name_label = ctk.CTkLabel(
            row_frame,
            text=stage_name,
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        name_label.grid(row=0, column=0, sticky="w", padx=16, pady=(12, 4))

        status_label = ctk.CTkLabel(
            row_frame,
            text=status,
            fg_color=color,
            corner_radius=8,
            padx=10,
            pady=6,
        )
        status_label.grid(row=0, column=1, sticky="e", padx=16, pady=(12, 4))

        notes_entry = ctk.CTkTextbox(row_frame, height=80)
        notes_entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=8)
        notes_entry.insert("1.0", stage.get("notes") or "")

        save_button = ctk.CTkButton(
            row_frame,
            text="Salvar observação",
            command=lambda s=stage_name: self._save_stage_note(s),
        )
        save_button.grid(row=2, column=0, padx=16, pady=(0, 12), sticky="w")

        self.stage_note_entries[stage_name] = notes_entry

    def _save_stage_note(self, stage_name: str) -> None:
        entry = self.stage_note_entries.get(stage_name)
        if not entry:
            return

        notes = entry.get("1.0", "end").strip()
        self.order_service.save_stage_notes(self.order_id, stage_name, notes)
        self._render_content()

    def _move_next(self) -> None:
        self.order_service.move_to_next_stage(self.order_id)
        self._render_content()

    def _move_previous(self) -> None:
        self.order_service.move_to_previous_stage(self.order_id)
        self._render_content()

    def _generate_message(self) -> None:
        sector = self.sector_option.get()
        message = self.order_service.generate_stage_message(self.order_id, sector)

        self.message_box.delete("1.0", "end")
        self.message_box.insert("1.0", message)

    def _copy_text(self, text: str) -> None:
        if not text:
            return

        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()

    def _open_edit_dialog(self) -> None:
        OrderFormDialog(
            self,
            order_id=self.order_id,
            on_save=self._handle_order_updated,
        )

    def _open_stock_withdraw_dialog(self) -> None:
        OrderStockWithdrawDialog(
            self,
            order_id=self.order_id,
            on_save=self._handle_stock_withdraw,
        )

    def _handle_stock_withdraw(self) -> None:
        self._render_content()

    def _handle_order_updated(self, order_id: int) -> None:
        self.order_id = order_id
        self._render_content()

    def _handle_back(self) -> None:
        if callable(self.on_back):
            self.on_back()

    def _simulate_stock_reservation(self):

        order = self.order_service.get_order_by_id(
            self.order_id
        )

        if not order:
            return

        result = (
            self.stock_service
            .simulate_order_reservation(
                order.items
            )
        )

        text = ""

        for item in result:

            text += (
                f"{item['size']} "
                f"{item['gender']}\n"
                f"Pedido: {item['requested']}\n"
                f"Reservado: {item['reserved']}\n"
                f"Faltam: {item['missing']}\n\n"
            )

        dialog = ctk.CTkToplevel(self)

        dialog.title(
            "Simulação de Reserva"
        )

        dialog.geometry(
            "500x400"
        )

        textbox = ctk.CTkTextbox(
            dialog
        )

        textbox.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        textbox.insert(
            "1.0",
            text or "Nenhum item encontrado."
        )