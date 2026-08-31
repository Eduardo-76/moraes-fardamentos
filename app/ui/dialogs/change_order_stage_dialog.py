import customtkinter as ctk

from tkinter import messagebox

from app.core.constants import ORDER_STAGES
from app.services.order_service import OrderService


class ChangeOrderStageDialog(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        order,
        on_save=None
    ):
        super().__init__(master)

        self.order = order
        self.on_save = on_save

        self.service = OrderService()

        self.title("Mover Etapa")
        self.geometry("520x320")

        self.transient(master)
        self.grab_set()

        self._build()

    def _build(self):

        title = ctk.CTkLabel(
            self,
            text="Mover Etapa da Produção",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        title.pack(
            pady=(20,10)
        )

        subtitle = ctk.CTkLabel(
            self,
            text=(
                f"Pedido #{self.order.id}\n"
                f"{self.order.client_name}"
            ),
            justify="center"
        )

        subtitle.pack()

        ctk.CTkLabel(
            self,
            text="Nova etapa"
        ).pack(
            anchor="w",
            padx=30,
            pady=(25,5)
        )

        self.stage_option = ctk.CTkOptionMenu(
            self,
            values=ORDER_STAGES
        )

        self.stage_option.pack(
            fill="x",
            padx=30
        )

        self.stage_option.set(
            self.order.current_stage
        )

        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.pack(
            fill="x",
            padx=30,
            pady=25
        )

        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=self.destroy,
            fg_color="#374151",
            hover_color="#1F2937",
        )

        cancel_button.pack(
            side="left"
        )

        save_button = ctk.CTkButton(
            buttons_frame,
            text="Salvar alteração",
            command=self._save,
        )

        save_button.pack(
            side="right"
        )

    def _save(self):

        new_stage = self.stage_option.get()

        if new_stage == self.order.current_stage:
            messagebox.showinfo(
                "Nenhuma alteração",
                "O pedido já está nesta etapa."
            )
            return

        confirmed = messagebox.askyesno(
            "Confirmar alteração",
            (
                f"Alterar o pedido #{self.order.id}?\n\n"
                f"Etapa atual: {self.order.current_stage}\n"
                f"Nova etapa: {new_stage}"
            )
        )

        if not confirmed:
            return

        try:

            self.service.update_stage(
                self.order.id,
                new_stage
            )

            if callable(self.on_save):
                self.on_save()

            self.destroy()

        except Exception as exc:

            messagebox.showerror(
                "Erro",
                str(exc)
            )