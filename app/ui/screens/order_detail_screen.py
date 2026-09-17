import customtkinter as ctk
from app.services.audio_service import AudioService
from app.core.constants import MESSAGE_SECTORS, STAGE_STATUS_COLORS
from app.services.order_service import OrderService
from app.ui.components.message_generator import MessageGenerator
from app.ui.dialogs.order_form_dialog import OrderFormDialog
from app.ui.dialogs.order_stock_withdraw_dialog import OrderStockWithdrawDialog
from app.services.stock_service import StockService
from app.ui.dialogs.select_stock_dialog import SelectStockDialog
from app.ui.dialogs.change_order_status_dialog import (
    ChangeOrderStatusDialog
)
from app.ui.components.order_summary import OrderSummary
from app.ui.components.order_command import OrderCommand
from tkinter import messagebox
from app.ui.components.production_flow import ProductionFlow
from app.ui.components.order_actions import OrderActions
from app.printing.command_printer import CommandPrinter
from app.services.payment_service import PaymentService
from app.ui.dialogs.payment_dialog import PaymentDialog


class OrderDetailScreen(ctk.CTkFrame):
    def __init__(self, master, order_id: int, on_back=None) -> None:
        super().__init__(master)

        self.order_id = order_id
        self.on_back = on_back
        self.order_service = OrderService()
        self.stock_service = StockService()
        self.payment_service = PaymentService()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self._build_header()
        self._build_content()

        self.command_printer = CommandPrinter()

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

        self.content_frame.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=8,
            pady=8
        )

        self.content_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self._render_content()

    def _render_content(self) -> None:

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.order = self.order_service.get_order_by_id(
            self.order_id
        )

        order = self.order

        if not order:

            label = ctk.CTkLabel(
                self.content_frame,
                text="Pedido não encontrado.",
                font=ctk.CTkFont(size=16)
            )

            label.grid(
                row=0,
                column=0,
                padx=16,
                pady=16,
                sticky="w"
            )

            return

        # =====================================================
        # RESUMO + COMANDA
        # =====================================================

        summary = OrderSummary(
            self.content_frame,
            order=self.order
        )

        summary.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=8,
            pady=8
        )

        command_text = (
            self.order_service
            .build_order_command_text(
                self.order_id
            )
        )

        command = OrderCommand(
            self.content_frame,
            command_text=command_text,
            callbacks={
                "copy_command": lambda: self._copy_text(
                    command_text
                )
            }
        )

        command.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=8,
            pady=(0, 8)
        )

        # =====================================================
        # ÁUDIO
        # =====================================================

        audio_callback = None

        if self.order.audio_id:

            audio_service = AudioService()

            audio = audio_service.get_audio_by_id(
                self.order.audio_id
            )

            if audio:

                audio_callback = (
                    lambda p=audio.file_path:
                    audio_service.open_audio(p)
                )

        # =====================================================
        # AÇÕES
        # =====================================================

        actions = OrderActions(
            self.content_frame,
            order=self.order,
            callbacks={
                "edit": self._open_edit_dialog,
                "status": self._change_status,

                "previous_stage": self._move_previous,
                "next_stage": self._move_next,

                "simulate": self._simulate_stock_reservation,
                "reserve": self._reserve_stock,
                "cancel_reservation": self._cancel_reservation,
                "withdraw": self._open_stock_withdraw_dialog,

                "audio": audio_callback,

                "preview_command": self._preview_command,
                "export_command_pdf": self._export_command_pdf,
            }
        )

        actions.grid(
            row=2,
            column=0,
            sticky="ew",
            padx=8,
            pady=(0, 8)
        )

        # =====================================================
        # FLUXO DE PRODUÇÃO
        # =====================================================

        flow = ProductionFlow(
            self.content_frame,
            self.order
        )

        flow.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=8,
            pady=(0, 8)
        )

        # =====================================================
        # DETALHES DAS ETAPAS
        # =====================================================

        self._build_stage_details()

        # =====================================================
        # FINANCEIRO
        # =====================================================

        self._build_financial_section()

        # =====================================================
        # GERADOR DE MENSAGEM
        # =====================================================

        message_component = MessageGenerator(
            self.content_frame,
            order_service=self.order_service,
            order_id=self.order_id,
            copy_callback=self._copy_text
        )

        message_component.grid(
            row=7,
            column=0,
            sticky="ew",
            padx=8,
            pady=8
        )

    def _build_stage_details(self) -> None:
        stages = self.order_service.list_order_stages(
            self.order_id
        )

        frame = ctk.CTkFrame(self.content_frame)

        frame.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=8,
            pady=(0, 8)
        )

        frame.grid_columnconfigure(
            0,
            weight=1
        )

        title = ctk.CTkLabel(
            frame,
            text="Detalhes das etapas",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=16,
            pady=(14, 10)
        )

        if not stages:
            label = ctk.CTkLabel(
                frame,
                text="Nenhuma informação de etapa disponível."
            )

            label.grid(
                row=1,
                column=0,
                sticky="w",
                padx=16,
                pady=(0, 14)
            )

            return

        for index, stage in enumerate(stages):

            stage_frame = ctk.CTkFrame(
                frame
            )

            stage_frame.grid(
                row=index + 1,
                column=0,
                sticky="ew",
                padx=12,
                pady=5
            )

            stage_frame.grid_columnconfigure(
                0,
                weight=1
            )

            stage_name = stage.get(
                "stage_name"
            ) or "Etapa"

            status = stage.get(
                "status"
            ) or "Em espera"

            started_at = stage.get(
                "started_at"
            )

            finished_at = stage.get(
                "finished_at"
            )

            status_text = f"Status: {status}"

            if started_at:
                status_text += f"\nInício: {started_at}"

            if finished_at:
                status_text += f"\nConclusão: {finished_at}"

            stage_label = ctk.CTkLabel(
                stage_frame,
                text=stage_name,
                font=ctk.CTkFont(
                    size=15,
                    weight="bold"
                )
            )

            stage_label.grid(
                row=0,
                column=0,
                sticky="w",
                padx=12,
                pady=(10, 2)
            )

            info_label = ctk.CTkLabel(
                stage_frame,
                text=status_text,
                justify="left",
                font=ctk.CTkFont(
                    size=13
                )
            )

            info_label.grid(
                row=1,
                column=0,
                sticky="w",
                padx=12,
                pady=(0, 10)
            )


    def _build_financial_section(self) -> None:
        frame = ctk.CTkFrame(self.content_frame)

        frame.grid(
            row=5,
            column=0,
            sticky="ew",
            padx=8,
            pady=(0, 8)
        )

        frame.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            frame,
            text="Financeiro",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            padx=16,
            pady=(14, 12),
            sticky="w"
        )

        total_value = float(
            self.order.total_value or 0
        )

        total_paid = self.payment_service.get_total_paid(
            self.order_id
        )

        remaining = self.payment_service.get_remaining_amount(
            self.order_id,
            total_value
        )

        status = self.payment_service.get_payment_status(
            self.order_id,
            total_value
        )

        # =================================================
        # RESUMO FINANCEIRO
        # =================================================

        summary_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        summary_frame.grid(
            row=1,
            column=0,
            padx=16,
            pady=(0, 12),
            sticky="ew"
        )

        summary_frame.grid_columnconfigure(
            0,
            weight=1
        )

        summary_frame.grid_columnconfigure(
            1,
            weight=1
        )

        summary_frame.grid_columnconfigure(
            2,
            weight=1
        )

        summary_frame.grid_columnconfigure(
            3,
            weight=1
        )

        self._create_financial_value(
            summary_frame,
            row=0,
            column=0,
            title="Valor final",
            value=f"R$ {total_value:.2f}"
        )

        self._create_financial_value(
            summary_frame,
            row=0,
            column=1,
            title="Total pago",
            value=f"R$ {total_paid:.2f}"
        )

        self._create_financial_value(
            summary_frame,
            row=0,
            column=2,
            title="A receber",
            value=f"R$ {remaining:.2f}"
        )

        self._create_financial_value(
            summary_frame,
            row=0,
            column=3,
            title="Status",
            value=status
        )

        # =================================================
        # BOTÃO PAGAMENTO
        # =================================================

        register_button = ctk.CTkButton(
            frame,
            text="+ Registrar pagamento",
            height=40,
            command=self._open_payment_dialog
        )

        register_button.grid(
            row=2,
            column=0,
            padx=16,
            pady=(0, 16),
            sticky="w"
        )

        if remaining <= 0:
            register_button.configure(
                state="disabled"
            )

        # =================================================
        # HISTÓRICO
        # =================================================

        history_title = ctk.CTkLabel(
            frame,
            text="Histórico de pagamentos",
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        history_title.grid(
            row=3,
            column=0,
            padx=16,
            pady=(0, 8),
            sticky="w"
        )

        payments = self.payment_service.list_payments(
            self.order_id
        )

        if not payments:
            empty_label = ctk.CTkLabel(
                frame,
                text="Nenhum pagamento registrado."
            )

            empty_label.grid(
                row=4,
                column=0,
                padx=16,
                pady=(0, 16),
                sticky="w"
            )

            return

        history_frame = ctk.CTkFrame(
            frame,
            fg_color="transparent"
        )

        history_frame.grid(
            row=4,
            column=0,
            padx=16,
            pady=(0, 16),
            sticky="ew"
        )

        history_frame.grid_columnconfigure(
            0,
            weight=1
        )

        history_frame.grid_columnconfigure(
            1,
            weight=1
        )

        history_frame.grid_columnconfigure(
            2,
            weight=1
        )

        for index, payment in enumerate(payments):

            paid_at = payment.paid_at or ""

            if paid_at:
                try:
                    from datetime import datetime

                    paid_at_dt = datetime.strptime(
                        paid_at,
                        "%Y-%m-%d %H:%M:%S"
                    )

                    paid_at = paid_at_dt.strftime(
                        "%d/%m/%Y %H:%M"
                    )

                except ValueError:
                    pass

            date_label = ctk.CTkLabel(
                history_frame,
                text=paid_at
            )

            date_label.grid(
                row=index,
                column=0,
                padx=(0, 12),
                pady=5,
                sticky="w"
            )

            method_label = ctk.CTkLabel(
                history_frame,
                text=payment.payment_method
            )

            method_label.grid(
                row=index,
                column=1,
                padx=12,
                pady=5,
                sticky="w"
            )

            amount_label = ctk.CTkLabel(
                history_frame,
                text=f"R$ {payment.amount:.2f}"
            )

            amount_label.grid(
                row=index,
                column=2,
                padx=(12, 0),
                pady=5,
                sticky="e"
            )


    def _create_financial_value(
        self,
        parent,
        row: int,
        column: int,
        title: str,
        value: str
    ) -> None:

        title_label = ctk.CTkLabel(
            parent,
            text=title,
            font=ctk.CTkFont(
                size=13
            )
        )

        title_label.grid(
            row=row,
            column=column,
            padx=8,
            pady=(0, 2),
            sticky="w"
        )

        value_label = ctk.CTkLabel(
            parent,
            text=value,
            font=ctk.CTkFont(
                size=16,
                weight="bold"
            )
        )

        value_label.grid(
            row=row + 1,
            column=column,
            padx=8,
            pady=(0, 4),
            sticky="w"
        )


    def _open_payment_dialog(self) -> None:
        total_value = float(
            self.order.total_value or 0
        )

        PaymentDialog(
            self,
            order_id=self.order_id,
            total_value=total_value,
            on_save=self._handle_payment_saved
        )


    def _handle_payment_saved(self) -> None:
        self._render_content()

    def _move_next(self) -> None:
        try:
            self.order_service.move_to_next_stage(self.order_id)
            self._render_content()

        except Exception as exc:
            messagebox.showerror(
                "Erro ao avançar etapa",
                str(exc)
            )


    def _move_previous(self) -> None:
        try:
            self.order_service.move_to_previous_stage(self.order_id)
            self._render_content()

        except Exception as exc:
            messagebox.showerror(
                "Erro ao voltar etapa",
                str(exc)
            )

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
                order
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

    def _reserve_stock(self):

        dialog = SelectStockDialog(self)

        self.wait_window(dialog)

        if not dialog.result:
            return

        stock_id = dialog.result

        try:

            result = self.order_service.reserve_order_stock(
                self.order_id,
                stock_id
            )

            text = "RESERVA REALIZADA\n\n"

            for item in result:

                text += (
                    f"{item['size']} "
                    f"{item['gender']}\n"
                    f"Reservado: {item['reserved']}\n"
                    f"Faltam: {item['missing']}\n\n"
                )

        except Exception as e:

            text = str(e)

        dialog = ctk.CTkToplevel(self)

        dialog.title(
            "Reserva de Estoque"
        )

        dialog.geometry(
            "500x400"
        )

        textbox = ctk.CTkTextbox(dialog)

        textbox.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        textbox.insert(
            "1.0",
            text
        )

        self._render_content()

    def _cancel_reservation(self):

        reservations = (
            self.stock_service
            .list_active_by_order(self.order_id)
        )

        if not reservations:
            messagebox.showinfo(
                "Reserva",
                "Este pedido não possui reservas ativas."
            )
            return

        try:

            for reservation in reservations:

                self.stock_service.cancel_reservation(
                    reservation["id"]
                )

            messagebox.showinfo(
                "Reserva",
                "Reserva cancelada com sucesso."
            )

            self._render_content()

        except Exception as e:

            messagebox.showerror(
                "Erro",
                str(e)
            )


    def _change_status(self):

        dialog = ChangeOrderStatusDialog(
            self,
            order=self.order,
            on_save=self._reload_order
        )

        self.wait_window(dialog)

    def _reload_order(self):

        self.order = self.order_service.get_order_by_id(
            self.order_id
        )

        self._render_content()

    def _copy_text(
        self,
        text: str
    ):
        self.clipboard_clear()
        self.clipboard_append(text)

        messagebox.showinfo(
            "Sucesso",
            "Texto copiado."
        )

    def _preview_command(self):

        self.command_printer.preview(
            self.order_id
        )

    def _export_command_pdf(self):

        self.command_printer.export_pdf(
            self.order_id
        )

