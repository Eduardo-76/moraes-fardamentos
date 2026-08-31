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
        super().__init__(
            master,
            fg_color="transparent"
        )

        self.order = order
        self.callbacks = callbacks

        self._build()

    # =====================================================
    # CONFIGURAÇÃO
    # =====================================================

    def _configure_columns(self, frame):

        for column in range(2):
            frame.grid_columnconfigure(
                column,
                weight=1
            )

    # =====================================================
    # BOTÃO
    # =====================================================

    def _create_button(
        self,
        parent,
        text,
        key,
        row,
        column,
        columnspan=1
    ):

        button = ctk.CTkButton(
            parent,
            text=text,
            command=self.callbacks.get(key),
            height=38
        )

        if (
            key == "withdraw"
            and self.order.stock_withdrawn
        ):
            button.configure(
                state="disabled"
            )

        button.grid(
            row=row,
            column=column,
            columnspan=columnspan,
            padx=4,
            pady=4,
            sticky="ew"
        )

        return button

    # =====================================================
    # CONSTRUÇÃO
    # =====================================================

    def _build(self):

        # =================================================
        # AÇÕES DO PEDIDO
        # =================================================

        order_frame = ctk.CTkFrame(
            self
        )

        order_frame.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=0,
            pady=(0, 8)
        )

        self._configure_columns(order_frame)

        title = ctk.CTkLabel(
            order_frame,
            text="Ações do pedido",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=8,
            pady=(8, 4)
        )

        self._create_button(
            order_frame,
            "Editar pedido",
            "edit",
            1,
            0
        )

        self._create_button(
            order_frame,
            "Alterar status",
            "status",
            1,
            1
        )

        # =================================================
        # PRODUÇÃO
        # =================================================

        production_frame = ctk.CTkFrame(
            self
        )

        production_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=0,
            pady=(0, 8)
        )

        self._configure_columns(
            production_frame
        )

        title = ctk.CTkLabel(
            production_frame,
            text="Produção",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=8,
            pady=(8, 4)
        )

        self._create_button(
            production_frame,
            "◀ Etapa anterior",
            "previous_stage",
            1,
            0
        )

        self._create_button(
            production_frame,
            "Próxima etapa ▶",
            "next_stage",
            1,
            1
        )

        # =================================================
        # ESTOQUE
        # =================================================

        stock_frame = ctk.CTkFrame(
            self
        )

        stock_frame.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=0,
            pady=(0, 8)
        )

        self._configure_columns(
            stock_frame
        )

        title = ctk.CTkLabel(
            stock_frame,
            text="Estoque",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=8,
            pady=(8, 4)
        )

        self._create_button(
            stock_frame,
            "Simular reserva",
            "simulate",
            1,
            0
        )

        self._create_button(
            stock_frame,
            "Reservar estoque",
            "reserve",
            1,
            1
        )

        withdraw_text = (
            "Estoque baixado"
            if self.order.stock_withdrawn
            else "Baixar estoque"
        )

        self._create_button(
            stock_frame,
            withdraw_text,
            "withdraw",
            2,
            0
        )

        self._create_button(
            stock_frame,
            "Cancelar reserva",
            "cancel_reservation",
            2,
            1
        )

        # =================================================
        # DOCUMENTOS
        # =================================================

        documents_frame = ctk.CTkFrame(
            self
        )

        documents_frame.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=0,
            pady=(0, 8)
        )

        self._configure_columns(
            documents_frame
        )

        title = ctk.CTkLabel(
            documents_frame,
            text="Documentos",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            padx=8,
            pady=(8, 4)
        )

        artwork_button = ctk.CTkButton(
            documents_frame,
            text="Adicionar arte",
            command=self._add_artwork,
            height=38
        )

        artwork_button.grid(
            row=1,
            column=0,
            padx=4,
            pady=4,
            sticky="ew"
        )

        self._create_button(
            documents_frame,
            "Visualizar comanda",
            "preview_command",
            1,
            1
        )

        self._create_button(
            documents_frame,
            "Exportar PDF",
            "export_command_pdf",
            2,
            0,
            columnspan=2
        )

        # =================================================
        # ÁUDIO
        # =================================================

        if (
            self.order.audio_id
            and self.callbacks.get("audio")
        ):

            audio_frame = ctk.CTkFrame(
                self
            )

            audio_frame.grid(
                row=4,
                column=0,
                sticky="ew",
                padx=0,
                pady=(0, 8)
            )

            audio_frame.grid_columnconfigure(
                0,
                weight=1
            )

            title = ctk.CTkLabel(
                audio_frame,
                text="Áudio",
                font=ctk.CTkFont(
                    size=16,
                    weight="bold"
                )
            )

            title.grid(
                row=0,
                column=0,
                sticky="w",
                padx=8,
                pady=(8, 4)
            )

            audio_button = ctk.CTkButton(
                audio_frame,
                text="▶ Ouvir áudio",
                command=self.callbacks["audio"],
                height=38
            )

            audio_button.grid(
                row=1,
                column=0,
                padx=4,
                pady=4,
                sticky="ew"
            )

    # =====================================================
    # ADICIONAR ARTE
    # =====================================================

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