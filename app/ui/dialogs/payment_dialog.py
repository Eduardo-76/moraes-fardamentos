import customtkinter as ctk
from tkinter import messagebox

from app.services.payment_service import PaymentService


class PaymentDialog(ctk.CTkToplevel):
    def __init__(
        self,
        master,
        order_id: int,
        total_value: float,
        on_save=None,
    ) -> None:
        super().__init__(master)

        self.order_id = order_id
        self.total_value = float(total_value or 0)
        self.on_save = on_save

        self.payment_service = PaymentService()

        self.title("Registrar pagamento")
        self.geometry("420x330")
        self.resizable(False, False)

        self.transient(master)
        self.grab_set()

        self._build()

    def _build(self) -> None:
        self.grid_columnconfigure(0, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Registrar pagamento",
            font=ctk.CTkFont(
                size=22,
                weight="bold",
            ),
        )
        title.grid(
            row=0,
            column=0,
            padx=24,
            pady=(24, 18),
            sticky="w",
        )

        value_label = ctk.CTkLabel(
            self,
            text="Valor",
            font=ctk.CTkFont(size=14),
        )
        value_label.grid(
            row=1,
            column=0,
            padx=24,
            pady=(0, 6),
            sticky="w",
        )

        self.amount_entry = ctk.CTkEntry(
            self,
            placeholder_text="Ex.: 100,00",
            height=40,
        )
        self.amount_entry.grid(
            row=2,
            column=0,
            padx=24,
            pady=(0, 14),
            sticky="ew",
        )
        self.amount_entry.focus()

        method_label = ctk.CTkLabel(
            self,
            text="Forma de pagamento",
            font=ctk.CTkFont(size=14),
        )
        method_label.grid(
            row=3,
            column=0,
            padx=24,
            pady=(0, 6),
            sticky="w",
        )

        self.method_combobox = ctk.CTkComboBox(
            self,
            values=list(
                self.payment_service.PAYMENT_METHODS
            ),
            height=40,
        )
        self.method_combobox.grid(
            row=4,
            column=0,
            padx=24,
            pady=(0, 22),
            sticky="ew",
        )
        self.method_combobox.set("Pix")

        buttons_frame = ctk.CTkFrame(self)
        buttons_frame.grid(
            row=5,
            column=0,
            padx=24,
            pady=(0, 20),
            sticky="ew",
        )

        buttons_frame.grid_columnconfigure(
            0,
            weight=1,
        )
        buttons_frame.grid_columnconfigure(
            1,
            weight=1,
        )

        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            command=self.destroy,
            height=40,
        )
        cancel_button.grid(
            row=0,
            column=0,
            padx=(0, 6),
            sticky="ew",
        )

        register_button = ctk.CTkButton(
            buttons_frame,
            text="Registrar pagamento",
            command=self._register_payment,
            height=40,
        )
        register_button.grid(
            row=0,
            column=1,
            padx=(6, 0),
            sticky="ew",
        )

        self.bind(
            "<Return>",
            lambda event: self._register_payment(),
        )

        self.bind(
            "<Escape>",
            lambda event: self.destroy(),
        )

    def _parse_amount(self) -> float:
        value = self.amount_entry.get().strip()

        if not value:
            raise ValueError(
                "Informe o valor do pagamento."
            )

        # Aceita formatos brasileiros:
        # 100,50
        # 1.000,50
        # Também aceita 100.50.
        if "," in value:
            value = value.replace(
                ".",
                "",
            ).replace(
                ",",
                ".",
            )
        else:
            value = value.replace(
                " ",
                "",
            )

        try:
            amount = float(value)
        except ValueError as exc:
            raise ValueError(
                "Informe um valor válido."
            ) from exc

        if amount <= 0:
            raise ValueError(
                "O valor do pagamento deve ser "
                "maior que zero."
            )

        return amount

    def _register_payment(self) -> None:
        try:
            amount = self._parse_amount()
            method = self.method_combobox.get().strip()

            self.payment_service.register_payment(
                order_id=self.order_id,
                amount=amount,
                payment_method=method,
                total_value=self.total_value,
            )

        except ValueError as exc:
            messagebox.showwarning(
                "Pagamento",
                str(exc),
                parent=self,
            )
            return

        except Exception as exc:
            messagebox.showerror(
                "Erro",
                "Não foi possível registrar "
                f"o pagamento.\n\n{exc}",
                parent=self,
            )
            return

        if callable(self.on_save):
            self.on_save()

        self.destroy()