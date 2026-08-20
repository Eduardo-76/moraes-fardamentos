import customtkinter as ctk


class OrderSummary(ctk.CTkFrame):

    def __init__(
        self,
        master,
        order,
    ):
        super().__init__(master)

        self.order = order
        self._build()

    def _build(self):

        self.grid_columnconfigure(
            0,
            weight=1
        )

        title = ctk.CTkLabel(
            self,
            text=self.order.client_name or "Sem cliente",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=16,
            pady=(16, 8)
        )

        self.summary_frame = ctk.CTkFrame(self)

        self.summary_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=12,
            pady=(0, 12)
        )

        self.summary_frame.grid_columnconfigure(
            0,
            weight=1
        )      

        self._build_info()
           
    def _build_info(self):
        info_frame = ctk.CTkFrame(
            self.summary_frame
        )

        info_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8),
            pady=8
        )

        info_frame.grid_columnconfigure(
            0,
            weight=1
        )

        title = ctk.CTkLabel(
            info_frame,
            text="Resumo do Pedido",
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=12,
            pady=(12, 10)
        )   

        fields = [
            ("Modelo", self.order.model),
            ("Tipo", self.order.type),
            ("Tecido", self.order.fabric),
            ("Quantidade", f"{self.order.quantity} peças" if self.order.quantity else "-"),
            ("Prazo", self.order.deadline),
            ("Prioridade", self.order.priority),
        ]    

        for index, (label, value) in enumerate(fields, start=1):

            display = value if value is not None else "-"

            ctk.CTkLabel(
                info_frame,
                text=f"{label}: {display}",
                anchor="w"
            ).grid(
                row=index,
                column=0,
                sticky="w",
                padx=12,
                pady=2
            ) 
