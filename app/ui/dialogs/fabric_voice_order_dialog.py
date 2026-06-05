import customtkinter as ctk


class FabricVoiceOrderDialog(ctk.CTkToplevel):

    def __init__(
        self,
        master,
        client_name,
        quantity,
        product_name,
        on_confirm=None
    ):
        super().__init__(master)

        self.client_name = client_name
        self.quantity = quantity
        self.product_name = product_name

        self.on_confirm = on_confirm

        self.title("Confirmar pedido")

        self.geometry("420x360")

        self.transient(master)

        self.grab_set()

        self._build_ui()

    def _build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="Pedido detectado",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        title.pack(pady=(20, 10))

        content = ctk.CTkFrame(self)

        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        # CLIENTE

        client_label = ctk.CTkLabel(
            content,
            text=f"Cliente:\n{self.client_name}",
            justify="left",
            anchor="w"
        )

        client_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # PRODUTO

        product_label = ctk.CTkLabel(
            content,
            text=f"Produto:\n{self.product_name}",
            justify="left",
            anchor="w"
        )

        product_label.pack(
            anchor="w",
            padx=20,
            pady=10
        )

        # QUANTIDADE

        quantity_label = ctk.CTkLabel(
            content,
            text=f"Quantidade:\n{self.quantity}",
            justify="left",
            anchor="w"
        )

        quantity_label.pack(
            anchor="w",
            padx=20,
            pady=10
        )

        # BOTÕES

        buttons_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        buttons_frame.pack(
            pady=20
        )

        cancel_btn = ctk.CTkButton(
            buttons_frame,
            text="Cancelar",
            fg_color="#DC2626",
            hover_color="#991B1B",
            command=self.destroy
        )

        cancel_btn.pack(
            side="left",
            padx=10
        )

        confirm_btn = ctk.CTkButton(
            buttons_frame,
            text="Confirmar",
            command=self._confirm
        )

        confirm_btn.pack(
            side="left",
            padx=10
        )

    def _confirm(self):

        self.destroy()

        if self.on_confirm:

            self.after(
                100,
                self.on_confirm
            )