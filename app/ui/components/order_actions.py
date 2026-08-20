import customtkinter as ctk

from tkinter import filedialog, messagebox

from pathlib import Path
import shutil

from app.core.paths import ARTWORK_DIR


class OrderActions(ctk.CTkFrame):

    def __init__(
        self,
        master,
        order,
        callbacks: dict
    ):
        super().__init__(master)

        self.order = order
        self.callbacks = callbacks

        self._build()

    def _build(self):

        self.grid_columnconfigure(
            20,
            weight=1
        )

        withdraw_text = (
            "Estoque baixado"
            if self.order.stock_withdrawn
            else "Baixar estoque"
        )

        buttons = [
            ("Editar pedido", "edit"),
            ("Alterar status", "status"),

            ("◀ Etapa", "previous_stage"),
            ("Etapa ▶", "next_stage"),

            ("Simular reserva", "simulate"),
            ("Reservar estoque", "reserve"),
            (withdraw_text, "withdraw"),
            ("Cancelar reserva", "cancel_reservation"),
        ]
        
        column = 0

        # =====================================================
        # AÇÕES DO PEDIDO
        # =====================================================

        for text, key in buttons:

            button = ctk.CTkButton(
                self,
                text=text,
                command=self.callbacks.get(key)
            )

            if (
                key == "withdraw"
                and self.order.stock_withdrawn
            ):
                button.configure(
                    state="disabled"
                )

            button.grid(
                row=0,
                column=column,
                padx=(0, 8),
                pady=0
            )

            column += 1

        # =====================================================
        # ARTE
        # =====================================================

        artwork_button = ctk.CTkButton(
            self,
            text="Adicionar arte",
            command=self._add_artwork
        )

        artwork_button.grid(
            row=0,
            column=column,
            padx=(0, 8),
            pady=0
        )

        column += 1

        # =====================================================
        # COMANDA
        # =====================================================

        preview_button = ctk.CTkButton(
            self,
            text="Visualizar comanda",
            command=self.callbacks.get(
                "preview_command"
            )
        )

        preview_button.grid(
            row=0,
            column=column,
            padx=(0, 8),
            pady=0
        )

        column += 1

        export_button = ctk.CTkButton(
            self,
            text="Exportar PDF",
            command=self.callbacks.get(
                "export_command_pdf"
            )
        )

        export_button.grid(
            row=0,
            column=column,
            padx=(0, 8),
            pady=0
        )

        column += 1

        # =====================================================
        # ÁUDIO
        # =====================================================

        if (
            self.order.audio_id
            and self.callbacks.get("audio")
        ):

            audio_button = ctk.CTkButton(
                self,
                text="Ouvir áudio",
                command=self.callbacks["audio"]
            )

            audio_button.grid(
                row=0,
                column=column,
                padx=(0, 8),
                pady=0
            )

    def _add_artwork(self):

        file_path = filedialog.askopenfilename(
            title="Selecionar arte",
            filetypes=[
                (
                    "Imagens e PDF",
                    "*.png *.jpg *.jpeg *.webp *.pdf"
                ),
                (
                    "Imagens",
                    "*.png *.jpg *.jpeg *.webp"
                ),
                (
                    "PDF",
                    "*.pdf"
                ),
            ]
        )

        if not file_path:
            return

        artwork_dir = ARTWORK_DIR

        artwork_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        source = Path(file_path)

        extension = source.suffix.lower()

        destination = (
            artwork_dir
            / f"pedido_{self.order.id}{extension}"
        )

        # Remove arte anterior do mesmo pedido.
        for old_file in artwork_dir.glob(
            f"pedido_{self.order.id}.*"
        ):

            try:
                old_file.unlink()

            except OSError:
                pass

        shutil.copy2(
            source,
            destination
        )

        messagebox.showinfo(
            "Arte adicionada",
            "A arte foi adicionada à comanda."
        )