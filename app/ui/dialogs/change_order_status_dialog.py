import customtkinter as ctk

from tkinter import messagebox

from app.services.order_service import OrderService


class ChangeOrderStatusDialog(ctk.CTkToplevel):

    STATUS_OPTIONS = [
        "Em espera",
        "Em produção",
        "Aguardando aprovação",
        "Pronto",
        "Entregue",
        "Cancelado",
    ]

    def __init__(
        self,
        master,
        order,
        on_save=None,
    ):
        super().__init__(master)

        self.order = order
        self.on_save = on_save

        self.service = OrderService()

        self.title("Alterar Status")
        self.geometry("520x360")

        self.transient(master)
        self.grab_set()

        self._build()

    def _build(self):

        title = ctk.CTkLabel(
            self,
            text="Alterar Status",
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
            text=f"Pedido #{self.order.id}\n{self.order.client_name}",
            justify="center"
        )
        subtitle.pack()

        ctk.CTkLabel(
            self,
            text="Novo status"
        ).pack(
            anchor="w",
            padx=30,
            pady=(25,5)
        )

        self.status_option = ctk.CTkOptionMenu(
            self,
            values=self.STATUS_OPTIONS
        )

        self.status_option.pack(
            fill="x",
            padx=30
        )

        self.status_option.set(
            self.order.status
        )

        ctk.CTkLabel(
            self,
            text="Observação"
        ).pack(
            anchor="w",
            padx=30,
            pady=(20,5)
        )

        self.notes = ctk.CTkTextbox(
            self,
            height=90
        )

        self.notes.pack(
            fill="both",
            padx=30
        )


        buttons = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        buttons.pack(
            pady=20
        )

        ctk.CTkButton(
            buttons,
            text="Cancelar",
            command=self.destroy
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            buttons,
            text="Salvar",
            command=self._save
        ).pack(
            side="left",
            padx=10
        )       

    def _save(self):

        try:

            self.service.change_status(
                order_id=self.order.id,
                new_status=self.status_option.get(),
                notes=self.notes.get(
                    "1.0",
                    "end"
                ).strip()
            )

            if callable(self.on_save):
                self.on_save()

            self.destroy()

        except Exception as e:

            messagebox.showerror(
                "Erro",
                str(e)
            )